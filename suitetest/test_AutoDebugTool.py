# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: test_AutoDebugTool.py.                                               *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

import Config
import ddt
import glob
import Logger
import Monitor
import os.path
import random
import RootManage
import time
import unittest

from typing import Union

from JsCreator import Process
from Libs import DssRhino
from Opt import Analysis, FolderOpt, prefix_indent


class Counter:
    def __init__(self, count_start: Union[int, None]):
        self.__counter = count_start

    def count_increase(self, increass):
        if self.__counter is not None:
            self.__counter += increass

    def count_decrease(self, decreass):
        if self.__counter is not None:
            self.__counter -= decreass

    def counter(self):
        return self.__counter


@ddt.ddt
class TestFrame(unittest.TestCase):
    """
    最基础使用框架：TestCase
    方法：setUp，tearDown，assertTrue
    特点：TestCase的测试顺序不是固定的是随机选择进行测试的。
    """

    @classmethod
    @ddt.data(RootManage.root_manager.config_path)
    def setUpClass(cls):
        """
        step1: 读取config文件参数
        :return:
        """
        # 读取配置文件
        cls.running_config = Config.running_config
        cls.stand_memory_list = ['{}.dat'.format(x['Name']) for x in cls.running_config.memoryconfig_datasection]
        cls.file_analysis = Analysis.FileAnalysis()
        _run_start_index = eval(cls.running_config.runningset_typeset['StartPro']) \
            if cls.running_config.runningset_typeset['RunningType'] == 'Special' else 1
        _save_start_index = eval(cls.running_config.runningset_autocountset['user_count_start']) \
            if cls.running_config.runningset_autocountset['index_count'].lower() == 'on' else None
        cls.save_index_counter = Counter(_save_start_index)
        cls.run_index_counter = Counter(_run_start_index)
        Logger.ulogger.fusion_log('SetUpClass Execution Complete', level=Logger.U_DEBUG)
        time.sleep(random.uniform(0.1, 0.2))
        cls.status = False    # 测试状态

    @classmethod
    def tearDownClass(cls):
        """
        进行最终结果数据保存
        :return:
        """
        Logger.ulogger.fusion_log('tearDownClass Execution Complete', level=Logger.U_DEBUG)
        time.sleep(random.uniform(0.1, 0.2))
        # print("完成一轮测试")
        pass
        # cls.folder_init.folder_all_save()
        # print("最后清理环境")

    def setUp(self):
        """
        step2: workspace 工作空间处理（目录结构）
        重复执行的构造函数
        构造单次测试时准备的文件夹
        :return: 返回值为一个包含所有结果路径的列表
        """
        # print("into setUp")
        work_space_path = self.running_config.workspace_workspace
        self.folder_init = FolderOpt.FolderSystem(work_space_path)
        self.folder_tree_list = self.folder_init.folder_tree_create()
        # # 不生成文件夹，只返回空的文件路径
        # folder_tree_list = self.__class__.folder_init.folder_tree_create_test()
        self.result_list = self.folder_init.runtime_result(self.folder_tree_list)
        # print("setup completed")
        self.out_name = None
        Logger.ulogger.fusion_log('setUp Execution Complete', level=Logger.U_DEBUG)
        time.sleep(random.uniform(0.1, 0.2))
        self.status = False    # 复位每轮测试状态值

    def tearDown(self):
        """
        单次执行结束操作，其中包含
        # 1.解析单个 out 执行后的 xml 文件
        # 2.解析单个 out 执行后的 dat 文件
        3.进行单次执行后的结果保存
        :return:
        """
        _savecount = self.save_index_counter.counter()
        _prefix = 'A{}_'.format(str(_savecount).zfill(prefix_indent)) if _savecount is not None else ''
        _save_name = '{}{}'.format(_prefix, self.out_name)
        self.save_index_counter.count_increase(1)
        self.run_index_counter.count_increase(1)
        _runtime_mode = self.running_config.toolconfig_mode
        runtime_file_clean = False if _runtime_mode == 'DEBUG' or not self.status else True
        self.folder_init.folder_project_save(_save_name, runtime_clean=runtime_file_clean)
        # print("tearDown completed")
        # A、B握手检测
        # while True:
        #     if os.path.exists(XDS100V3_handshake_path):
        #         print("握手成功，测试已同步")
        #         break
        Logger.ulogger.fusion_log('tearDown Execution Complete', level=Logger.U_DEBUG)
        time.sleep(random.uniform(0.1, 0.2))

    @ddt.file_data(RootManage.root_manager.json_path)
    @Monitor.Monitor.ExceptionMonitor.check_main_test_function(
        Config.running_config.workspace_prj_dir,
        Config.running_config.runningset_typeset,
        RootManage.root_manager.json_path)
    def test_case_single(self, out_path, test_msg='执行异常'):
        '''{}'''.format(os.path.splitext(os.path.basename(out_path))[0])
        """
        1.通过 DDT 数据驱动传递 Json 文件中字典的 values 到 TestCase 中。
        :return:
        """
        # === 修改out文件路径
        project_path_fix = out_path.replace("\\", '/')
        # print(out_path)

        # ===== 1. 解析out
        # === 获得工程名
        project_name = os.path.splitext(os.path.basename(out_path))[0]
        self.out_name = project_name
        _output = "Test Case: {} - {}".format(self.run_index_counter.counter(), project_name)
        Logger.ulogger.fusion_log(
            _output, level=Logger.U_INFO, formatter='\n{}'.format(Logger.ulogger.fmt_time_a_msg))

        # ===== 2.文件结构识别
        cio_folder, memory_folder, xml_folder, js_folder, running_data_folder = self.folder_tree_list
        cio_file, memory_file, xml_file, js_file, running_data_file = self.result_list
        _output = '\n\t'.join(self.result_list)
        Logger.ulogger.fusion_log(
            _output, level=Logger.U_DEBUG, formatter='\t{}'.format(Logger.ulogger.fmt_message))

        # ===== 3.构建运行JS
        # ===== 参数配置：三种模式（loadexport，loadrun， loadexportrun）参数冗余覆盖。
        emulator_params_dict = {
            "time_sleep": "500",
            "ccxml_file": self.running_config.deviceconfig_ccxml,
            "running_ctrl": self.running_config.projectset_ctrl,
            "session_config": self.running_config.deviceconfig_config
        }
        function_params_dict = {
            "time_sleep": "500",
            "running_ctrl": self.running_config.projectset_ctrl,
            "running_stop_flag": self.running_config.projectset_breakpoint,
            "memory_save": self.running_config.memoryconfig_datasection,
            "result_folder": memory_folder
        }
        end_params_dict = {}

        # ===== 对断点地址列表进行断点设置 JS 构造。
        js_builder = Process.Process(js_file)
        running_mode = self.running_config.runningset_mode  # 不能直接使用，此处仅为申明，并非实际类
        js_builder.construct_building(
            running_mode.mode_cls(), emulator_params_dict, function_params_dict, end_params_dict)

        # ===== 对 JS 进行参数修订
        js_change_params_dict = {
            'replace::out_file': project_path_fix,
            'replace::xml_path': xml_folder,
            'replace::cio_file': cio_file,
            'replace::reserve_save_text': ''
        }
        js_builder.replace_js_var(js_change_params_dict)

        # ===== 4.调试运行程序并保存dat: 调试debug脚本。
        call_dss = DssRhino.CallDssRhino(self.running_config.deviceconfig_invoke.replace('\\', '/'))
        runtime_flag_file = call_dss.dss_call(js_file)
        # runtime_flag_file = call_dss.dss_call_debug(js_file)

        # ===== 判断运行状态
        # = XML
        # if not issubclass(running_mode_cls, JsCreator.LoadExport):
        if running_mode.mode_name() != 'LoadExport':
            xml_file_list = glob.glob(os.path.join(xml_folder, "*.xml"))
            xml_status, xml_extrac_file = self.file_analysis.xml_result_parsing(xml_file_list)
        else:
            xml_status = True
        # = Memory
        # if not issubclass(running_mode_cls, JsCreator.LoadRun):
        if running_mode.mode_name() != 'LoadRun':
            memory_status = self.file_analysis.memory_result_check(memory_folder, self.stand_memory_list)
        else:
            memory_status = True

        # === 识别结束标签和 dat 生成情况，此处的断言即作为测试用例通过与否统计的断言。
        test_status = os.path.exists(runtime_flag_file) and xml_status and memory_status
        Logger.ulogger.fusion_log('Test one done, assertive judgment in progress', level=Logger.U_DEBUG)
        Logger.ulogger.fusion_log("操作状态: {0}".format(test_status), level=Logger.U_INFO)
        self.status = test_status    # 运行到此处时传递结果值，如未运行至此处，结果值保持为错误
        self.assertTrue(test_status, msg=test_msg)
