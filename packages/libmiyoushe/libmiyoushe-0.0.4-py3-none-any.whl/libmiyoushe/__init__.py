import hashlib
import json
import os
import pathlib
import warnings

import requests

requests.packages.urllib3.disable_warnings()

session = requests.session()

lib_version = '0.0.4'
lib_name = 'libmiyoushe'
lib_desc = "A module for miyoushe(米游社), include mihoyo account authentication, some actions for miyoushe(米游社), etc."
home_dir = str(pathlib.Path.home())
run_dir = os.path.join(home_dir, '.libhoyolab')
config_dir = os.path.join(run_dir, 'configs')
account_file = os.path.join(config_dir, 'account.json')
current_user_file = os.path.join(run_dir, 'current_user')

public_key = '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDDvekdPMHN3AYhm/vktJT+YJr7\ncI5DcsNKqdsx5DZX0gDuWFuIjzdwButrIYPNmRJ1G8ybDIF7oDW2eEpm5sMbL9zs\n9ExXCdvqrn51qELbqj0XxtMTIpaCHFSI50PfPpTFV9Xt/hmyVwokoOXFlAEgCn+Q\nCgGs52bFoYMtyi+xEQIDAQAB\n-----END PUBLIC KEY-----'
Salt_K2 = 'F6tsiCZEIcL9Mor64OXVJEKRRQ6BpOZa'
Salt_LK2 = 'xc1lzZFOBGU0lz8ZkPgcrWZArZzEVMbA'
Salt_4X = 'xV8v4Qu54lUKrEYFZkJhB8cuOh9Asafs'
Salt_6X = 't0qEgfub6cvueAPgR5m9aQWWVciEer7v'
Salt_PROD = 'JwYDpKvLj6MrMqqYU6jTKF17KNO2PXoS'
mysVersion = '2.55.1'
mysClient_type = '2'

account_default = {'account': {}, 'account_hash': '99914b932bd37a50b983c5e7c90ae93b'}

newsType = {'announce': '1', 'activity': '2', 'information': '3'}
actions = {"article": "文章", "recommend": "推荐", "announce": "公告", "activity": "活动", "information": "资讯",
           "history": "历史", "search": "搜索", "setting": "设置", "user": "用户", "error": "错误", "login": "登录"}

if not os.path.exists(run_dir):
    os.mkdir(run_dir)

if not os.path.exists(config_dir):
    os.mkdir(config_dir)

try:
    with open(current_user_file, 'r') as f:
        _current_user = f.read()
except:
    _current_user = '-1'
    with open(current_user_file, 'w') as f:
        f.write(_current_user)


def md5(text) -> str:
    """
    md5加密
    :param text: 需要加密的文本
    :return:
    """
    md5_obj = hashlib.md5()
    md5_obj.update(text.encode())
    return md5_obj.hexdigest()


try:
    with open(account_file) as f:
        account_set = json.load(f)
    if account_set['account_hash'] != md5(json.dumps(account_set['account'])):
        warnings.warn('The saved account had been changed and not operate by this module, clearing...', Warning)
        account_set = account_default
        with open(account_file, 'w') as f:
            json.dump(account_set, f, indent=2, ensure_ascii=False)
except:
    account_set = account_default
    with open(account_file, 'w') as f:
        json.dump(account_set, f, indent=2, ensure_ascii=False)


def getExistUser():
    """
    获取当前已记录的账号
    :return:
    """
    try:
        with open(account_file) as f:
            account_set = json.load(f)
    except:
        account_set = account_default
        with open(account_file, 'w') as f:
            json.dump(account_set, f, indent=2, ensure_ascii=False)
    return list(account_set['account'].keys())


def get_current_user():
    """
    获取当前使用的账户uid（若未设置，则自动设置为已有记录的第一个；如读取到的uid不存在，则将uid重置为-1）
    :return:
    """
    global _current_user
    with open(current_user_file, 'r') as f:
        _current_user = f.read()
    exist_user = getExistUser()
    if _current_user in exist_user:
        return _current_user
    else:
        _current_user = '-1'
    if _current_user == '-1' and len(exist_user) > 0:
        _current_user = exist_user[0]
        with open(current_user_file, 'w') as f:
            f.write(_current_user)
    return _current_user


def set_current_user(uid='-1'):
    """
    设置并返回当前使用的账户uid（若uid不在已有记录中，则自动设置为已有记录的第一个）
    :return:
    """
    global _current_user
    exist_user = getExistUser()
    if uid in exist_user:
        _current_user = uid
        with open(current_user_file, 'w') as f:
            f.write(uid)
    else:
        _current_user = '-1'
    if _current_user == '-1' and len(exist_user) > 0:
        _current_user = exist_user[0]
        with open(current_user_file, 'w') as f:
            f.write(_current_user)
    return _current_user
