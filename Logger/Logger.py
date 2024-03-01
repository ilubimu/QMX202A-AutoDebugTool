# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: Logger.py.                                                           *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

import logging
import logging.handlers
import sys


class LoggingInfoLog:
    def __init__(self, level: int):
        """ 多次初始化(创建多个) Logger 时，应避免使用相同的 logger_name，
        否则在执行某个更改时可能对其他使用相同 logger_name 的 logger 产生影响 """
        self.main_logger = logging.getLogger(self.__logger_dicide())  # 参数可填对应模块名(区分以避免多次调用重叠)
        self.logger_init(self.main_logger, level)
        # print(logging.Logger.manager.loggerDict.keys())
        self.fmt_levelno = '%(levelno)s'  # 日志级别的数值
        self.fmt_levelname = '%(levelname)s'  # 日志级别的名称
        self.fmt_pathname = '%(pathname)s'  # 当前执行程序路径(sys.argv[0])
        self.fmt_filename = '%(filename)s'  # 当前执行程序名
        self.fmt_funcname = '%(funcName)s'  # 日志的当前函数
        self.fmt_lineno = '%(lineno)d'  # 日志的当前行号
        self.fmt_asctime = '%(asctime)s'  # 日志的时间
        self.fmt_threadid = '%(thread)d'  # 线程 ID
        self.fmt_threadname = '%(threadName)s'  # 线程名称
        self.fmt_processid = '%(process)d'  # 进程 ID
        self.fmt_message = '%(message)s'  # 日志信息
        self.fmt_none = ''  # 无信息
        # 自定义
        self.fmt_time_a_msg = '{} - {}'.format(self.fmt_asctime, self.fmt_message)
        self.spacer = '*' * 100

    @staticmethod
    def __logger_dicide():
        _logger_name_frame = 'main_logger_{}'
        _logger_distinguisher = 0
        while _logger_name_frame.format(str(_logger_distinguisher).zfill(3)) \
                in logging.Logger.manager.loggerDict.keys():
            _logger_distinguisher += 1
        return _logger_name_frame.format(str(_logger_distinguisher).zfill(3))

    @staticmethod
    def logger_init(user_logger: logging.Logger, level=logging.DEBUG):
        user_logger.setLevel(level)

    @staticmethod
    def logger_decide(user_logger: logging.Logger, level: int):
        if level == logging.NOTSET:
            pass
        elif level == logging.DEBUG:
            return user_logger.debug
        elif level == logging.INFO:
            return user_logger.info
        elif level == logging.WARNING:
            return user_logger.warning
        elif level == logging.ERROR:
            return user_logger.error
        elif level == logging.CRITICAL:
            return user_logger.critical
        elif level == logging.FATAL:
            return user_logger.fatal
        else:
            raise Exception("logging level set error, illegal level: {}".format(level))


class TerminalInfoLog(LoggingInfoLog):
    def __init__(self, level=logging.DEBUG):
        super().__init__(level)
        self.terminal_handler = logging.StreamHandler()

    # def terminal_log_init(self, level=logging.DEBUG):
    #     # === 创建默认 logger
    #     self.main_logger.setLevel(level)

    def terminal_text_log(self, log_in_text, stream=sys.stdout,
                          level=logging.DEBUG, formatter='%(asctime)s - %(message)s'):
        # === 创建定制化 handler，用于日志信息写入
        self.terminal_handler = logging.StreamHandler(stream)
        # self.terminal_handler = logging.StreamHandler(sys.stderr)
        self.terminal_handler.setLevel(level)

        # === 配置个性化输出日志格式
        _formatter = logging.Formatter(formatter)
        self.terminal_handler.setFormatter(_formatter)
        self.main_logger.addHandler(self.terminal_handler)

        # === 错误写入日志操作(ERROR 级别)
        # print(type(self.main_logger))
        self.logger_decide(self.main_logger, level)(log_in_text)
        # self.main_logger.error(log_in_text)

        # === 移除操作 handler
        self.main_logger.removeHandler(self.terminal_handler)


class FileInfoLog(LoggingInfoLog):
    def __init__(self, log_in_file, level=logging.DEBUG):
        super().__init__(level)
        # self.fmt_error_detail = '{} | {} | {} | {} | {} | {} | {}\n\t{}'.format(
        #     self.fmt_asctime, self.fmt_levelname, self.fmt_funcname, self.fmt_lineno,
        #     self.fmt_threadid, self.fmt_threadname, self.fmt_processid, self.fmt_message
        # )
        self.log_in_file = log_in_file
        # self.__user_log_init()
        self.file_handler = logging.FileHandler(self.log_in_file)

    def file_log_init(self, log_mode='w+'):
        # === 初始化(清除内容)
        logging.FileHandler(self.log_in_file, log_mode)

    def file_text_log(self, log_in_text, log_mode='a+', level=logging.DEBUG, formatter='%(message)s'):
        # === 创建定制化 handler，用于日志信息写入
        self.file_handler = logging.FileHandler(self.log_in_file, log_mode)
        self.file_handler.setLevel(level)

        # === 配置个性化输出日志格式
        _formatter = logging.Formatter(formatter)
        self.file_handler.setFormatter(_formatter)
        self.main_logger.addHandler(self.file_handler)

        # === 错误写入日志操作(level 级别)
        self.logger_decide(self.main_logger, level)(log_in_text)

        # === 移除操作 handler
        self.main_logger.removeHandler(self.file_handler)


class FusionLog(LoggingInfoLog):
    def __init__(self, log_data_file, file_level=logging.DEBUG, terminal_level=logging.DEBUG):
        super().__init__(logging.DEBUG)
        self.file_logger = FileInfoLog(log_data_file, level=file_level)
        self.terminal_logger = TerminalInfoLog(level=terminal_level)

    def fusion_log(self, log_inf, t_stream=sys.stdout, f_log_mode='a+',
                   level=logging.DEBUG, formatter='%(asctime)s - %(message)s'):
        self.terminal_logger.terminal_text_log(log_inf, stream=t_stream, level=level, formatter=formatter)
        self.file_logger.file_text_log(log_inf, log_mode=f_log_mode, level=level, formatter=formatter)
