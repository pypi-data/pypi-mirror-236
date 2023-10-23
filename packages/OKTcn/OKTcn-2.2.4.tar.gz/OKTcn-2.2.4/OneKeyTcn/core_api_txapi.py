import requests, json, re, time
import NorrisUtils.BuildConfig
import NorrisUtils.RawUtils
import base64
import codecs
import redis
import configparser
import datetime
import platform

config = configparser.ConfigParser()
try:
    config.read("config.ini")
except:
    pass
redis_db = None
try:
    redis_db = redis.Redis(host=config.get('redis', 'host'))
except:
    pass

config_key = 'path_m'
if platform.system().lower() == 'windows':
    config_key = 'path_w'
    print("Windows")
elif platform.system().lower() == 'linux':
    print("linux")
elif platform.system().lower() == 'darwin':
    config_key = 'path_m'
    print("Mac")
try:
    tokens_path = config.get('tokens_path', config_key)
    print(tokens_path)
    config.read(tokens_path)
except:
    pass

try:
    json_str = config.get("tokens", "json")
    tokens = json.loads(json_str)
except:
    tokens = {}
    pass
print(tokens)
# https://blog.csdn.net/weixin_47590344/article/details/129251757
# 积分不足 {'code': 4102, 'msg': '积分不足', 'data': None, 'time': 1694766032}
API_TCN = 'https://api.txapi.cn/v1/short_url/tcn'
API = 'https://api.txapi.cn/v1/short_url'
token_other = 'Z1QljZOZiT4NTG'


class APItxApi(object):
    """
    txapi
    http://txapi.cn/api_detail?id=1609184287570001920
    """
    _redis_db = redis_db
    _token = token_other

    def __init__(self):
        pass

    @property
    def redis_db(self):
        return self._redis_db

    @redis_db.setter
    def redis_db(self, value):
        self._redis_db = value

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    def is_token_none(self, token):
        return token is None

    def parse_result(self, req):
        '''
        解析结果
        :param req:
        {"code":200,"msg":"OK","data":{"long_url":"http://www.baidu.com","short_url":"http://t.cn/Rxmm0XL"},"time":1695020937}
        {'code': 4102, 'msg': '积分不足', 'data': None, 'time': 1694766032}
        :return:
        '''
        try:
            parsed_data = json.loads(req.text)
            short_url = parsed_data['data']['short_url']
            print(short_url)
            return short_url
        except:
            pass
        return '提取失败:' + req.text

    def one_key_shorten(self, url, logfunc=print):
        """
        一键变短链
        :param url:
        :param logfunc:
        :return:
        """
        if url is None or url == '':
            return ''
        if self.redis_db is not None and self.redis_db.get(url) is not None:
            return str(self.redis_db.get(url), encoding="utf-8")
        params = {
            'token': self.token,
            # 'token': tokens.get('176'),
            'url': url
        }
        req = requests.get(API, params=params, allow_redirects=False, verify=False)
        logfunc(req.url)
        logfunc(req.text)
        result = self.parse_result(req)
        logfunc(result)
        if result.__contains__("失败"):
            return url
        if self.redis_db is not None:
            self.redis_db.set(url, result, ex=60 * 60 * 3)
        return result

    def one_key_tcn(self, url, logfunc=print):
        """
        白嫖TCN
        采用token轮询大法
        :return:
        """
        if url is None or url == '':
            return ''
        if self.redis_db is not None and self.redis_db.get(url) is not None:
            return str(self.redis_db.get(url), encoding="utf-8")
        token = self.popup_token()
        if self.is_token_none(token):
            return self.one_key_shorten(url)
        params = {
            'token': token,
            'url': url
        }
        req = requests.get(API_TCN, params=params, allow_redirects=False, verify=False, timeout=(5, 10))
        logfunc(req.text)
        '''
        解析结果
        :param req:
        {"code":200,"msg":"OK","data":{"long_url":"http://www.baidu.com","short_url":"http://t.cn/Rxmm0XL"},"time":1695020937}
        {'code': 4102, 'msg': '积分不足', 'data': None, 'time': 1694766032}
        :return:
        '''
        try:
            parsed_data = json.loads(req.text)
            if parsed_data['code'] == 200:
                result = self.parse_result(req)
                logfunc(result)
                if result.__contains__("失败"):
                    return url
                if self.redis_db is not None:
                    self.redis_db.set(url, result, ex=60 * 60 * 24 * 3)
                return result

            # {'code': 4102, 'msg': '积分不足', 'data': None, 'time': 1694766032}
            # 积分不足，换token继续
            if parsed_data['code'] == 4102:
                expire_time = datetime.datetime.combine(datetime.date.today(), datetime.time(23, 59, 59))
                # 有redis 才能实现效果
                if self.redis_db is None:
                    return self.one_key_shorten(url)
                # 没有redis直接转走用普通专练
                else:
                    if token == token_other:
                        self.redis_db.set(token_other, token_other)
                        # 当晚过期
                        self.redis_db.expireat(token_other, expire_time)
                    else:
                        key = next((k for k, v in tokens.items() if v == token), None)
                        self.redis_db.set(token, key)
                        # 当晚过期
                        self.redis_db.expireat(token, expire_time)
                    return self.one_key_tcn(url)
            # 其他情况，返回原url
            else:
                return url
        except Exception as e:
            print(e)

    def threshold(self, url, token, redis_db=redis_db):
        pass

    def popup_token(self):
        if self.redis_db is None:
            return token_other
        if self.redis_db.get(token_other) == '' or self.redis_db.get(token_other) is None:
            return token_other
        for key, value in tokens.items():
            if self.redis_db.get(value) == '' or self.redis_db.get(value) is None:
                return value
        return None

# # 示例用法
# url = 'https://h5.m.jd.com/rn/42yjy8na6pFsq1cx9MJQ5aTgu3kX/index.html?'
# api = APItxApi()
# print(api.one_key_tcn(url, logfunc=print))
#
# print(api.popup_token())
