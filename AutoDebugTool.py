#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AT 2021.8.26
自动化调试： V1.0
实现功能：
"""
# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: AutoDebugTool.py.                                                    *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************
import Config
import Licenses
import Logger
import os
import random
import RootManage
import suitetest
import time
# import traceback

from Libs import Env, Exit
from Monitor import UserException

if __name__ == "__main__":
    # ===== 1: 读取 Config 文件参数
    Logger.ulogger.fusion_log('Parasing the configuration file...', level=Logger.U_INFO,
                              formatter='\n{}'.format(Logger.ulogger.fmt_time_a_msg))
    testModule = suitetest.TestFrame
    # 环境初始化参量
    auto_runner = Env.EnvInit()
    runner_config = Config.running_config
    Logger.ulogger.fusion_log('Env initialize completes', level=Logger.U_INFO)
    tool_debug_mode = runner_config.toolconfig_mode
    time.sleep(random.uniform(0.2, 0.4))

    try:
        # ===== 2.信息校验
        Logger.ulogger.fusion_log('Verifying licenses...', level=Logger.U_INFO,
                                  formatter='\n{}'.format(Logger.ulogger.fmt_time_a_msg))
        if tool_debug_mode != 'DEBUG':
            _status = Licenses.licenses_verify()
            if not _status:
                raise UserException.LicenseVerifyError
                # Exit.Exit.exit_on_f_in('Licenses verify failed')
        Logger.ulogger.fusion_log('Licenses verified', level=Logger.U_INFO)
        time.sleep(random.uniform(0.3, 0.5))

        # ===== 3.板卡连接测试
        Logger.ulogger.fusion_log('Starting board connection test...', level=Logger.U_INFO,
                                  formatter='\n{}'.format(Logger.ulogger.fmt_time_a_msg))
        suitetest.ccs_connection_test.test_ccs_connection_verify()
        Logger.ulogger.fusion_log('Board connection test: PASS\n', level=Logger.U_INFO)

        # ===== 4.解析
        workSpacePath = runner_config.workspace_workspace
        # print(workSpacePath, type(workSpacePath))
        # sys.exit()
        runningCountSet = runner_config.runningset_roundtime
        # runningModeStr = runner_config.runningset_mode.__name__
        runningMode = runner_config.runningset_mode  # 仅为载体，并非可实际使用的 JS 构造类，仅提供入口等信息
        runningModeStr = runningMode.mode_name()

        # print(runningMode, runningMode().__class__.__name__)
        # print(runningCountSet, type(runningCountSet))
        # sys.exit()
        time.sleep(random.uniform(0.3, 0.5))

        # ===== 5.生成顶层的两个文件夹：allResult 和 projectResult
        Logger.ulogger.fusion_log('Folder structure preparing...', level=Logger.U_INFO)
        folder_running_system = auto_runner.test_base_folder_system_construct(workSpacePath)
        project_folder = folder_running_system.project_result
        Logger.ulogger.fusion_log('Folder structure built', level=Logger.U_INFO)

        # ===== 6. out 文件查找与展示
        time.sleep(0.1)
        Logger.ulogger.fusion_log('Indexing...', level=Logger.U_INFO)
        time.sleep(random.uniform(0.2, 0.5))
        find_file_list, run_file_list, run_json = auto_runner.test_json_construct(
            runner_config.workspace_prj_dir, runner_config.runningset_typeset,
            RootManage.root_manager.json_path, save_flg=False)
        _index_inf = '\n\t'.join(map(lambda fie: '{} - {}'.format(*fie), enumerate(find_file_list, start=1)))
        Logger.ulogger.fusion_log(
            _index_inf, level=Logger.U_DEBUG, formatter='\t{}'.format(Logger.ulogger.fmt_message))
        Logger.ulogger.fusion_log('Indexing completes', level=Logger.U_INFO)
        time.sleep(0.1)

        # ===== 7.运行区间模拟截取(已在初始化中完成)
        time.sleep(0.1)
        Logger.ulogger.fusion_log('Reindexing...', level=Logger.U_INFO)
        time.sleep(random.uniform(0.5, 1.2))
        Logger.ulogger.fusion_log('Reindexing completes', level=Logger.U_INFO)
        time.sleep(random.uniform(0.3, 0.5))

        # ===== 8.Travel 和 Special 运行模式展示
        _output_inf = 'Total projects amount to run: {}'.format(len(run_file_list))
        Logger.ulogger.fusion_log(
            _output_inf, level=Logger.U_INFO, formatter='\n{}'.format(Logger.ulogger.fmt_time_a_msg))
        time.sleep(0.1)
        runningTypeSet = runner_config.runningset_typeset
        _running_start = eval(runningTypeSet['StartPro']) if runningTypeSet['RunningType'] == 'Special' else 1
        _running_end = len(run_file_list) + _running_start - 1
        _output_inf = 'Running Mode: {}({}, {}) - {}'.format(
            runningTypeSet['RunningType'], _running_start, _running_end, runningModeStr)
        Logger.ulogger.fusion_log(_output_inf, level=Logger.U_INFO)
        time.sleep(random.uniform(0.3, 0.5))

        # ===== 9.初始化测试类
        TestUnitFrame = suitetest.suite.TestBaseSuite(workSpacePath, testModule, test_title=runningModeStr)

        # ===== 10.根据执行次数进行循环遍历
        for runCount in range(runningCountSet):
            # 运行后自动生成报告
            runCount += 1
            _output_inf = 'Running in round {}'.format(runCount)
            Logger.ulogger.fusion_log(
                _output_inf, level=Logger.U_INFO, formatter='\n{}'.format(Logger.ulogger.fmt_time_a_msg))
            TestUnitFrame.connect_suite(project_folder)
            Logger.ulogger.fusion_log('Saving result files for round {}'.format(runCount), level=Logger.U_INFO)
            folder_running_system.folder_run_count_save(runCount)
            time.sleep(random.uniform(0.5, 1.2))
            # sys.exit()
    except UserException.LicenseVerifyError as le:
        _err_inf = 'Licenses verify failed'
        # Logger.ulogger.fusion_log('错误详情: {}'.format(le), level=Logger.U_CRITICAL)
        Logger.ulogger.fusion_log(_err_inf, level=Logger.U_CRITICAL)
        # Exit.Exit.exit_on_f_in(_err_inf)
    except UserException.TestConnectionError as te:
        _err_inf = '板卡连接测试失败, 请检查运行配置文件是否正确或仿真器是否处于空闲状态'
        # Logger.ulogger.fusion_log('错误详情: {}'.format(te), level=Logger.U_CRITICAL)
        Logger.ulogger.fusion_log(_err_inf, level=Logger.U_CRITICAL)
        # Exit.Exit.exit_on_f_in(_err_inf)
    except PermissionError as pe:
        _err_inf = '请退出所选文件路径，当所指定工作工作空间文件系统相关文件夹处于活动状态时无法操作'
        # Logger.ulogger.fusion_log('错误详情: {}'.format(pe), level=Logger.U_CRITICAL)
        Logger.ulogger.fusion_log(_err_inf, level=Logger.U_CRITICAL)
        # Exit.Exit.exit_on_f_in(_err_inf)
    except Exception as ree:
        # print(traceback.format_exc())
        _err_inf = '流程错误，请结合日志分析'
        Logger.ulogger.fusion_log('错误详情: {}'.format(ree), level=Logger.U_CRITICAL)
        Logger.ulogger.fusion_log(_err_inf, level=Logger.U_CRITICAL)
        # Exit.Exit.exit_on_f_in(_err_inf)
    else:
        # ===== 11.保存
        Logger.ulogger.fusion_log('All test complete, saving result files...', level=Logger.U_INFO,
                                  formatter='\n{}'.format(Logger.ulogger.fmt_time_a_msg))
        folder_running_system.folder_all_save()
        time.sleep(random.uniform(0.1, 0.2))
    finally:
        # ===== 12.清理操作
        Logger.ulogger.fusion_log('Cleaning files...', level=Logger.U_INFO,
                                  formatter='\n{}'.format(Logger.ulogger.fmt_time_a_msg))
        if tool_debug_mode != 'DEBUG':
            os.remove(RootManage.root_manager.json_path)
        time.sleep(random.uniform(0.1, 0.2))

        Logger.ulogger.fusion_log('All Done', level=Logger.U_INFO)
        time.sleep(random.uniform(0.1, 0.2))
        Logger.ulogger.file_logger.file_text_log(
            Logger.ulogger.spacer, level=Logger.U_INFO, formatter=Logger.ulogger.fmt_message)
        Exit.Exit.exit_on_output()
