import sys,os
from loguru import logger

# 获取当前项目的绝对路径
# 第一次dirname当前文件路径，第二次得到上一层路径
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(root_dir,'logs') # 存放项目日志目录的绝对路径

if not os.path.exists(log_dir):
    os.mkdir(log_dir)

LOG_FILE = 'translation.log'        # 存储日志的文件

class MyLogger:
    def __init__(self):
        log_file_path = os.path.join(log_dir, LOG_FILE)
        self.logger = logger  # 写日志的对象
        # 清空所有设置
        self.logger.remove()
        # 添加控制台输出的格式,sys.stdout为输出到屏幕;关于这些配置还需要自定义请移步官网查看相关参数说明

        # level = 'DEBUG' 这个表示能输出的最低日志级别
        # 日志级别排序： TRACE < DEBUG < INFO < SUCCESS < WARNING < ERROR  < Critical
        self.logger.add(sys.stdout, level='DEBUG',
                        format="<green>{time:YYYYMMDD HH:mm:ss}</green> | "  # 颜色>时间
                               "{process.name} | "  # 进程名
                               "{thread.name} | "  # 线程名
                               "<cyan>{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
                               ":<cyan>{line}</cyan> | "  # 行号
                               "<level>{level}</level>: "  # 等级
                               "<level>{message}</level>",  # 日志内容
                        )
        # 输出到文件的格式,注释下面的add',则关闭日志写入
        self.logger.add(log_file_path, level='DEBUG', encoding='UTF-8', # level='DEBUG'这个表示能输出的最低日志级别  TRACE <  DEBUG < INFO < WARN < ERROR
                        format='{time:YYYYMMDD HH:mm:ss} - '  # 时间
                               "{process.name} | "  # 进程名
                               "{thread.name} | "  # 进程名
                               '{module}.{function}:{line} - {level} -{message}',  # 模块名.方法名:行号
                        rotation="10 MB",  # 日志文件新生成的规则  rotation="1 week" 一周生成一次新的文件  rotation="1 days" 每隔一天生成新的日志文件
                        retention=20  # 保留日志文件的规则 保留最近的20个文件 retention='1 month' 保留一个月的日志文件
                        )

    def get_logger(self):
        return self.logger

log = MyLogger().get_logger()

if __name__ == '__main__':


    # print('str.pdf'['str.pdf'.rindex('.'):])

    # log.debug("this is a debug message")
    # log.info("this is an info message")
    # log.warning("this is a warining message")
    # log.trace("xxx")


    # @log.catch  # 整个函数自动加上try， catch。自动捕获异常，并且通过日志打印
    # def test():
    #     print(3 / 0)

    # 等同与上述 加@log.catch的方法
    def test():
        try:
            print(3 / 0)
        except ZeroDivisionError as e:
            log.error(e)
            log.exception(e)  # 以后常用

    test()