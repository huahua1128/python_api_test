import unittest
from libext.ddt import ddt,data
from common.do_excel import DoExcel
from common.request import Request
from common import contants
from common.read_config import ReadConfig
from common.logger import get_logger
import json
from  common import context

do_excel = DoExcel(contants.case_dir,'list')
cases = do_excel.get_data()
readconfig = ReadConfig()
path_url = readconfig.get_value('url', 'path_url')   #这些放到类里面也可以，用self调用
logger = get_logger('list')

@ddt
class TestList(unittest.TestCase):  # 继承TestCase类

    @classmethod
    def setUpClass(cls):  # TestRecharge类执行前执行一次   类方法
        cls.request = Request()  # 实例化对象 Request() 实例化为了传递cookies,Request初始化的时候有session的对象

    def setUp(self):
        pass

    @data(*cases)
    def test_list(self, case):
        logger.info("开始执行{0}模块的第{1}条用例：{2}".format(case.module, case.case_id, case.title))
        # 从用例里面取出来参数化部分进行替换
        data_new = context.replace(case.data)
        resp = self.request.request(method = case.method, url= path_url+case.url, data = data_new)  # 要传新的数据
        case.expected = json.loads(case.expected)
        try:
            self.assertEqual(case.expected['code'], resp.json()['code'], 'list error')  # list error是提示
            # logger.info(resp.json())
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

    @classmethod  # TestRecharge类执行完毕后执行一次
    def tearDownClass(cls):
        cls.request.session.close()  # 关闭会话


if __name__ == '__main__':
    unittest.main()

