import requests
import json
from common.logger import get_logger

logger = get_logger('request')

class Request:

    def __init__(self):
        self.session = requests.sessions.session()   # 实例化一个session对象

    def request(self, method, url, data = None, cookies = None):
        if data is not None and type(data) == str:
            data = json.loads(data)   # 如果是字符串 就转成字典
        try:
            if method.upper() == 'GET':
                return self.session.request(method, url = url, params = data, cookies = cookies)
            elif method.upper() == 'POST':
                return self.session.request(method, url=url, data=data, cookies=cookies)
            else:
                logger.warning("不支持该请求方式")
        except Exception as e:
            logger.error('执行请求报错',e)


if __name__ == '__main__':
    request = Request()  # 实例化一个对象
    url = 'http://47.107.168.87:8080/futureloan/mvc/api/member/login'
    data = {"mobilephone":"13539787043","pwd":"huahua123456"}
    rep = request.request('ttt', url, data = data)
    print(rep.text)


