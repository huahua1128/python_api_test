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
from common.context import Context

# 第一种方法。将excel里面的第一条用例设计成正常登陆，session保持会话的方式来请求的话， 需要将request的实例化的对象放在类里面，获取excel数据运行用例。

# do_excel = DoExcel(contants.case_dir, 'recharge')
# cases = do_excel.get_data()
# path_url = ReadConfig(contants.conf_file_dir).get_value('URL', 'path_url')  # 这些放到类里面也可以，用self调用
# request = Request()     # 这部分代码也可以放在类里面，类属性，调用的时候在当类属性调用

@ddt
class TestAudit(unittest.TestCase):  # 继承TestCase类
    do_excel = DoExcel(contants.case_dir, 'audit')
    cases = do_excel.get_data()
    readconfig = ReadConfig()
    path_url = readconfig.get_value('url', 'path_url')  # 这些放到类里面也可以，用self调用
    logger = get_logger('audit')
    # 以上都是类属性   request = Request() 实例化为了传递cookies,Request初始化的时候有session的对象

    @classmethod
    def setUpClass(cls):  # TestRecharge类执行前执行一次   类方法
        cls.request = Request()    # 实例化对象 Request() 实例化为了传递cookies,Request初始化的时候有session的对象
        cls.mysql = MysqlUtil()   # 实例化一个对象

    def setUp(self):  # 每个用例执行前执行一次
        pass

    @data(*cases)
    def test_audit(self, case):
        self.logger.info("开始执行{0}模块的第{1}条用例：{2}".format(case.module, case.case_id, case.title))
        # 查找参数化的测试数据，动态的替换
        data_new = context.replace(case.data)
        data_new = json.loads(data_new)
        self.logger.info(data_new)
        resp = self.request.request(method = case.method, url= self.path_url+case.url, data = data_new)  #request.path_url都是类属性
        self.logger.info(resp.text)
        case.expected = json.loads(case.expected)
        try:
            self.assertEqual(case.expected['code'], resp.json()['code'], 'audit error')  # audit error是提示
            #判断是否加标成功，加标成功就去数据库查询该用户创建的最新的标的
            if resp.json()['msg'] == '加标成功':
                loan_user_id = getattr(Context, 'loan_user_id')  # 相当于data_new['memberId']
                sql = "select id from future.loan where MemberId = {0} " \
                      "order by createTime desc limit 1".format(loan_user_id)
                global loan_id
                loan_id  = self.mysql.fetch_one(sql)[0]  # int型的数据
                setattr(Context, 'loan_id', str(loan_id))  # 后续的接口要通过正则替换。必须str
            # 更新状态成功就做数据校验
            if '更新状态成功' in resp.json()['msg']:
                sql = 'select Status from future.loan where Id={0} ' \
                      'order by createTime desc limit 1'.format(data_new['id'])
                result = self.mysql.fetch_one(sql)
                self.assertEqual(result[0], int(data_new['status']))
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

    @classmethod   # TestInvest类执行完毕后执行一次
    def tearDownClass(cls):
        cls.request.session.close()   # 关闭会话
        cls.mysql.close()   # 关闭mysql

if __name__ == '__main__':
    unittest.main()