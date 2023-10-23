import requests, json, re, time
import NorrisUtils.BuildConfig
import NorrisUtils.RawUtils
import base64
import codecs

API = 'https://api.xiaomark.com/v1/link/create'
headers = {"Content-Type": "application/json"}


class APIXiaoMark(object):
    """
    目前只对接京东域名
    XiaoMark api
    https://xiaomark.com/book/open-api/add.html#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0%E8%AF%B4%E6%98%8E
    """

    def __init__(self):
        pass

    def dispatch_event(self, url):
        """
        分发事件
        :param url:
        :return:  是否由本类完成分发
        """
        return False
        if url is None or url == '' or not isinstance(url, str):
            return False
        return self.on_intercept_event(url)

    def on_intercept_event(self, url):
        """
        是否拦截事件
        :param url:
        :return:
        """
        if url is None or url == '' or not isinstance(url, str):
            return False
        if url.__contains__("pro.m.jd.com") or url.__contains__("item.m.jd.com") or url.__contains__("jd.com"):
            return True
        return False

    def on_event(self, url):
        last_tcn = self.dump_last_tcn(url)
        if last_tcn != '':
            return last_tcn
        return self.one_key_shorten(url)

    def dump_last_tcn(self, url, logfunc=print):
        """
        检查有无历史短链，有则直接使用
        https://xiaomark.com/book/open-api/group-link.html#%E8%AF%B7%E6%B1%82
        :param url:
        :param logfunc:
        :return:
        """
        try:
            data = {
                "apikey": "d510a8737f4ab3b5776b3142cdb4c74f",
                "group_sid": "963ii90v",
                "offset": 0,
                "limit": 100
            }
            req = requests.post('https://api.xiaomark.com/v1/link/get', data=json.dumps(data), headers=headers, allow_redirects=False, verify=False)
            logfunc(req.text)
            result = json.loads(req.text)
            for item in result['data']['links']:
                if url == item['origin_url']:
                    return item['url']
            return ''
        except:
            return ''

    def one_key_shorten(self, url, logfunc=print):
        """
        一键变短链   目前只对接京东域名
        :param url:
        :param logfunc:
        :return:
        """
        data = {
            "apikey": "d510a8737f4ab3b5776b3142cdb4c74f",
            "group_sid": "963ii90v",
            "origin_url": url
        }
        req = requests.post(API, data=json.dumps(data), headers=headers, allow_redirects=False, verify=False)
        logfunc(req)
        logfunc(req.text)
        result = self.parse_result(req)
        if result.__contains__("失败"):
            return url
        return result

    def parse_result(self, req, logfunc=print):
        '''
        解析结果
        :param req:
        {"code":0,"data":{"group":{"name":"jd","sid":"963ii90v"},"link":{"name":"\u77ed\u94fe\u63a5KDaabr","origin_url":"https://pro.m.jd.com/mall/active/3AWQD5ttD6aUg8nue6D7CryKptzW/index.html?cu=true&rid=10304&hideyl=1&utm_source=kong&utm_medium=jingfen&utm_campaign=t_1000761320_&utm_term=347d122d61b04c8e906037d0ec37a27a","url":"https://sourl.cn/KDaabr"},"n_links_today":3},"message":"\u8bf7\u6c42\u6210\u529f"}
        :return:
        '''
        try:
            parsed_data = json.loads(req.text)
            short_url = parsed_data['data']['link']['url']
            logfunc(short_url)
            return short_url
        except:
            pass
        return '提取失败:' + req.text

# # 示例用法
# url = 'https://pro.m.jd.com/mall/active/3AWQD5ttD6aUg8nue6D7CryKptzW/index.html?cu=true&rid=10304&hideyl=1&utm_source=kong&utm_medium=jingfen&utm_campaign=t_1000761320_&utm_term=347d122d61b04c8e906037d0ec37a27a'
# (APIXiaoMark().one_key_shorten(url))
