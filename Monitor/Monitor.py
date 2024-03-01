# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: Monitor.py.                                                          *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

import collections
import functools
import inspect
import shutil

import Logger
import Monitor
import os.path
import random
import time
import unittest

from Libs import Exit, Env


class ExceptionMonitor:
    def __init__(self):
        pass

    # def check_config_input(self, check_func):
    #     """ Config 文件读取错误处理 """
    #     @functools.wraps(check_func)
    #     def wrap_the_func(*args, **kwargs):
    #         try:
    #             return_result = check_func(*args, **kwargs)
    #             # print("Check Success")
    #         except Exception as e:
    #             return_result = []
    #             print(str(e))
    #             print("配置文件格式出错")
    #             input('Please press enter key to exit ...')
    #             sys.exit()
    #         return return_result
    #     return wrap_the_func

    @staticmethod
    def check_config_input(func):
        """ Config 文件读取错误处理 """

        @functools.wraps(func)
        def wrap_the_func(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
                # print("Check Success")
            except Exception as e:
                Logger.ulogger.terminal_logger.terminal_text_log('错误详情是: {}'.format(
                    e), level=Logger.U_CRITICAL)
                Logger.ulogger.terminal_logger.terminal_text_log('错误函数是: {}'.format(
                    func.__name__), level=Logger.U_CRITICAL)
                Exit.Exit.exit_on_f_in('配置文件格式出错')

        return wrap_the_func

    @staticmethod
    def check_file_split(func):
        """ 路径拆分文件名后的重复性检查 """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                _base_list, _name_list = func(self, *args, **kwargs)
                if len(_name_list) != len(set(_name_list)):
                    Logger.ulogger.terminal_logger.terminal_text_log(
                        list((collections.Counter(_name_list) - collections.Counter(set(_name_list))).elements()),
                        level=Logger.U_CRITICAL)
                    raise Exception("存在同名 out 文件")
            except Exception as e:
                Logger.ulogger.terminal_logger.terminal_text_log('错误详情是: {}'.format(
                    e), level=Logger.U_CRITICAL)
                Logger.ulogger.terminal_logger.terminal_text_log('错误函数是: {}'.format(
                    func.__name__), level=Logger.U_CRITICAL)
                # 退出
                Exit.Exit.exit_on_f_in('依赖构建环境异常')
            else:
                return _base_list, _name_list

        return wrapper

    @staticmethod
    def check_xml_status(func):
        """ 运行状态 xml 文件检查 """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            _xml_status, _xml_extrac_path = False, None
            try:
                _xml_status, _xml_extrac_path = func(self, *args, **kwargs)
                if not _xml_status:
                    raise Monitor.UserException.XmlDatError("Program test run result error, please check")
            except Exception as e:
                Logger.ulogger.fusion_log('错误详情是: {}'.format(
                    e), level=Logger.U_CRITICAL)
                Logger.ulogger.fusion_log('错误函数是: {}'.format(
                    func.__name__), level=Logger.U_CRITICAL)
                time.sleep(random.uniform(0.2, 0.4))
                # raise Monitor.UserException.XmlDatError(e)    # 不触发异常，保证流程性
            # else:
            #     return _xml_status, _xml_extrac_path
            finally:
                return _xml_status, _xml_extrac_path

        return wrapper

    @staticmethod
    def check_memory_status(func):
        """ 运行导出结果 memory 文件检查 """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            _memory_status = False
            try:
                _memory_status = func(self, *args, **kwargs)
                if not _memory_status:
                    raise Monitor.UserException.MemDatError("Program export data file error, please check")
            except Exception as e:
                Logger.ulogger.fusion_log('错误详情是: {}'.format(
                    e), level=Logger.U_CRITICAL)
                Logger.ulogger.fusion_log('错误函数是: {}'.format(
                    func.__name__), level=Logger.U_CRITICAL)
                time.sleep(random.uniform(0.2, 0.4))
                # raise Monitor.UserException.MemDatError(e)    # 不触发异常，保证流程性
            # else:
            #     return _memory_status
            finally:
                return _memory_status

        return wrapper

    @staticmethod
    def check_js_file_create(func):
        """ js 文件或 json 文件构建错误处理(文件存在性) """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return_result = func(self, *args, **kwargs)
                if not os.path.exists(return_result):
                    raise FileNotFoundError("JS running file not found")
            except Exception as e:
                Logger.ulogger.fusion_log('错误详情是: {}'.format(
                    e), level=Logger.U_CRITICAL)
                Logger.ulogger.fusion_log('错误函数是: {}'.format(
                    func.__name__), level=Logger.U_CRITICAL)
                time.sleep(random.uniform(0.2, 0.4))
                raise Monitor.UserException.JsCreationError
            else:
                return return_result

        return wrapper

    @staticmethod
    def check_main_test_function(workspace_prj, running_typeset, json_init_path, save_flg=True):
        # 构建初始化 json
        try:
            Logger.ulogger.fusion_log('Scanning...\n', level=Logger.U_INFO)
            Env.EnvInit().test_json_construct(workspace_prj, running_typeset, json_init_path, save_flg)
        except Exception as ie:
            Logger.ulogger.fusion_log('错误详情是: {}'.format(ie), level=Logger.U_CRITICAL)
            # 退出
            # raise UserException.JsonCreationError('依赖构建环境异常')
            if os.path.exists(json_init_path):
                os.remove(json_init_path)
            Exit.Exit.exit_on_f_in('环境依赖构建异常')
        """ 单次运行实时错误监测 """

        def check_main_test(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                sig = inspect.signature(func).parameters
                msg_head = 'msg'
                msg = sig.get(msg_head).default if msg_head in sig.keys() else '执行异常'
                msg = kwargs.get(msg_head) if msg_head in kwargs.keys() else msg
                try:
                    return func(self, *args, **kwargs)
                except AssertionError as ae:  # 断言出错
                    Logger.ulogger.fusion_log('错误详情是: {}(执行状态错误)'.format(
                        ae), level=Logger.U_CRITICAL)
                    Logger.ulogger.fusion_log('错误函数是: {}'.format(
                        func.__name__), level=Logger.Logger.logging.CRITICAL)
                    # 断言补充
                    unittest.TestCase().assertTrue(False, msg=msg)
                except Exception as e:  # 其他错误
                    Logger.ulogger.fusion_log('错误详情是: {}(执行流程错误)'.format(
                        e), level=Logger.U_CRITICAL)
                    Logger.ulogger.fusion_log('错误函数是: {}'.format(
                        func.__name__), level=Logger.U_CRITICAL)
                    # 断言补充
                    unittest.TestCase().assertTrue(False, msg=msg)
                    # raise e

            return wrapper

        return check_main_test

    # @staticmethod
    # def check_main_test_function(func):
    #     """ 单次运行实时错误监测 """
    #     Env.EnvInit().test_json_construct()    # 构建初始化 json 运行文件
    #
    #     @functools.wraps(func)
    #     def wrapper(self, *args, **kwargs):
    #         sig = inspect.signature(func).parameters
    #         msg_head = 'msg'
    #         msg = sig.get(msg_head).default if msg_head in sig.keys() else '执行异常'
    #         msg = kwargs.get(msg_head) if msg_head in kwargs.keys() else msg
    #         try:
    #             return func(self, *args, **kwargs)
    #         except AssertionError as e:    # 断言出错，不做其他处理
    #             Logger.ulogger.fusion_log('错误详情是: {}'.format(
    #                 e), level=Logger.U_CRITICAL)
    #             Logger.ulogger.fusion_log('错误函数是: {}'.format(
    #                 func.__name__), level=Logger.U_CRITICAL)
    #         except Exception as e:    # 其他错误，补充断言判断
    #             Logger.ulogger.fusion_log('错误详情是: {}'.format(
    #                 e), level=Logger.U_CRITICAL)
    #             Logger.ulogger.fusion_log('错误函数是: {}'.format(
    #                 func.__name__), level=Logger.U_CRITICAL)
    #             # 断言补充
    #             unittest.TestCase().assertTrue(False, msg=msg)
    #             # raise e
    #     return wrapper

    @staticmethod
    def check_reportor(func):
        """ 测试结果统计生成错误监测 """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                Logger.ulogger.fusion_log('错误详情是: {}'.format(
                    e), level=Logger.U_CRITICAL)
                Logger.ulogger.fusion_log('错误函数是: {}'.format(
                    func.__name__), level=Logger.U_CRITICAL)
                # raise e

        return wrapper

    @staticmethod
    def check_file_found(func):
        """ 测试结果统计生成错误监测 """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                Logger.ulogger.fusion_log('错误详情是: {}'.format(
                    e), level=Logger.U_CRITICAL)
                Logger.ulogger.fusion_log('错误函数是: {}'.format(
                    func.__name__), level=Logger.U_CRITICAL)
                # raise e

        return wrapper

    @staticmethod
    def check_connection_test(func):
        """ CCS 连接测试错误监测 """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            _tempdir = None
            try:
                status, _tempdir = func(self, *args, **kwargs)
                if not status:
                    raise Exception("ERROR: CCS connection test error")
            except Exception as e:
                # Logger.ulogger.fusion_log('错误详情是: {}'.format(
                #     e), level=Logger.U_CRITICAL)
                # Logger.ulogger.fusion_log('错误函数是: {}'.format(
                #     func.__name__), level=Logger.U_CRITICAL)
                # Exit.Exit.exit_on_f_in('板卡连接测试失败，请检查运行配置文件是否正确或仿真器是否处于空闲状态')
                Logger.ulogger.fusion_log('板卡连接测试失败，请检查运行配置文件是否正确或仿真器是否处于空闲状态',
                                          level=Logger.U_CRITICAL)
                raise Monitor.UserException.TestConnectionError('板卡连接测试失败')
            else:
                return status
            finally:
                if os.path.exists(_tempdir):
                    shutil.rmtree(_tempdir)

        return wrapper
