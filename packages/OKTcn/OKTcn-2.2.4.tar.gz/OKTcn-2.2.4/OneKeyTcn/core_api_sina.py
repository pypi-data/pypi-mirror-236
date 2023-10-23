import requests, json, re, time
import NorrisUtils.BuildConfig
import NorrisUtils.RawUtils
import base64
import codecs

API = 'https://www.sina.lt/api.php?from=w&site=dwz.win&url='
url = 'http://www.baidu.com'
cookie_str = 'PHPSESSID=2kmlmd6ps4ktmcect1a66gmish; Hm_lvt_fd97a926d52ef868e2d6a33de0a25470=1694765176; Hm_lpvt_fd97a926d52ef868e2d6a33de0a25470=1694766463; __tins__19242943=%7B%22sid%22%3A%201694765175667%2C%20%22vd%22%3A%205%2C%20%22expires%22%3A%201694768263235%7D; __51cke__=; __51laig__=5'
CookieDict = NorrisUtils.RawUtils.extractRawDict({}, cookie_str, splitBy=';')


def base64encode_utf16to8(url):
    '''
    请帮我用python 实现 js的内置方法 base64encode(utf16to8(url))
    要使用Python实现JavaScript中的内置方法base64encode(utf16to8(url))，您可以使用Python的base64和codecs模块来完成。
    首先，您需要将URL从UTF-16编码转换为UTF-8编码。然后，使用base64模块的b64encode函数对UTF-8编码的URL进行Base64编码。
    以下是使用Python实现的代码示例：
    :param url:
    :return:
    '''
    utf8_url = codecs.encode(url, 'utf-8')
    base64_url = base64.b64encode(utf8_url).decode('utf-8')
    return base64_url


class APISina(object):
    """
    sina api
    https://www.sina.lt/index.html
    """
    API = 'https://www.sina.lt/api.php?from=w&site=dwz.win&url='
    cookie_str = 'PHPSESSID=2kmlmd6ps4ktmcect1a66gmish; Hm_lvt_fd97a926d52ef868e2d6a33de0a25470=1694765176; Hm_lpvt_fd97a926d52ef868e2d6a33de0a25470=1694766463; __tins__19242943=%7B%22sid%22%3A%201694765175667%2C%20%22vd%22%3A%205%2C%20%22expires%22%3A%201694768263235%7D; __51cke__=; __51laig__=5'

    def __init__(self):
        pass

    def set_cookie_str(self, str):
        """
        外部设置更新cookie
        :param str:
        :return:
        """
        self.cookie_str = str

    def parse_result(self, req):
        '''
        解析结果
        :param req:
        {"result": "ok", "data": {"short_url": "https://dwz.win/a6gT", "title": "..", "expired_at": None, "black": 0}}
        {"result":"error","data":"\u9875\u9762\u5df2\u8fc7\u671f\uff0c\u8bf7\u5237\u65b0\u540e\u518d\u8bd5."}
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

    def one_key_shorten(self, url, logfunc=None):
        """
        一键变短链
        :param url:
        :param logfunc:
        :return:
        """
        cookie_dict = NorrisUtils.RawUtils.extractRawDict({}, cookie_str, splitBy=';')
        req = requests.get(API + base64encode_utf16to8(url), allow_redirects=False, cookies=cookie_dict, verify=False)
        if logfunc != None:
            logfunc(req)
            logfunc(req.text)
        result = self.parse_result(req)
        if logfunc != None:
            logfunc(result)
        if result.__contains__("失败"):
            return url
        return result


# # 示例用法
# url = 'https://h5.m.jd.com/rn/42yjy8na6pFsq1cx9MJQ5aTgu3kX/index.html?has_native=0'
# (APISina().one_key_shorten(url, logfunc=print))
