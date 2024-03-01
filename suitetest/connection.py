# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: connection.py.                                                       *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************
import shutil

import Config
import glob
import Logger
import Monitor
import os.path
import tempfile

from JsCreator.Process import Process
from JsCreator.JsCreator import RunningModeArch
from Libs import DssRhino
from Opt import FolderOpt, Analysis


class CCSConnectionVerify:
    def __init__(self):
        self.running_config = Config.running_config

    @Monitor.Monitor.ExceptionMonitor.check_connection_test
    def test_ccs_connection_verify(self):
        # = 临时主路径
        Logger.ulogger.fusion_log('Building the folder construction for CCS connection test...', level=Logger.U_DEBUG)
        __temp_base = tempfile.gettempdir()
        _suffix, _prefix = '_CCS_CONNECTION', 'TEST_'
        # = 清理
        Logger.ulogger.fusion_log('Residual test directory cleanning...', level=Logger.U_DEBUG)
        for _c_dir in glob.glob(os.path.join(__temp_base, '{}*{}'.format(_prefix, _suffix))):
            shutil.rmtree(_c_dir, ignore_errors=True)
        # = 测试
        # _tempdir = tempfile.mkdtemp(suffix='_CCS_CONNECTION', prefix='TEST_', dir=__temp_base)     # 不会自动删除
        with tempfile.TemporaryDirectory(suffix=_suffix, prefix=_prefix, dir=__temp_base) as _tempdir:
            Logger.ulogger.fusion_log(f'Build Env: {_tempdir}', level=Logger.U_DEBUG)

            # = 创建临时工作空间
            _folder_init = FolderOpt.FolderSystem(_tempdir)
            __test_base_structure = _folder_init.folder_tree_create()
            _test_run_structure = _folder_init.runtime_result(__test_base_structure)
            _, _v_memory_folder, _v_xml_folder, _, _ = __test_base_structure
            _v_cio_file, _, _, _v_js_file, _ = _test_run_structure
            Logger.ulogger.fusion_log('Folder construction build completes', level=Logger.U_DEBUG)

            # = 构建运行测试文件
            Logger.ulogger.fusion_log('Building JS file for CCS connection test...', level=Logger.U_DEBUG)
            emulator_params_dict = {
                "time_sleep": "500",
                "ccxml_file": self.running_config.deviceconfig_ccxml,
                "running_ctrl": self.running_config.projectset_ctrl,
                "session_config": self.running_config.deviceconfig_config
            }
            function_params_dict = {
                "memory_save": self.running_config.memoryconfig_datasection,
                "result_folder": _v_memory_folder
            }
            end_params_dict = {}

            # = 对断点地址列表进行断点设置 JS 构造。
            js_builder = Process(_v_js_file)
            builder_cls = RunningModeArch(-1)  # -1 为预留的 测试连接 方案，注：此处仅为定义，不能直接使用，名称不一致
            js_builder.construct_building(
                builder_cls.mode_cls(), emulator_params_dict, function_params_dict, end_params_dict)

            # = 对 JS 进行参数修订
            js_change_params_dict = {
                'replace::xml_path': _v_xml_folder,
                'replace::cio_file': _v_cio_file,
                'replace::reserve_save_text': ''
            }
            js_builder.replace_js_var(js_change_params_dict)
            Logger.ulogger.fusion_log('Connection test JS build completes', level=Logger.U_DEBUG)

            # = 尝试调用
            call_dss = DssRhino.CallDssRhino(self.running_config.deviceconfig_invoke.replace('\\', '/'))
            runtime_flag_file = call_dss.dss_call(_v_js_file)

            # = 运行状态校验
            file_analysis = Analysis.FileAnalysis()
            xml_file_list = glob.glob(os.path.join(_v_xml_folder, "*.xml"))
            stand_memory_list = ['{}.dat'.format(x['Name']) for x in self.running_config.memoryconfig_datasection]
            xml_status, xml_extrac_file = file_analysis.xml_result_parsing(xml_file_list)
            memory_status = file_analysis.memory_result_check(_v_memory_folder, stand_memory_list)

        return xml_status and memory_status, _tempdir
