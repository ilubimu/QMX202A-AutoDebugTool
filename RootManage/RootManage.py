# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: RootManage.py.                                                       *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

import os.path
import sys


class RootManage:
    def __init__(self):
        self.root_path = self.forzen_current_path()

        _config_path = r"AutoDebugTool.cfg"  # 配置文件
        _json_path = r"TestDDT.json"  # 数据 json 文件
        _log_file = r'AutoDebugTool.log'  # 运行日志文件

        self.log_file = os.path.join(self.root_path, _log_file)
        self.config_path = os.path.join(self.root_path, _config_path)
        self.json_path = os.path.join(self.root_path, _json_path)

    @staticmethod
    def forzen_current_path():
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        # elif __file__:
        else:
            return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
