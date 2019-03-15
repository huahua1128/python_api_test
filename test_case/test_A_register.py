import unittest
import json
from libext.ddt import ddt, data
from common.do_excel import DoExcel
from common.request import Request
from common import contants
from common.read_config import ReadConfig
from common.connect_mysql import MysqlUtil
from common.logger import get_logger


do_excel = DoExcel(contants.case_dir, 'register')
cases = do_excel.get_data()
readconfig = ReadConfig()
path_url = readconfig.get_value('url', 'path_url')  # 这些放到类里面也可以，用self调用
logger = get_logger('register')


@ddt
class TestRegister(unittest.TestCase):  # 继承TestCase类

    @classmethod
    def setUpClass(cls):
        cls.mysql = MysqlUtil(return_dict = True)
        cls.request = Request()  # 实例化对象 Request() 实例化为了传递cookies,Request初始化的时候有session的对象

    def setUp(self):
        sql = "select max(mobilephone)  as max_phone  from future.member"
        self.max = self.mysql.fetch_one(sql)['max_phone']  # 元组索引取值  #把max  global一下，下面可以直接用max,不用self调用

    @data(*cases)
    def test_register(self, case):
        logger.info("开始执行{0}模块的第{1}条用例：{2}".format(case.module, case.case_id, case.title))
        data_dict = json.loads(case.data)
        if data_dict["mobilephone"] == "${register_mobile}":  # 要注意excel里面要有mobilephone
            data_dict["mobilephone"] = int(self.max) + 1
        case.expected = json.loads(case.expected)      # case.expected 转成字典
        resp = self.request.request(method=case.method, url=path_url + case.url, data=data_dict)  # 要注意data = data_dict
        try:
            self.assertEqual(case.expected['code'], resp.json()['code'], 'register error')  # register error是提示
           # 成功且regname为空时做数据库校验
            if resp.json()['msg'] == '注册成功' and data_dict['regname'] == None:
                sql = 'select * from future.member where mobilephone={0}'.format(data_dict["mobilephone"])
                results = self.mysql.fetch_all(sql)
                self.assertEqual(1, len(results))  # 是否加入了一条数据
                self.assertEqual(0,results[0]['LeaveAmount'])  # 余额是否为0
                self.assertIsNone(results[0]['RegName'])   # regname是否是空
            elif resp.json()['msg'] == '注册成功' and data_dict['regname'] != None:   # 成功且regname不为空时做数据库校验
                sql = 'select * from future.member where mobilephone={0}'.format(data_dict["mobilephone"])
                results = self.mysql.fetch_all(sql)
                self.assertEqual(1, len(results))  # 是否加入了一条数据
                self.assertEqual(0, results[0]['LeaveAmount'])  # 余额是否为0
                self.assertIsNotNone(results[0]['RegName'])  # regname是否是空
            elif resp.json()['msg'] == '"手机号码已被注册':  # 判断已经被注册的
                sql = 'select * from future.member where mobilephone={0}'.format(data_dict["mobilephone"])
                results = self.mysql.fetch_all(sql)
                self.assertEqual(1, len(results))   # 查出一条数据
            do_excel.write_back(case.case_id + 1, resp.text, 'PASS')
            logger.info("第{}条测试用例执行的结果是：PASS".format(case.case_id))
        except AssertionError as e:
            do_excel.write_back(case.case_id + 1, resp.text, 'FAIL')
            logger.info("第{}条测试用例执行的结果是：FAIL".format(case.case_id))
            logger.error("执行失败！期望结果是：{0}，实际结果是：{1}".format(case.expected, resp.json()))
            raise e

    def tearDown(self):
        logger.info('用例执行完毕')
        logger.info("******************************************************")

    @classmethod
    def tearDownClass(cls):
        cls.mysql.close()
        cls.request.session.close()  # 关闭会话


if __name__ == '__main__':
    unittest.main()
