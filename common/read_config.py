from  configparser import ConfigParser
from  common import contants

class  ReadConfig:
    ''' 读配置文件的类 '''
    def __init__(self):
        self.config = ConfigParser()
        self.config.read(contants.global_dir, encoding = 'utf-8')   # 加载开关配置文件    # 有中文要加utf-8
        try:
            open = self.config.getboolean('switch', 'open')
            if open:   #如果是True
                self.config.read(contants.conf_file1_dir, encoding='utf-8')   # 加载配置文件1
            else:
                self.config.read(contants.conf_file2_dir, encoding='utf-8')   # 加载配置文件2
        except Exception as e:
            print("switch的值必须是布尔值，请修改",e)
            raise e

    def get_value(self, section, option):  # 字符串
        return self.config.get(section, option)

    def get_int(self, section, option):   # 整型
        return self.config.getint(section, option)

    def get_float(self, section, option):   # 浮点型
        return self.config.getfloat(section, option)

    def get_boolean(self, section, option):   # 布尔值
        return self.config.getboolean(section, option)


if  __name__ == '__main__':
   read_config =  ReadConfig()  # 这个对象只能调用ReadConfig里面的方法

   res= read_config.get_value('url','path_url')
   print(type(res), res)

   # ress = read_config.config.get('url','path_url')  # 如果不封装下面的方法就需要这样去调用
   #  #    read_config对象没有get方法，read_config只能去获取ReadConfig的config方法才有get这个方法
   # print(type(ress), ress)





