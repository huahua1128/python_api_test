import unittest
# import HTMLTestRunnerNew    # 将这个模块放在python中
from libext import HTMLTestRunnerNew
from common import contants

# suite = unittest.TestSuite()
# loader = unittest.TestLoader()

# suite.addTest(loader.loadTestsFromTestCase(TestLogin))
# suite.addTest(loader.loadTestsFromTestCase(TestRegister))
# suite.addTest(loader.loadTestsFromTestCase(TestRecharge))

# 全部用例运行
discover = unittest.defaultTestLoader.discover(contants.test_case_dir, pattern = 'test_*.py')

with open(contants.report_dir, 'wb') as file:
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file, verbosity=2,title="接口测试报告",
                                              description='关于前程贷的接口测试报告',tester="花花")
    runner.run(discover)