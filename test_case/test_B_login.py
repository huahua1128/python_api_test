import unittest
from libext.ddt import ddt,data
from common.do_excel import DoExcel
from common.request import Request
from common import contants
from common.read_config import ReadConfig
from common.logger import get_logger
from common.connect_mysql import MysqlUtil
import json
from  common import context

do_excel = DoExcel(contants.case_dir,'login')
cases = do_excel.get_data()
readconfig = ReadConfig()
path_url = readconfig.get_value('url', 'path_url')   #这些放到类里面也可以，用self调用
logger = get_logger('login')

@ddt
class TestLogin(unittest.TestCase):  # 继承TestCase类

    @classmethod
    def setUpClass(cls):  # TestRecharge类执行前执行一次   类方法
        cls.request = Request()  # 实例化对象 Request() 实例化为了传递cookies,Request初始化的时候有session的对象
        cls.mysql = MysqlUtil()  # 实例化一个对象

    def setUp(self):
        pass

    @data(*cases)
    def test_login(self, case):
        logger.info("开始执行{0}模块的第{1}条用例：{2}".format(case.module, case.case_id, case.title))
        # 查找参数化的测试数据，动态的替换
        data_new = context.replace(case.data)
        # logger.info(data_new)
        resp = self.request.request(method=case.method, url=path_url + case.url,data=data_new)
        # logger.info(resp.text)
        case.expected = json.loads(case.expected)
        try:
            self.assertEqual(case.expected['code'], resp.json()['code'], 'login error')  # login error是提示
            do_excel.write_back(case.case_id + 1, resp.text, 'PASS')
            logger.info("第{}条测试用例执行的结果是：PASS".format(case.case_id))
        except AssertionError as e:
            do_excel.write_back(case.case_id + 1, resp.text, 'FAIL')
            logger.info("第{}条测试用例执行的结果是：FAIL".format(case.case_id))
            logger.error("执行失败！期望结果是：{0}，实际结果是：{1}".format(case.expected, resp.text))
            raise e


    def tearDown(self):
        logger.info('用例执行完毕')
        logger.info("******************************************************")

    @classmethod  # TestAdd类执行完毕后执行一次
    def tearDownClass(cls):
        cls.request.session.close()  # 关闭会话
        cls.mysql.close()  # 关闭mysql


if __name__ == '__main__':
    unittest.main()



