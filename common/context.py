import re
from common.read_config import ReadConfig

config = ReadConfig()
class Context:  # 上下文类，数据的准备和记录
    admin_user = config.get_value('data', 'admin_user')
    admin_pwd = config.get_value('data', 'admin_pwd')
    loan_user_id = config.get_value('data', 'loan_user_id')
    normal_user = config.get_value('data', 'normal_user')
    normal_pwd = config.get_value('data', 'normal_pwd')
    normal_user_id = config.get_value('data', 'normal_user_id')
    # 这些都要提前去数据库查询再写入配置文件，loan_id是在加标的那个用例运行完后给这个context类加一个属性

def replace(s):
    p = "\$\{(.*?)}"     # \\是为了能识别到$符号  （）代表一个组    ？匹配一次
    while re.search(p,s):  # 找到的时候
        m = re.search(p,s)    # 查找，s中查找p,找到一个就返回一个对象
        key = m.group(1)    # 取第一个组的字符串
        if hasattr(Context, key):  # 判断是否有这个属性
            value = getattr(Context, key)
            s = re.sub(p, value, s, count = 1)   # count =1 是替换一次  sub是查找并且替换 在s中找p表达式，最后用value去替换s中的p
        else:
            return  None  # 告知没有这个属性
    return  s
# serach 任意位置开始查找，找到一个就返回match对象，所以每次找只有一个，用这个是为了用group去找data的key,最后在sub中用作替换
# sub 默认查找全部，返回的是一个列表，找到所有满足的组里面的内容返回一个列表，count=0是替换全部，count =1 是替换一次
# 这两个是re模块的两个函数，查找替换的方式不一样，用在这里两个的功能也不一样

if __name__ == '__main__':
    s = '{"mobilephone":"${admin_user}","pwd":"${admin_pwd}"}'  # 字符串
    s = replace(s)
    print(type(s), s)