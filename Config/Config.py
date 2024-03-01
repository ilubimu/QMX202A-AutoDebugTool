# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: Config.py.                                                           *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

import configparser
import JsCreator
import Logger
import Monitor


class Config:
    def __init__(self):
        # WorkSpace
        self.workspace_workspace = None
        self.workspace_prj_dir = None
        # DeviceConfig
        self.deviceconfig_ccxml = None
        self.deviceconfig_config = None
        self.deviceconfig_invoke = None
        # DeviceInit
        self.deviceinit_gel = None
        # RunningSet
        self.runningset_autocountset = None
        self.runningset_typeset = None
        self.runningset_roundtime = None
        self.runningset_mode = None
        # ProjectSet
        self.projectset_ctrl = None
        self.projectset_breakpoint = None
        # MemoryConfig
        self.memoryconfig_datasection = None
        # ToolConfig
        self.toolconfig_mode = None

    # @staticmethod
    # def __running_mode_select(mode):
    #     _base_mode_config = {
    #         '1': 'LoadExportRun',
    #         '2': 'LoadExport',
    #         '3': 'LoadRun',
    #         '4': 'LoadRunExport'
    #     }
    #     _mode_num_set, _mode_set = zip(*_base_mode_config.items())
    #     if mode in _mode_set:
    #         return eval('{}.{}'.format('JsCreator', mode))
    #     elif mode in _mode_num_set:
    #         return eval('{}.{}'.format('JsCreator', _mode_set[_mode_num_set.index(mode)]))
    #     else:
    #         raise Exception("Running mode set error, only for "
    #                         "'LoadExportRun(1), LoadExport(2), LoadRun(3), LoadRunExport(4)'")

    @Monitor.Monitor.ExceptionMonitor.check_config_input
    def read_config(self, cfg_file_temp):
        config = configparser.ConfigParser()
        config.read(cfg_file_temp, encoding='utf-8')

        # WorkSpace
        _workspace = config.get('WorkSpace', 'workspace')
        _project_dir = config.get('WorkSpace', 'project_dir')
        self.workspace_workspace = _workspace
        self.workspace_prj_dir = _project_dir
        workspace = [_workspace, _project_dir]
        Logger.ulogger.fusion_log(workspace, level=Logger.U_DEBUG)

        # DeviceConfig
        _device_ccxml = config.get('DeviceConfig', 'device_ccxml')
        _device_config = config.get('DeviceConfig', 'device_config')
        _dss_invoke = config.get('DeviceConfig', 'dss_invoke')
        self.deviceconfig_ccxml = _device_ccxml
        self.deviceconfig_config = _device_config
        self.deviceconfig_invoke = _dss_invoke
        device_config = [_device_ccxml, _device_config, _dss_invoke]
        Logger.ulogger.fusion_log(workspace, level=Logger.U_DEBUG)

        #  DeviceInit
        # _ddr_init = config.get('Init', 'DDR')
        __gel_dic = config.get('DeviceInit', 'gel')
        _gel_init = eval(__gel_dic)
        self.deviceinit_gel = _gel_init
        init = [_gel_init]
        Logger.ulogger.fusion_log(init, level=Logger.U_DEBUG)

        # RunningSet
        __auto_count_set_dic = config.get('RunningSet', 'autocountset')
        _auto_count_set = eval(__auto_count_set_dic)
        __running_type_set_dic = config.get('RunningSet', 'runningtypeset')
        _running_type_set = eval(__running_type_set_dic)
        _running_time = eval(config.get('RunningSet', 'runningtime'))
        _running_time = _running_time if _running_time >= 1 else 1
        __running_mode = config.get('RunningSet', 'runningmode')
        # _running_mode = self.__running_mode_select(__running_mode)
        _running_mode = JsCreator.RunningModeArch(__running_mode)
        self.runningset_autocountset = _auto_count_set
        self.runningset_typeset = _running_type_set
        self.runningset_roundtime = _running_time
        self.runningset_mode = _running_mode
        running_set = [_auto_count_set, _running_type_set, _running_time, _running_mode]
        Logger.ulogger.fusion_log(running_set, level=Logger.U_DEBUG)

        # ProjectSet
        __running_mode_set_dic = config.get('ProjectSet', 'running_ctrl')
        _running_mode_set = eval(__running_mode_set_dic)
        __breakpoint_set_list = eval(config.get('ProjectSet', 'running_stop_flag'))
        self.projectset_ctrl = _running_mode_set
        self.projectset_breakpoint = __breakpoint_set_list
        _project_set = [_running_mode_set, __breakpoint_set_list]
        Logger.ulogger.fusion_log(_project_set, level=Logger.U_DEBUG)

        # MemoryConfig
        _memory_config = eval(config.get('MemoryConfig', 'memorydata'))
        self.memoryconfig_datasection = _memory_config
        Logger.ulogger.fusion_log(_memory_config, level=Logger.U_DEBUG)

        # ToolConfig
        __tool_config = config.get('ToolConfig', 'tool_runtime_mode').upper()
        self.toolconfig_mode = __tool_config
        _tool_config = [__tool_config]
        Logger.ulogger.fusion_log(_tool_config, level=Logger.U_DEBUG)

        return workspace, device_config, init, running_set, _project_set, _memory_config, _tool_config
