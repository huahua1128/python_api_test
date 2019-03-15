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


@ddt
class TestAdd(unittest.TestCase):  # 继承TestCase类
    do_excel = DoExcel(contants.case_dir, 'add')
    cases = do_excel.get_data()
    readconfig = ReadConfig()
    path_url = readconfig.get_value('url', 'path_url')  # 这些放到类里面也可以，用self调用
    logger = get_logger('add')
    # 以上都是类属性   request = Request() 实例化为了传递cookies,Request初始化的时候有session的对象

    @classmethod
    def setUpClass(cls):  # TestRecharge类执行前执行一次   类方法
        cls.request = Request()    # 实例化对象 Request() 实例化为了传递cookies,Request初始化的时候有session的对象
        cls.mysql = MysqlUtil(return_dict = True)   # 实例化一个对象

    def setUp(self):  # 每个用例执行前执行一次
        pass

    @data(*cases)
    def test_add(self, case):
        self.logger.info("开始执行{0}模块的第{1}条用例：{2}".format(case.module, case.case_id, case.title))
        # 查找参数化的测试数据，动态的替换
        self.logger.info(case.data)
        data_new = context.replace(case.data)
        data_new = json.loads(data_new)
        self.logger.info(data_new)
        resp = self.request.request(method = case.method, url= self.path_url+case.url, data = data_new)  #request.path_url都是类属性
        self.logger.info(resp.text)
        case.expected = json.loads(case.expected)
        try:
            self.assertEqual(case.expected['code'], resp.json()['code'], 'add error')  # add error是提示
            # 加标成功时做数据校验
            if resp.json()['msg'] == '加标成功':
                sql = 'select * from future.loan where MemberID={0} ' \
                      'order by createTime desc limit 1'.format(data_new['memberId'])
                results = self.mysql.fetch_all(sql)
                self.assertEqual(results[0]['Title'], data_new['title'])
                self.assertEqual(results[0]['Amount'], data_new['amount'])
                self.assertEqual(results[0]['LoanRate'], float(data_new['loanRate']))
                self.assertEqual(results[0]['LoanTerm'], data_new['loanTerm'])
                self.assertEqual(results[0]['LoanDateType'], data_new['loanDateType'])
                self.assertEqual(results[0]['RepaymemtWay'], data_new['repaymemtWay'])
                # self.assertEqual(results[0]['BiddingDays'], data_new['biddingDays'])
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

    @classmethod   # TestAdd类执行完毕后执行一次
    def tearDownClass(cls):
        cls.request.session.close()   # 关闭会话
        cls.mysql.close()   # 关闭mysql

if __name__ == '__main__':
    unittest.main()
