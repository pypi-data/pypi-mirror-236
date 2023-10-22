import logging
import random
import string
import time
import uuid
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64

from . import *
from . import configs

logger = logging.getLogger('libhoyolab.base')


def randomStr(n) -> str:
    """
    生成指定位数的随机字符串
    :param n: 指定位数
    :return:
    """
    return (''.join(random.sample(string.digits + string.ascii_letters, n))).lower()


def DS1(salt='lk2') -> str:
    """
    生成米游社DS1
    :return:
    """
    n = Salt_LK2 if salt.lower() == 'lk2' else Salt_K2
    i = str(int(time.time()))
    r = randomStr(6)
    c = md5(f"salt={n}&t={i}&r={r}")
    return "{},{},{}".format(i, r, c)


def DS2(query='', body='', salt='4x') -> str:
    """
    生成米游社DS2
    :param query: 查询参数（当算法为Ds2，请求为get时使用）
    :param body: post内容（当算法为Ds2，请求为post时使用）
    :param salt: 指定算法所需的salt（当算法为Ds2时使用）
    :return: str
    """
    if salt.lower() == '4x':
        salt = Salt_4X
    elif salt.lower() == '6x':
        salt = Salt_6X
    elif salt.lower() == 'prod':
        salt = Salt_PROD
    t = int(time.time())
    r = random.randint(100001, 200000)
    if body != '':
        if type(body) is str:
            body = json.loads(body)
        body = json.dumps(body, sort_keys=True)
    if query != '':
        query = '&'.join(sorted(query.split('&')))
    main = f"salt={salt}&t={t}&r={r}&b={body}&q={query}"
    ds = md5(main)
    return f"{t},{r},{ds}"


def headerGenerate(app='web', client='4', withCookie=True, withDs=True, withFp=True, agro=1, query='', body: str | dict = '',
                   salt_agro1='lk2', salt_agro2='4x', Referer="https://www.miyoushe.com/", stoken_ver=1,
                   ltoken_ver=1) -> dict:
    """
    生成请求头
    :param withFp: 是否包含Fp信息
    :param app: ‘app’ 或 ‘web’（已弃用）
    :param client: 1：iOS 2：Android 4：网页 5：其他
    :param withCookie: 是否携带cookie信息
    :param withDs: 是否包含Ds（已弃用）
    :param agro: Ds算法（Ds1 -> 1 或 Ds2 -> 2）
    :param query: 查询参数（当算法为Ds2，请求为get时使用）
    :param body: post内容（当算法为Ds2，请求为post时使用）
    :param salt_agro1: 指定算法为Ds1的salt
    :param salt_agro2: 指定算法为Ds2的salt
    :param Referer: 请求头的Referer字段
    :param ltoken_ver: ltoken等级
    :param stoken_ver: stoken等级
    :return: dict
    """
    account = configs.readAccount(str, stoken_ver=stoken_ver, ltoken_ver=ltoken_ver)
    headers = {
        "Cookie": account if withCookie else '',
        'User-Agent': "okhttp/4.8.0" if client == '2' else f'Mozilla/5.0 (Linux; Android 12; vivo-s7 Build/RKQ1.211119.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.79 Mobile Safari/537.36 miHoYoBBS/{mysVersion}',
        "Dnt": "1",
        "DS": DS1(salt_agro1) if agro == 1 else DS2(query, body, salt_agro2),
        "x-rpc-client_type": client,
        "x-rpc-app_version": mysVersion,
        "X-Requested-With": "com.mihoyo.hyperion",
        "x-rpc-device_id": str(uuid.uuid3(uuid.NAMESPACE_URL, account)),
        'Origin': 'https://webstatic.mihoyo.com',
        "x-rpc-device_name": "vivo s7",
        "x-rpc-device_model": "vivo-s7",
        "x-rpc-sys_version": "12",
        "x-rpc-channel": "miyousheluodi",
        "x-rpc-verify_key": "bll8iq97cem8",
        "Referer": Referer,
    }
    if withFp:
        headers['x-rpc-device_id'] = (''.join(random.sample(string.digits + string.ascii_letters, 16))).lower()
        body = {
            "device_id": headers['x-rpc-device_id'],
            "seed_id": (''.join(random.sample(string.digits + string.ascii_letters, 16))).lower(),
            "seed_time": str(int(time.time() * 1000)),
            "platform": "2",
            "device_fp": (''.join(random.sample(string.digits, 10))).lower(),
            "app_name": "bbs_cn",
            "ext_fields": '{"productName":"mmm", "board": "fghjm", "ramCapacity": "114514", "deviceInfo": "eftyh", "hardware": "ertyh", "display": "ertyh", "buildTime": "16918185684", "hostname": "gdhntyrn", "brand": "hetyhertyhomo"}'
        }
        r = session.post('https://public-data-api.mihoyo.com/device-fp/api/getFp', json=body)
        headers['x-rpc-device_fp'] = r.json()['data']['device_fp']
    return headers


def encrypt(message):
    """校验RSA加密 使用公钥进行加密"""
    cipher = Cipher_pkcs1_v1_5.new(RSA.importKey(public_key))
    cipher_text = base64.b64encode(cipher.encrypt(message.encode())).decode()
    return cipher_text


def connectApi(apiUrl: str, method='get', data=None, headers=None) -> requests.Response:
    """
    api连接
    :param apiUrl: url地址
    :param method: 连接方式（get 或 post）
    :param data: post内容
    :param headers: 请求头
    :return:
    """
    if headers is None:
        headers = headerGenerate(app='web')
    if data is None:
        data = {}
    count = 5
    err = None
    resp = None
    while count != 0:
        try:
            if method.lower() == 'get':
                resp = session.get(url=apiUrl, headers=headers, verify=False, timeout=5)
            elif method.lower() == 'post':
                resp = session.post(url=apiUrl, headers=headers, json=data, verify=False, timeout=5)
            else:
                raise Exception('method not matched!')

            break
        except Exception as e:
            err = e
            count -= 1
            continue
    if count == 0:
        raise Exception(f'Connection Failed! {err}')
    return resp


def connectionTest():
    """
    测试连接到米游社是否正常
    :return: 访问状态
    """
    try:
        resp = session.get('https://www.miyoushe.com')
        return resp.ok
    except requests.exceptions.ConnectionError:
        return False
