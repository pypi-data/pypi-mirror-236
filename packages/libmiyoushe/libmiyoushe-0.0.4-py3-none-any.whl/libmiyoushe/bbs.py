import pprint
import time

from delta import Delta

from . import *
from . import urls, threadRender
import logging

from .base import connectApi, headerGenerate

logger = logging.getLogger('libhoyolab.bbs')


def articleSet(raw_articles: list, method: str = 'normal') -> list:
    """
    生成简化后的文章流
    :param raw_articles: 原来的文章流
    :param method: 文章流类型
    :return:
    """
    articles = list()
    for articleInfo in raw_articles:
        try:
            article = dict()
            if method == 'history':
                articleInfo = articleInfo['post']
            article['post_id'] = articleInfo['post']['post_id']
            article['title'] = articleInfo['post']['subject']
            article['describe'] = articleInfo['post']['content'][:50] + str(
                "..." if len(articleInfo['post']['content']) > 50 else '')
            try:
                article['cover'] = articleInfo['post']['images'][0] if articleInfo['post']['cover'] == "" else \
                    articleInfo['post']['cover']
            except:
                article['cover'] = ''
            article['authorAvatar'] = articleInfo['user']['avatar_url']
            article['uid'] = int(articleInfo['user']['uid'])
            article['authorName'] = articleInfo['user']['nickname']
            describe = articleInfo['user']['certification']['label'] if len(
                articleInfo['user']['certification']['label']) > 0 else articleInfo['user']['introduce'][
                                                                        :15] + '...' if len(
                articleInfo['user']['introduce']) > 15 else ''
            article['authorDescribe'] = describe
            article['type'] = articleInfo['post']['view_type']
            article['upvote'] = bool(articleInfo['self_operation']['attitude'])
            article['collect'] = bool(articleInfo['self_operation']['is_collected'])
            articles.append(article)
        except Exception as e:
            print(type(e), e)
            continue

    return articles


def getEmotions(gid: str | int = '2') -> dict:
    """
    获取表情包所对应的图片路径
    :param gid:
    :return: dict
    """
    logger.info('emotion lib is running')
    emotionDict = dict()
    req = session.get(urls.emoticon_set.format(str(gid)), verify=False)
    contents = json.loads(req.content.decode("utf8"))['data']['list']

    for emotionSet in contents:
        for emotion in emotionSet['list']:
            emotionDict[emotion['name']] = emotion['icon']

    return emotionDict


def getGame(game):
    resp = connectApi(urls.getGameList)
    if game == 'all':
        game_list = list()
        for item in resp.json()['data']['list']:
            game_list.append([item['name'], item['id'], item['op_name'], item['en_name']])
        return game_list
    else:
        for item in resp.json()['data']['list']:
            if item['en_name'] == game or item['name'] == game or item['op_name'] == game or item['id'] == game:
                return [item['name'], item['id'], item['op_name'], item['en_name']]
        return ['', 0, '']


class Article:
    """
    文章类：从服务器索取文章信息
    """

    def __init__(self, post_id):
        """
        初始化文章类
        :param post_id: 文章id
        """
        logger.info(f'getting article from {post_id}')
        logger.info('accessing ' + urls.getPostFull.format(str(post_id)))
        headers = headerGenerate(app='web')
        resp = connectApi(urls.getPostFull.format(str(post_id)), headers=headers)
        self.result = resp.json()

    def getReleasedTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S",
                             time.localtime(int(self.result['data']['post']['post']['created_at'])))

    def getContent(self) -> str:
        """
        获取文章内容(基于HTML)
        :return:
        """
        return threadRender.replaceAll(self.result["data"]['post']['post']['content'],
                                       emotionDict=getEmotions(gid=self.result["data"]['post']['post']['game_id']))

    def getStructuredContent(self) -> str:
        """
        获取结构化的文章内容（基于Quill的Delta）
        :return:
        """
        structured = self.result["data"]["post"]["post"]["structured_content"]
        return threadRender.replaceAllFromDelta(structured, emotionDict=getEmotions(
            gid=self.result["data"]['post']['post']['game_id']))

    def getVideo(self) -> str:
        """
        获取视频及其不同的清晰度
        :return:
        """
        return json.dumps(self.result["data"]["post"]["vod_list"])

    def getSelfAttitude(self) -> bool:
        """
        获取用户是否给文章点赞
        :return:
        """
        return bool(self.result['data']['post']['self_operation']['attitude'])

    def getSelfCollect(self) -> bool:
        """
        获取用户是否给文章收藏
        :return:
        """
        return bool(self.result['data']['post']['self_operation']['is_collected'])

    def getVotes(self) -> int:
        """
        获取文章的点赞数
        :return:
        """
        return int(self.result['data']['post']['stat']['like_num'])

    def getCollects(self) -> int:
        """
        获取文章的收藏数
        :return:
        """
        return int(self.result['data']['post']['stat']['bookmark_num'])

    def getAuthorDescribe(self) -> str:
        """
        获取作者简介
        :return:
        """
        return f"{self.result['data']['post']['user']['certification']['label'] if len(self.result['data']['post']['user']['certification']['label']) > 0 else self.result['data']['post']['user']['introduce']}"

    def getTags(self) -> list:
        """
        获取文章标签
        :return:
        """
        tags = list()
        for tag in self.result['data']['post']['topics']:
            tags.append({
                'name': tag['name'],
                'cover': tag['cover'],
                'id': tag['id']
            })
        return tags


class Page:
    """
    文章流类
    """

    def __init__(self, gid, pageType, page=1, pageSize=50):
        """
        初始化文章流类
        :param gid: 论坛板块id
        :param pageType: 文章流类型
        :param page: 页数
        :param pageSize: 单次获取的最大的文章数量
        """
        self.page = page
        logger.info('getting page')
        if pageType == 'recommend':
            apiUrl = urls.webHome.format(str(gid), str(page), str(pageSize))
        elif pageType == 'feed':
            apiUrl = urls.feedPosts.format(str(gid))
        else:
            if pageType not in newsType:
                typeNum = '1'
            else:
                typeNum = newsType[pageType]
            apiUrl = urls.getNewsList.format(str(gid), str(typeNum), str(pageSize),
                                             str(abs((int(page) - 1) * int(pageSize))))
        logger.info('accessing ' + apiUrl)
        header = headerGenerate(app='app', client='2')
        req = connectApi(apiUrl, headers=header)
        result = req.json()
        self.articles = articleSet(result['data']['recommended_posts' if pageType == 'recommend' else 'list'])


class Forum:

    def __init__(self, forum_id, gid, last_id='', pageSize=20, is_hot=False, sort_type=1):
        apiUrl = urls.getForumPostList.format(str(forum_id), str(gid), 'false', str(is_hot).lower(), str(pageSize),
                                              str(sort_type), str(last_id))  # str(last_id)
        resp = connectApi(apiUrl=apiUrl).json()
        self.articles = articleSet(resp['data']['list'])
        self.is_last = resp['data']['is_last']
        self.last_id = resp['data']['last_id']

    @staticmethod
    def getAllForum():
        resp = connectApi(urls.getAllGamesForums)
        data_list = resp.json()['data']['list']
        forums = dict()
        for game in data_list:
            tmp_list = list()
            for forum in game['forums']:
                tmp_list.append({'id': forum['id'], 'name': forum['name'], 'game_id': forum['game_id']})
            forums[str(game['game_id'])] = tmp_list
        return forums


class Comments:
    """
    评论流类
    """

    def __init__(self, post_id, gid, page=1, max_size=20, rank_by_hot=True, orderby=1, only_master=False):
        """
        初始化评论流类
        :param post_id: 文章id
        :param gid: 游戏id
        :param page: 页数
        :param max_size: 单次获取的最大的评论数量
        :param rank_by_hot: 是否按热度排序
        :param orderby: 排序方式（1.最早，2.最新）
        :param only_master: 仅楼主
        """
        self.page = int(page)
        self.post_id = post_id
        self.gid = str(gid)
        start = abs((int(page) - 1) * int(max_size))
        logger.info(f"getting comments from {post_id}, start from {start}")
        emotionDict = getEmotions(gid)
        apiUrl = urls.getPostReplies.format(str(gid), str(rank_by_hot).lower(), str(post_id), str(max_size),
                                            str(start), str(orderby), str(only_master).lower())
        logger.info("accessing " + apiUrl)
        header = headerGenerate(app='app', client='2', Referer='https://app.mihoyo.com')
        resp = connectApi(apiUrl, headers=header)
        result = resp.json()
        self.rank_by_hot = rank_by_hot
        self.comments = []
        comments: list = [None] * (max_size + 1) if rank_by_hot else [None] * max_size
        self.have_top = False
        self.isLastFlag = result['data']['is_last']
        comments_raw = result['data']['list']
        for i in range(len(comments_raw)):
            try:
                reply = comments_raw[i]
                tmp = {
                    'reply_id': reply['reply']['reply_id'],
                    'floor_id': reply['reply']['floor_id'],
                    'post_id': reply['reply']['post_id'],
                    'content': threadRender.replaceAllFromDelta(reply['reply']['struct_content'], emotionDict),
                    'username': reply['user']['nickname'],
                    'uid': int(reply['user']['uid']),
                    'avatar': reply['user']['avatar_url'],
                    'describe': reply['user']['certification']['label'] if len(
                        reply['user']['certification']['label']) > 0 else reply['user']['introduce'],
                    'like_num': reply['stat']['like_num'],
                    'sub_num': int(reply['stat']['sub_num']),
                    'upvoted': bool(reply['self_operation']['reply_vote_attitude']) and bool(
                        reply['self_operation']['attitude'])
                }
                if rank_by_hot:
                    if reply['reply']:
                        comments[0] = tmp
                    else:
                        comments[i + 1] = tmp
                else:
                    comments[i] = tmp
                for reply in comments:
                    if reply is not None:
                        self.comments.append(reply)
            except:
                continue


class RootComment:
    """
    评论类
    """

    def __init__(self, post_id, reply_id):
        """
        初始化评论类
        :param post_id: 文章id
        :param reply_id: 评论id
        """
        self.post_id = post_id
        self.reply_id = reply_id
        logger.info(f"getting root comment {reply_id} in {post_id}")
        logger.info(f"accessing {urls.getRootReplyInfo.format(str(post_id), str(reply_id))}")
        resp = connectApi(urls.getRootReplyInfo.format(str(post_id), str(reply_id))).json()['data']
        emotionDict = getEmotions(resp['reply']['reply']['game_id'])
        self.comment = {
            'reply_id': resp['reply']['reply']['reply_id'],
            'floor_id': resp['reply']['reply']['floor_id'],
            'post_id': resp['reply']['reply']['post_id'],
            'content': threadRender.replaceAllFromDelta(resp['reply']['reply']['struct_content'], emotionDict),
            'username': resp['reply']['user']['nickname'],
            'uid': int(resp['reply']['user']['uid']),
            'avatar': resp['reply']['user']['avatar_url'],
            'describe': resp['reply']['user']['certification']['label'] if len(
                resp['reply']['user']['certification']['label']) > 0 else resp['reply']['user']['introduce'],
            'like_num': resp['reply']['stat']['like_num'],
            'upvoted': bool(resp['reply']['self_operation']['reply_vote_attitude']) and bool(
                resp['reply']['self_operation']['attitude'])
        }


class SubComments:
    """
    楼中楼类
    """

    def __init__(self, post_id, floor_id, last_id=0, gid=2, max_size=20):
        """
        初始化楼中楼类
        :param post_id: 文章id
        :param floor_id: 评论楼层id
        :param last_id: 最后的评论id
        :param gid: 游戏id（仅限获取表情图片）
        :param max_size: 单次获取的最大的评论数量
        """
        self.post_id = post_id
        self.floor_id = floor_id
        self.prev_id = last_id
        self.gid = gid
        logger.info(f"getting sub comments from {floor_id} in {post_id}, start from id {last_id}")
        emotionDict = getEmotions(gid)
        apiUrl = urls.getSubReplies.format(str(post_id), str(floor_id), str(last_id), str(max_size))
        logger.info(f'accessing {apiUrl}')
        header = headerGenerate()
        resp = connectApi(apiUrl=apiUrl, headers=header).json()
        self.comments = list()
        self.isLastFlag = resp['data']['is_last']
        self.last_id = resp['data']['last_id']
        comments_raw = resp['data']['list']
        for reply in comments_raw:
            self.comments.append({
                'reply_id': reply['reply']['reply_id'],
                'post_id': reply['reply']['post_id'],
                'content': threadRender.replaceAllFromDelta(reply['reply']['struct_content'], emotionDict),
                'username': reply['user']['nickname'],
                'uid': int(reply['user']['uid']),
                'avatar': reply['user']['avatar_url'],
                'describe': reply['user']['certification']['label'] if len(
                    reply['user']['certification']['label']) > 0 else reply['user']['introduce'],
                'like_num': reply['stat']['like_num'],
                'upvoted': bool(reply['self_operation']['reply_vote_attitude']) and bool(
                    reply['self_operation']['attitude'])
            })


class Search:
    """
    搜索类
    """

    def __init__(self, keywords, gid, page=1, max_size=20):
        """
        初始化搜索类
        :param keywords: 关键字
        :param gid: 游戏id
        :param page: 页数
        :param max_size: 单次获取的最大的文章数量
        """
        self.gid = gid
        start = int(page)
        logger.info(f'searching {keywords}, from {start}')
        logger.info(f'accessing {urls.searchPosts.format(str(gid), str(keywords), str(start), str(max_size))}')
        req = connectApi(apiUrl=urls.searchPosts.format(str(gid), str(keywords), str(start), str(max_size)))
        result = req.json()
        self.isLastFlag = result['data']['is_last']
        self.articles = articleSet(result['data']['posts'])
        self.results = {'gid': self.gid, 'isLast': self.isLastFlag, 'articles': self.articles}


class User:
    """
    用户类
    """

    def __init__(self, uid=0):
        """
        初始化用户类
        :param uid: 请求的用户uid（若uid为0，则指向已登录的用户）
        """
        self.uid = uid
        logger.info(f"getting user {uid}'s informations")
        logger.info(f"accessing {urls.getUserFullInfo.format(uid)}")
        resp = connectApi(apiUrl=urls.getUserFullInfo.format(uid))
        info = resp.json()
        self.isExist = False
        self.isLogin = False
        if info['retcode'] == 0:
            self.info = info['data']
            self.posts = list()
            if uid == 0:
                self.isLogin = True
            self.isExist = True
        else:
            self.info = dict()
            self.posts = list()

    def getUid(self):
        """
        获取用户uid（若不存在则返回0）
        :return:
        """
        return int(self.info['user_info']['uid']) if self.isExist else 0

    def getNickname(self):
        """
        获取用户昵称
        :return:
        """
        if self.uid == 0:
            return self.info['user_info']['nickname'] if self.isLogin else '未登录'
        else:
            return self.info['user_info']['nickname'] if self.isExist else '用户不存在'

    def getAvatar(self):
        """
        获取用户头像
        :return:
        """
        return self.info['user_info']['avatar_url'] if self.isExist else urls.defaultAvatar

    def getUserPost(self, offset=0, size=20):
        """
        获取用户所发表的文章
        :param offset:
        :param size: 单次获取的最大的文章数量
        :return:
        """
        resp = connectApi(urls.userPost.format(offset, size, self.getUid()))
        posts = resp.json()['data']
        userPosts = dict(isLast=posts['is_last'], posts=articleSet(posts['list']), next=posts['next_offset'])
        return userPosts
    


class Actions:
    """
    操作类
    """

    @staticmethod
    def follow(uid):
        """
        关注用户
        :param uid: 用户uid
        :return:
        """
        logger.info(f"following user {uid}")
        header = headerGenerate(app='app', client='2', Referer='https://app.mihoyo.com')
        resp = connectApi(urls.follow, method='post', headers=header, data={'entity_id': str(uid)}).json()
        logger.info(resp)
        return resp['retcode'], resp['message']

    @staticmethod
    def unfollow(uid):
        """
        取关用户
        :param uid: 用户uid
        :return:
        """
        logger.info(f"unfollowing user {uid}")
        header = headerGenerate(app='app', client='2', Referer='https://app.mihoyo.com')
        resp = connectApi(urls.follow, method='post', headers=header, data={'entity_id': str(uid)}).json()
        logger.info(resp)
        return resp['retcode'], resp['message']

    @staticmethod
    def upvotePost(post_id, isCancel=False):
        """
        文章点赞操作
        :param post_id: 文章id
        :param isCancel: 是否取消点赞
        :return:
        """
        logger.info(f'{"canceling " if isCancel else ""}upvote the post {post_id}')
        header = headerGenerate(app='app', client='2', Referer='https://app.mihoyo.com')
        resp = connectApi(urls.upvotePost, method='post', headers=header,
                          data={"post_id": post_id, "is_cancel": isCancel}).json()
        logger.info(resp)
        return resp['retcode'], resp['message']

    @staticmethod
    def upvoteReply(reply_id, post_id, isCancel=False):
        """
        评论点赞操作
        :param reply_id: 评论id
        :param post_id: 文章id
        :param isCancel: 是否取消点赞
        :return:
        """
        logger.info(f'{"canceling " if isCancel else ""}upvote the reply {reply_id} in {post_id}')
        header = headerGenerate(app='app', client='2', Referer='https://app.mihoyo.com')
        resp = connectApi(urls.upvoteReply, method='post', headers=header,
                          data={"post_id": post_id, "reply_id": reply_id, "is_cancel": isCancel, "gids": '1'}).json()
        logger.info(resp)
        return resp['retcode'], resp['message']

    @staticmethod
    def collectPost(post_id, isCancel=False):
        """
        收藏文章
        :param post_id: 文章id
        :param isCancel: 是否取消收藏
        :return:
        """
        logger.info(f'{"canceling " if isCancel else ""}collect the post{post_id}')
        header = headerGenerate(app='app', client='2', Referer='https://app.mihoyo.com')
        resp = connectApi(urls.collectPost, method='post', headers=header,
                          data={"post_id": post_id, "is_cancel": isCancel}).json()
        return resp['retcode'], resp['message']

    @staticmethod
    def getHistory(offset=''):
        """
        获取用户浏览历史
        :param offset:
        :return:
        """
        logger.info("getting user's history")
        header = headerGenerate(app='app', client='2', Referer='https://app.mihoyo.com')
        resp = connectApi(urls.history.format(str(offset)), headers=header).json()['data']
        # print(resp)
        return {'article': articleSet(resp['list'], method='history'), 'isLast': resp['is_last']}

    @staticmethod
    def releaseReply(text, post_id, reply_id='', delta=None):
        """
        发布评论
        :param delta: 评论的delta结构化信息（基于quill.js）
        :param text: 评论文本
        :param post_id: 发布到的文章uid
        :param reply_id: 回复楼中楼的id
        :return:
        """
        if delta is None:
            delta = {'ops': list(Delta().insert(text))}
        if delta is str:
            delta = json.loads(delta)
        logger.info(f"releasing the reply to post {post_id} with content {text}")
        header = headerGenerate(app='app', client='2', Referer='https://app.mihoyo.com')
        delta = json.dumps(delta['ops'], ensure_ascii=False)
        reply_contents = {
            "content": text,
            "post_id": str(post_id),
            "reply_id": str(reply_id),
            "structured_content": delta
        }
        resp = connectApi(urls.releaseReply, method='post', data=reply_contents, headers=header).json()
        return resp['retcode'], resp['message']

    @staticmethod
    def deleteReply(post_id, reply_id):
        """
        发布评论
        :param post_id: 发布到的文章uid
        :param reply_id: 回复楼中楼的id
        :return:
        """
        logger.info(f"deleting the reply to post {post_id}")
        header = headerGenerate(app='app', client='2', Referer='https://app.mihoyo.com')
        reply_contents = {
            "post_id": str(post_id),
            "reply_id": str(reply_id),
        }
        resp = connectApi(urls.releaseReply, method='post', data=reply_contents, headers=header).json()
        return resp['retcode'], resp['message']
