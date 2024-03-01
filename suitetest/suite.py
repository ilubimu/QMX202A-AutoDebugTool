# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: suite.py.                                                            *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

import datetime
import Monitor
import unittest

from BeautifulReport import BeautifulReport


class TestBaseSuite:
    def __init__(self, workspace, module_cls, test_title='测试'):
        self.workspace = workspace
        self.module_cls = module_cls
        self.test_title = test_title

    def loader_suite(self):
        """
        加载Loader至Suite中，传递参数Suite
        :param self:None
        :return:参数Suite
        """
        suite_test2 = unittest.TestSuite()
        loader = unittest.TestLoader()
        # 加载的是一个测试类
        name = loader.loadTestsFromTestCase(self.module_cls)
        # name = loader.loadTestsFromName(self.module)
        # 也可以传递单个Loader给Runner，跳过Suite进行运行。
        suite_test2.addTest(name)
        return suite_test2

    def runner_report(self, suite_name, project_result):
        # test_report_path = r"{}\report".format(self.workspace)
        test_report_path = project_result
        now_time = datetime.datetime.now().strftime('%Y%m%d.%H%M%S')
        test_report_name = '测试报告.' + str(now_time)
        result = BeautifulReport(suite_name)
        result.report(description=self.test_title, filename=test_report_name,
                      report_dir=test_report_path, theme='theme_default')
        return 0

    @Monitor.Monitor.ExceptionMonitor.check_reportor
    def connect_suite(self, project_result):
        suite = self.loader_suite()
        # print(suite)
        # exit(0)
        self.runner_report(suite, project_result)
        return 0
