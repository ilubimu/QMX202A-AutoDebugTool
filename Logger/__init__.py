# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: __init__.py.                                                         *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

import RootManage

from Logger import Logger

# 特征值
U_NOTSET = Logger.logging.NOTSET
U_DEBUG = Logger.logging.DEBUG
U_INFO = Logger.logging.INFO
U_WARNING = Logger.logging.WARNING
U_ERROR = Logger.logging.ERROR
U_CRITICAL = Logger.logging.CRITICAL
U_FATAL = Logger.logging.FATAL

# 日志 / 终端输出等级
f_log_level = U_DEBUG  # 建议使用 logging.DEBUG 等级
t_log_level = U_INFO  # 正式版本应使用 logging.INFO 及以上等级

# 初始化日志
ulogger = Logger.FusionLog(
    RootManage.root_manager.log_file, file_level=f_log_level, terminal_level=t_log_level)
ulogger.file_logger.file_log_init()
ulogger.file_logger.file_text_log(
    'This log records only the primary running status information', level=U_INFO)
ulogger.file_logger.file_text_log(RootManage.root_manager.root_path, level=U_INFO)
ulogger.file_logger.file_text_log(ulogger.spacer + '\n', level=U_INFO, formatter=ulogger.fmt_message)
