import logging  # 所以不能以logging为文件名（自己的文件命名不能和引入的模块名冲突）
import logging.handlers
from common.read_config import ReadConfig
from common import contants

read_config = ReadConfig()
in_level = read_config.get_value('log', 'in_level')
out_level = read_config.get_value('log', 'out_level')
file_level = read_config.get_value('log', 'file_level')
formate = read_config.get_value('log', 'formatter')
file_path = contants.log_dir

def get_logger(logger_name):
    # 收集器 -----创建一个日志收集器  log名字是同一个的时候就是同一个对象
    logger = logging.getLogger(logger_name)  # getLogger 是个函数，必须传一个参数，作为自己的日志收集器的名字，否则还是会用root logger
    logger.setLevel(in_level)  # 给日志收集器设置level   (相当于第一次过滤)  设置了日志收集器的level,上面加不加名字都可以。但是一般还是要加上名字

    # # 输出格式   Formatter 是个类  规定日志输出的格式
    formatter = logging.Formatter(formate)

    # # 输出渠道 -----输出到指定文件  文件路径 绝对路径和相对路径都可以
    file_handler = logging.handlers.RotatingFileHandler(file_path, encoding='utf-8',  maxBytes=20 * 1024 * 1024,
                                                        backupCount=10)
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)

    # 输出渠道
    console_handler = logging.StreamHandler()  # 创建一个输出到控制台的渠道
    console_handler.setLevel(out_level)  # 给自己设置的渠道设置level  (相当于第二次过滤)
    console_handler.setFormatter(formatter)

    # # 对接  日志收集器和输出渠道进行对接
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return  logger


if __name__ == '__main__':
    logger = get_logger(logger_name='invest')
    logger.error('this is error')
    logger.info('this is info')
    logger.debug('this is debug')
    logger.warning('this is warning')
