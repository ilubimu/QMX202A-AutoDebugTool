#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
AT 2021.8.26
自动化调试： V1.0
实现功能：
'''

# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: AutoTool_Debug_v1.0.py.                                              *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

import glob
import json
import shutil
import subprocess
import os
import sys
import re
from functools import wraps
# import psutil
import time
import signal
import datetime
import configparser

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import unittest
import ddt
from BeautifulReport import BeautifulReport

# root path
config_path = r"./ProConfig_mode.cfg"
json_path = r"TestDDT.json"


class ExceptionMonitor:
    def __init__(self):
        pass

    def check_config_input(self, check_func):
        @wraps(check_func)
        def wrap_the_func(*args, **kwargs):
            try:
                return_result = check_func(*args, **kwargs)
                # print("Check Success")
            except Exception as e:
                return_result = []
                print(str(e))
                print("配置文件格式出错")
                input('Please press enter key to exit ...')
                exit()
            return return_result

        return wrap_the_func


exception_monitor = ExceptionMonitor()


class Config:
    def __init__(self):
        pass

    @exception_monitor.check_config_input
    def read_config(self, cfg_file_temp):
        config = configparser.ConfigParser()
        config.read(cfg_file_temp, encoding='utf-8')

        #     写入参数值
        _workspace = config.get('WorkSpace', 'workspace')
        _project_dir = config.get('WorkSpace', 'project_dir')
        workspace = [_workspace, _project_dir]
        # print(_workspace,_project_dir)
        # print(workspace)

        #    JS配置及运行模式
        _device_ccxml = config.get('DeviceConfig', 'device_ccxml')
        _device_config = config.get('DeviceConfig', 'device_config')
        _dss_invoke = config.get('DeviceConfig', 'dss_invoke')
        device_config = [_device_ccxml, _device_config, _dss_invoke]
        # print(_device_ccxml, _device_config, _dss_invoke)
        # print(device_config)

        #  Init板卡平台初始
        DDRInit = config.get('Init', 'DDR')
        GELDic = config.get('Init', 'GEL')
        GELInit = eval(GELDic)
        RegistersDic = config.get('Init', 'Registers')
        RegistersClear = eval(RegistersDic)
        Init = [DDRInit, GELInit, RegistersClear]
        #     print(DDRInit,GELInit,RegistersClear)
        #     print(Init)

        #     RunningMode设置：类型，次数
        auto_count_start = config.get('RunningSet', 'auto_count_start')
        RunningTypeSetDic = config.get('RunningSet', 'RunningTypeSet')
        RunningTypeSet = eval(RunningTypeSetDic)
        RunningTime = config.get('RunningSet', 'RunningTime')
        RunningSet = [RunningTypeSet, RunningTime, auto_count_start]
        #     print(RunningType,RunningMode,RunningTime)
        #     print(RunningSet)

        #    ProjectSet设置：调试结果模式
        RunningModeSetDic = config.get('ProjectSet', 'RunningModeSet')
        RunningModeSet = eval(RunningModeSetDic)
        BreakpointSetList = config.get('ProjectSet', 'BreakpointSet')
        ProjectSet = [RunningModeSet, BreakpointSetList]
        MemoryConfig = config.get('MemoryConfig', 'MemoryData')
        #     print(CodeStyle,SaveMode,ListMemoryData)
        #     print(MemoryConfig)
        return workspace, device_config, Init, RunningSet, ProjectSet, MemoryConfig


class FolderSystem:
    def __init__(self, works_pace):
        self.workspace = works_pace
        self.running_result = r"{}\RunningResult".format(works_pace)
        self.project_result = r"{}\ProjectResult".format(works_pace)
        self.all_result = r"{}\AllResultSave".format(works_pace)

    def folder_all_result_create(self):
        os.makedirs(self.all_result)

    def folder_project_result_create(self):
        os.makedirs(self.project_result)

    def folder_project_save(self, pro_name):
        """
        程序运行完成后结果的保存
        :param project_name:
        :return:
        """
        save_first_folder = r"{0}\{1}".format(self.project_result, pro_name)
        if os.path.exists(self.project_result):
            shutil.move(self.running_result, save_first_folder)
        else:
            os.makedirs(self.project_result)
            shutil.move(self.running_result, save_first_folder)
        print(save_first_folder)
        # input("Enter")
        # 待优化文件夹改名
        return 0

    def folder_project_multi_save(self, first_dir_name, sub_dir_name):
        """
        程序运行完成后结果的保存
        :param sub_dir_name:
        :param first_dir_name:
        :return:
        """
        save_first_folder = r"{0}\{1}".format(self.project_result, first_dir_name)
        save_result_folder = r"{0}\{1}".format(save_first_folder, sub_dir_name)
        # print(save_first_folder)
        # print(save_result_folder)
        # if os.path.exists(save_first_folder):
        #     shutil.move(self.running_result, save_result_folder)
        # else:
        #     os.makedirs(save_first_folder)
        #     shutil.move(self.running_result, save_result_folder)
        if not os.path.exists(save_first_folder):
            os.makedirs(save_first_folder)
        if os.path.exists(save_result_folder):
            shutil.rmtree(save_result_folder)
        shutil.move(self.running_result, save_result_folder)
        # 待优化文件夹改名
        # return 0
        return save_result_folder

    def folder_all_save(self):
        local_time = datetime.datetime.now()
        time_style = local_time.strftime("%Y%m%d(%H-%M-%S)")
        all_result_path = self.all_result + time_style
        shutil.move(self.all_result, all_result_path)
        return 0

    def folder_run_count_save(self, run_count):
        local_time = datetime.datetime.now()
        time_style = local_time.strftime("%Y%m%d(%H-%M-%S)")
        count_folder = r"{}\Cnt：{}".format(self.all_result, run_count)
        run_count_path = r"{}_{}".format(count_folder, time_style)
        shutil.move(self.project_result, r"{}".format(run_count_path))
        return 0

    def folder_tree_create(self):
        file_path_list = list()
        folder_name = ["XML", "CIO", "Memory", "JsScript", "ResultAddressData"]
        for name in folder_name:
            makedir = r"{}\{}".format(self.running_result, name)
            if os.path.exists(makedir):
                shutil.rmtree(makedir)
            os.makedirs(makedir)
            # try:
            #     os.makedirs(makedir)
            # except Exception as error:
            #     print(str(error))
            #     print("已有当前文件夹")
            #     exit()
            file_path_list.append(makedir)
        return file_path_list

    def folder_tree_create_test(self):
        """
        测试函数：此函数不会创建文件夹只是构建文件路径
        :return:返回一个文件路径
        """
        file_path_list = list()
        folder_name = ["XML", "CIO", "Memory", "JsScript"]
        for name in folder_name:
            makedir = r"{}\{}".format(self.running_result, name)
            # os.makedirs(makedir)
            # try:
            #     os.makedirs(makedir)
            # except Exception as error:
            #     print(str(error))
            #     print("已有当前文件夹")
            #     exit()
            file_path_list.append(makedir)
        return file_path_list

    @staticmethod
    def runtime_result(folder_list):
        """
        文件构建，将后续结果需要的文件事先构建好其字符路径。
        :return:返回一个包含xml_path，cio_file，memory_file，js_file四个路径的字符串的列表
        """
        result_list = list()
        xml_path = r"{}".format(folder_list[0]).replace("\\", "/")
        cio_file = r"{}\CIOFile.txt".format(folder_list[1]).replace("\\", "/")
        memory_file = r"{}\MemoryFile.dat".format(folder_list[2]).replace("\\", "/")
        js_file = r"{}\FirstVersion.js".format(folder_list[3])
        running_data_path = r"{}".format(folder_list[4]).replace("\\", "/")
        result_list.append(xml_path)
        result_list.append(cio_file)
        result_list.append(memory_file)
        result_list.append(js_file)
        result_list.append(running_data_path)
        return result_list

    def connect_folder_func(self):
        """
        链接文件功能的函数，组合使用的方式
        :return:返回一个列表
        """
        folder_tree_list = self.folder_tree_create()
        result_tree_list = self.runtime_result(folder_tree_list)
        # print(result_tree_list)
        return result_tree_list


def find_extension_file(find_path, filename_extension):
    """
    索引一个路径下的某个后缀名，返回根据查找到的所有文件的路径组成的列表
    :param find_path:索引路径
    :param filename_extension:需要索引的文件拓展名
    :return: 返回索引路径下带文件拓展名文件路径的列表
    """
    list_pro_path = list()
    for root, dirs, names in os.walk(find_path):
        for name in names:
            if os.path.splitext(name)[1] == filename_extension:
                pro_name = os.path.join(root, name)
                list_pro_path.append(pro_name)
    return list_pro_path


# DebugMode
class DebugMode:

    # 1.加载导出模式
    def load_export(self):
        pass

    # 2.加载运行模式
    def load_run(self):
        pass

    # 3.加载导出运行模式
    def load_export_run(self):
        pass


def debug_mode_select(mode_set):
    debug_mode = DebugMode()
    if mode_set == "1":
        # 1.加载导出模式
        debug_mode.load_export()
        return "LoadExport"
    elif mode_set == "2":
        # 2.加载运行模式
        debug_mode.load_run()
        return "LoadExport"
    elif mode_set == "3":
        # 3.加载导出运行模式
        debug_mode.load_export_run()
        return "LoadExport"
    else:
        print("just support debug mode：1,2,3")
        return False


# === Abstract Builder
class JsBuilder:
    def emulator_init(self, emulator_params_dict):
        raise NotImplementedError

    def function(self, function_params_dict):
        raise NotImplementedError

    def end_process(self, end_params_dict):
        raise NotImplementedError

    def __repr__(self):
        return "check all step"


# === 1: LoadExport
class LoadExport(JsBuilder):
    def emulator_init(self, emulator_params_dict):
        ccxml_file = emulator_params_dict["ccxml_file"].replace("\\", "/")
        ccxml_config = emulator_params_dict["ccxml_config"].replace("\\", "/")
        emulator_context = """
// Import the DSS packages into our namespace to save on typing
importPackage(Packages.com.ti.debug.engine.scripting)
importPackage(Packages.com.ti.ccstudio.scripting.environment)
importPackage(Packages.java.lang)
var DeviceCCXMLFile = \"{0}\";
var script = ScriptingEnvironment.instance();
var ds = script.getServer( \"DebugServer.1\" );
ds.setConfig( DeviceCCXMLFile );
debugSession_0 = {1}
Thread.sleep(1000);
debugSession_0.target.connect();
debugSession_0.target.getResetType(0).issueReset();
""".format(ccxml_file, ccxml_config)
        return emulator_context

    def function(self, function_params_dict):
        load_dat_text = function_params_dict["load_dat_text"]
        load_cover_dat_text = function_params_dict["load_cover_dat_text"]
        result_folder = function_params_dict["result_folder"]
        result_folder = result_folder.replace("\\", "/")
        function_context = ("""
//Function：Run and get PCvalue
Thread.sleep(500);
{0}
Thread.sleep(500);

{1}
debugSession_0.memory.saveData2( 0x300000, 0, 0x1FFFF, "{2}/Chip_Flash.dat", 15, false);
debugSession_0.memory.saveData2( 0x0000, 0, 0x200, "{2}/M0_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0x0400, 0, 0x200, "{2}/M1_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0x8000, 0, 0x800, "{2}/L0_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0x9000, 0, 0x800, "{2}/L1_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0xA000, 0, 0x800, "{2}/L2_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0xB000, 0, 0x800, "{2}/L3_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0xC000, 0, 0x800, "{2}/L4_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0xD000, 0, 0x800, "{2}/L5_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0xE000, 0, 0x800, "{2}/L6_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0xF000, 0, 0x800, "{2}/L7_SRAM.dat", 15, false);
Thread.sleep(500);
""").format(load_dat_text, load_cover_dat_text, result_folder)
        return function_context

    def end_process(self, end_params_dict):
        end_context = """
debugSession_0.target.disconnect();
        """
        return end_context


# === 2: LoadRun
class LoadRun(JsBuilder):
    def emulator_init(self, emulator_params_dict):
        ccxml_file = emulator_params_dict["ccxml_file"].replace("\\", "/")
        ccxml_config = emulator_params_dict["ccxml_config"].replace("\\", "/")
        emulator_context = """
// Import the DSS packages into our namespace to save on typing
importPackage(Packages.com.ti.debug.engine.scripting)
importPackage(Packages.com.ti.ccstudio.scripting.environment)
importPackage(Packages.java.lang)
var DeviceCCXMLFile = \"{0}\";
var script = ScriptingEnvironment.instance();
var ds = script.getServer( \"DebugServer.1\" );
ds.setConfig( DeviceCCXMLFile );
debugSession_0 = {1}
Thread.sleep(1000);
debugSession_0.target.connect();
debugSession_0.target.getResetType(0).issueReset();
""".format(ccxml_file, ccxml_config)
        return emulator_context

    def function(self, function_params_dict):
        load_dat_text = function_params_dict["load_dat_text"]
        load_cover_dat_text = function_params_dict["load_cover_dat_text"]
        result_folder = function_params_dict["result_folder"]
        result_folder = result_folder.replace("\\", "/")
        function_context = ("""
//Function：Run and get PCvalue
Thread.sleep(500);
{0}
Thread.sleep(500);

{1}
debugSession_0.memory.saveData2( 0x300000, 0, 0x1FFFF, "{2}/Chip_Flash.dat", 15, false);
debugSession_0.memory.saveData2( 0x0000, 0, 0x200, "{2}/M0_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0x0400, 0, 0x200, "{2}/M1_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0x8000, 0, 0x800, "{2}/L0_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0x9000, 0, 0x800, "{2}/L1_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0xA000, 0, 0x800, "{2}/L2_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0xB000, 0, 0x800, "{2}/L3_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0xC000, 0, 0x800, "{2}/L4_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0xD000, 0, 0x800, "{2}/L5_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0xE000, 0, 0x800, "{2}/L6_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0xF000, 0, 0x800, "{2}/L7_SRAM.dat", 15, false);
Thread.sleep(500);
""").format(load_dat_text, load_cover_dat_text, result_folder)
        return function_context

    def end_process(self, end_params_dict):
        end_context = """
debugSession_0.target.disconnect();
        """
        return end_context


# === 3: LoadExportRun
class LoadExportRun(JsBuilder):
    def emulator_init(self, emulator_params_dict):
        ccxml_file = emulator_params_dict["ccxml_file"].replace("\\", "/")
        ccxml_config = emulator_params_dict["ccxml_config"].replace("\\", "/")
        emulator_context = """
// Import the DSS packages into our namespace to save on typing
importPackage(Packages.com.ti.debug.engine.scripting)
importPackage(Packages.com.ti.ccstudio.scripting.environment)
importPackage(Packages.java.lang)
var DeviceCCXMLFile = \"{0}\";
var script = ScriptingEnvironment.instance();
var ds = script.getServer( \"DebugServer.1\" );
ds.setConfig( DeviceCCXMLFile );
debugSession_0 = {1}
Thread.sleep(1000);
debugSession_0.target.connect();
debugSession_0.target.getResetType(0).issueReset();
""".format(ccxml_file, ccxml_config)
        return emulator_context

    def function(self, function_params_dict):
        load_dat_text = function_params_dict["load_dat_text"]
        load_cover_dat_text = function_params_dict["load_cover_dat_text"]
        result_folder = function_params_dict["result_folder"]
        result_folder = result_folder.replace("\\", "/")
        function_context = ("""
//Function：Run and get PCvalue
Thread.sleep(500);
{0}
Thread.sleep(500);

{1}
debugSession_0.memory.saveData2( 0x300000, 0, 0x1FFFF, "{2}/Chip_Flash.dat", 15, false);
debugSession_0.memory.saveData2( 0x0000, 0, 0x200, "{2}/M0_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0x0400, 0, 0x200, "{2}/M1_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0x8000, 0, 0x800, "{2}/L0_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0x9000, 0, 0x800, "{2}/L1_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0xA000, 0, 0x800, "{2}/L2_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0xB000, 0, 0x800, "{2}/L3_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0xC000, 0, 0x800, "{2}/L4_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0xD000, 0, 0x800, "{2}/L5_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0xE000, 0, 0x800, "{2}/L6_SRAM.dat", 15, false);
debugSession_0.memory.saveData2( 0xF000, 0, 0x800, "{2}/L7_SRAM.dat", 15, false);
Thread.sleep(500);
""").format(load_dat_text, load_cover_dat_text, result_folder)
        return function_context

    def end_process(self, end_params_dict):
        end_context = """
debugSession_0.target.disconnect();
        """
        return end_context


# Director
class Process:
    def __init__(self, js_file_path):
        self.builder = None
        self.mode = None
        self.js_file_path = js_file_path

    def execute_mode(self, mode):
        print("Step: select mode")
        self.mode = mode
        return self.mode

    def gen_js_text(self, text):
        with open(self.js_file_path, "w+", encoding="utf-8") as fp:
            fp.write(text)
        return self.js_file_path

    # Director
    def construct_building(self, cls, emulator_param_dict, function_param_dict, end_param_dict):
        self.builder = cls()
        emulator_context = self.builder.emulator_init(emulator_param_dict)
        function_context = self.builder.function(function_param_dict)
        end_context = self.builder.end_process(end_param_dict)
        complex_js_text = emulator_context + function_context + end_context
        js_file_path = self.gen_js_text(complex_js_text)
        return js_file_path

    # Product
    @property
    def building(self):
        return self.builder


@ddt.ddt
class TestFrame(unittest.TestCase):
    """
    最基础使用框架：TestCase
    方法：setUp，tearDown，assertTrue
    特点：TestCase的测试顺序不是固定的是随机选择进行测试的。
    """

    @classmethod
    @ddt.data(*json_path)
    @ddt.data(*config_path)
    def setUpClass(cls):
        """
        step1: 读取config文件参数
        :return:
        """
        # 读取配置文件
        # print("into setUpClass")
        # 待修改替换掉配置文件的参数
        config = Config()
        (workspace_configs, et_configs, frame_configs, tool_chain_configs, breakpoint_configs) \
            = config.read_config(config_path)
        cls.work_space_list = workspace_configs
        cls.et_configs = et_configs
        cls.init_board_list = frame_configs
        cls.running_mode_list = tool_chain_configs
        cls.project_set_list = breakpoint_configs
        # print("over setUpClass")

    @classmethod
    def tearDownClass(cls):
        """
        进行最终结果数据保存
        :return:
        """
        print("完成一轮测试")
        pass
        # cls.folder_init.folder_all_save()
        # print("最后清理环境")

    def setUp(self):
        """
        step2: workspace工作空间处理（目录结构）
        重复执行的构造函数
        构造单次测试时准备的文件夹
        :return:返回值为一个包含所有结果路径的列表
        """
        # print("into setUp")
        work_space_path = self.__class__.work_space_list[0]
        self.folder_init = FolderSystem(work_space_path)
        folder_tree_list = self.folder_init.folder_tree_create()
        # # 不生成文件夹，只返回空的文件路径
        # folder_tree_list = self.__class__.folder_init.folder_tree_create_test()
        self.result_list = self.folder_init.runtime_result(folder_tree_list)
        # print("setup completed")

    def tearDown(self):
        """
        单次执行结束操作，其中包含
        1.解析单个out执行后的xml文件
        2.解析单个out执行后的dat文件
        3.进行单次执行后的结果保存
        :return:
        """
        xml_path = self.result_list[0]
        xml_folder = os.path.abspath(os.path.join(xml_path, ".."))
        xml_parser(xml_folder)
        self.folder_init.folder_project_save(self.out_name)
        # print("tearDown completed")
        # A、B握手检测
        # while True:
        #     if os.path.exists(XDS100V3_handshake_path):
        #         print("握手成功，测试已同步")
        #         break

    @ddt.file_data(json_path)
    def test_case_one(self, out_path):
        """
        1.通过DDT数据驱动传递Json文件中字典的values到TestCase中。
        :return:
        """
        print("Test case")
        print(out_path)

        # ===== 1. 解析out
        # === 获得工程名
        project_name = os.path.splitext(os.path.basename(out_path))[0]
        # === 修改out文件路径
        project_path_fix = out_path.replace("\\", '/')

        # ===== 2.文件结构识别
        xml_path = self.result_list[0]
        cio_file = self.result_list[1]
        memory_file = self.result_list[2]
        js_file = self.result_list[3]
        # print(memory_file)

        # ===== 3.构建运行JS
        # ===== 参数配置：三种模式（loadexport，loadrun， loadexportrun）参数冗余覆盖。
        emulator_params_dict = {"ccxml_file": et_configs[0],
                                "ccxml_config": et_configs[1],
                                "xml_dir": dir_dict['xml_dir']}
        function_params_dict = {"load_out_text": js_out_text,
                                "set_pc_list_text": breakpoint_pc_list,
                                "right_end_flag": frame_right_flag,
                                "error_end_flag": frame_error_flag,
                                "memory_dir": dir_dict['memory_dir']}
        end_params_dict = {}
        # ===== 对断点地址列表进行断点设置:JS构造。
        js_builder = Process(js_file)
        js_builder.construct_building(SetBreakPoint, emulator_params_dict, function_params_dict, end_params_dict)

        # ===== 4.调试运行程序并保存dat：调试debug脚本。
        call_dss = CallDssRhino(dss_bat_path)
        runtime_flag_file = call_dss.dss_call(js_file)

        # ===== 5.判断程序结束标签
        # === loadexport，loadrun， loadexportrun
        # print(runtime_flag_file)
        # while True:
        #     if os.path.exists(runtime_flag_file):
        #         self.assertTrue(os.path.exists(runtime_flag_file), "相等")
        #         # os.remove(r"{}".format(runtime_flag_file))
        #         break
        # === 识别结束标签和dat生成情况，此处的断言即作为测试用例通过与否统计的断言。
        self.assertTrue(os.path.exists(runtime_flag_file), "相等")


class TestBaseSuite:
    def __init__(self, workspace, module):
        self.workspace = workspace
        self.module = module

    def loader_suite(self):
        """
        加载Loader至Suite中，传递参数Suite
        :param self:None
        :return:参数Suite
        """
        suite_test2 = unittest.TestSuite()
        loader = unittest.TestLoader()
        # 加载的是一个测试类
        name = loader.loadTestsFromName(self.module)
        # 也可以传递单个Loader给Runner，跳过Suite进行运行。
        suite_test2.addTest(name)
        return suite_test2

    @staticmethod
    def runner_report(suite_name, project_result):
        # test_report_path = r"{}\report".format(self.workspace)
        test_report_path = project_result
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')
        test_report_name = '测试报告' + str(now_time)
        result = BeautifulReport(suite_name)
        result.report(description='测试', filename=test_report_name, report_dir=test_report_path, theme='theme_default')
        return 0

    def connect_suite(self, project_result):
        suite = self.loader_suite()
        # print(suite)
        # exit(0)
        self.runner_report(suite, project_result)
        return 0


if __name__ == "__main__":

    # ===== step1: 读取config文件参数
    testModule = 'TestFrame'
    configAnalysis = ConfigAnalysis(xds100v2_run_config_path)
    workSpaceList = configAnalysis.workspace()
    workSpacePath = workSpaceList[0]
    # print(workSpacePath, type(workSpacePath))
    # exit()
    runningModeList = configAnalysis.running_mode()
    runningCountSet = runningModeList[1]
    # print(runningCountSet, type(runningCountSet))
    # # exit()

    # ===== 2.生成顶层的两个文件夹：allResult和projectResult
    TestUnitFrame = TestBaseSuite(workSpacePath, testModule)
    folderInit = FolderSystem(workSpacePath)
    folderInit.folder_all_result_create()
    projectFolder = folderInit.project_result
    # print(projectFile, type(projectFile))

    # ===== 3.查找到out文件路径并编排成字典存放到json文件中
    workspace_path = workspace_configs[0]
    project_top_path = workspace_configs[1]
    findFileList = find_extension_file(project_top_path, ".out")
    print("Start: 索引out文件")
    print("\n".join(findFileList))
    print("Success: 索引out文件完成")

    # ===== 4.处理实现Travel和Special模式的两种方案。
    runningTypeSet = runningModeList[0]
    if runningTypeSet['RunningType'] == 'Travel':
        runningOutList = findFileList
    elif runningTypeSet['RunningType'] == 'Special':
        runningOutList = findFileList[int(runningTypeSet['StartPro']):int(runningTypeSet['EndPro'])]
    else:
        runningOutList = list()
        print("Please enter right config [RunningMode]-runningTypeSet-RunningType param: Travel/Special")
    # 处理结束
    listOutName = fileAnalysis.file_split(runningOutList)
    # print(list_out_name)
    findFileDict = dict(zip(listOutName, runningOutList))
    ddtDataPath = json_path
    with open(ddtDataPath, "w+") as f:
        f.write(json.dumps(findFileDict, ensure_ascii=False, indent=4))
        f.seek(0)
    # ===== 5.根据执行次数进行循环遍历
    for runCount in range(runningCountSet):
        # 运行后自动生成报告
        runCount += 1
        TestUnitFrame.connect_suite(projectFolder)
        # countPath = r"{}\AllResultSave\{}".format(ccsWorkSpace, runCount)
        folderInit.folder_run_count_save(runCount)
        # exit()
    folderInit.folder_all_save()
