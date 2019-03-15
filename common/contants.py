import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(os.path.abspath(__file__))

# base_dir = os.path.dirname(os.getcwd())   # 其他文件下运行的时候
# # base_dir = os.getcwd()   # run里面运行的时候的基础地址

print(base_dir)
datas_dir = os .path.join(base_dir,'datas')
case_dir = os.path.join(datas_dir,'cases.xlsx')
print('case_dir', case_dir)

conf_dir = os.path.join(base_dir,'conf')
global_dir = os.path.join(conf_dir,'global.conf')
conf_file1_dir = os.path.join(conf_dir,'conf_file_1.conf')
conf_file2_dir = os.path.join(conf_dir,'conf_file_2.conf')

logs_dir = os.path.join(base_dir,'logs')
log_dir = os.path.join(logs_dir,'case.log')
print(log_dir)

reports_dir = os.path.join(base_dir,'reports')
report_dir = os.path.join(reports_dir, 'report.html')
print(report_dir)

test_case_dir = os.path.join(base_dir,'test_case')
print(test_case_dir)
