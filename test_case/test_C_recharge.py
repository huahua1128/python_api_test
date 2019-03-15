import unittest
import json
from libext.ddt import ddt,data
from common.do_excel import DoExcel
from common.request import Request
from common import contants
from common.read_config import ReadConfig
from common.logger import get_logger
from common import context
from common.connect_mysql import MysqlUtil
import math

# 第一种方法。将excel里面的第一条用例设计成正常登陆，session保持会话的方式来请求的话， 需要将request的实例化的对象放在类里面，获取excel数据运行用例。

# do_excel = DoExcel(contants.case_dir, 'recharge')
# cases = do_excel.get_data()
# path_url = ReadConfig(contants.conf_file_dir).get_value('URL', 'path_url')  # 这些放到类里面也可以，用self调用
# request = Request()     # 这部分代码也可以放在类里面，类属性，调用的时候在当类属性调用

@ddt
class TestRecharge(unittest.TestCase):  # 继承TestCase类
    do_excel = DoExcel(contants.case_dir, 'recharge')
    cases = do_excel.get_data()
    readconfig = ReadConfig()
    path_url = readconfig.get_value('url', 'path_url')  # 这些放到类里面也可以，用self调用
    logger = get_logger('recharge')
    # 以上都是类属性   request = Request() 实例化为了传递cookies,Request初始化的时候有session的对象

    @classmethod
    def setUpClass(cls):  # TestRecharge类执行前执行一次   类方法
        cls.request = Request()    # 实例化对象 Request() 实例化为了传递cookies,Request初始化的时候有session的对象
        cls.mysql = MysqlUtil()

    def setUp(self):  # 每个用例执行前执行一次
        pass

    @data(*cases)
    def test_recharge(self, case):
        self.logger.info("开始执行{0}模块的第{1}条用例：{2}".format(case.module, case.case_id, case.title))
        # 查找参数化的测试数据，动态的替换
        data_new = context.replace(case.data)
        data_new = json.loads(data_new)  # 数据变成字典
        if data_new['mobilephone']:  # 判断手机号不为空
            if self.mysql.fetch_one('select * from future.member where mobilephone={0}'.format(data_new['mobilephone'])):#数据库存在的手机号
                sql = "select LeaveAmount  from future.member where mobilephone={0}" \
                    " order by RegTime desc limit 1".format(data_new['mobilephone'])
                LeaveAmount_1 = self.mysql.fetch_one(sql)[0]   # 执行前查询余额
        resp = self.request.request(method = case.method, url= self.path_url+case.url, data = data_new)  #request.path_url都是类属性
        self.logger.info(resp.json())
        case.expected = json.loads(case.expected)
        try:
            self.assertEqual(case.expected['code'], resp.json()['code'], 'recharge error')  # recharge error是提示
            if resp.json()['msg'] == '充值成功':  # 充值成功时判断
                sql = "select LeaveAmount  from future.member where mobilephone={0} " \
                      "order by RegTime desc limit 1".format(data_new['mobilephone'])
                LeaveAmount_2 = self.mysql.fetch_one(sql)[0]   # 充值后的余额
                self.assertEqual(math.ceil(LeaveAmount_2), math.ceil(float(LeaveAmount_1) + float(data_new['amount'])))
                # 向上取整判断充值前后金额是否相等，用到了math模块  math.ceil
            self.do_excel.write_back(case.case_id + 1, resp.text, 'PASS')
            self.logger.info("第{}条测试用例执行的结果是：PASS".format(case.case_id))
        except AssertionError as e:
            self.do_excel.write_back(case.case_id + 1, resp.text, 'FAIL')
            self.logger.info("第{}条测试用例执行的结果是：FAIL".format(case.case_id))
            self.logger.error("执行失败！期望结果是：{0}，实际结果是：{1}".format(case.expected, resp.json()))
            raise e

    def tearDown(self):
        self.logger.info('用例执行完毕')
        self.logger.info("******************************************************")

    @classmethod   # TestRecharge类执行完毕后执行一次
    def tearDownClass(cls):
        cls.request.session.close()   # 关闭会话


# (未完成)
# 若不将excel中的第一条设计为登陆用例，也可以在setUpClass(cls)类方法中去先登陆，然后再执行充值用例。

if __name__ == '__main__':
    unittest.main()