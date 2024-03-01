# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: Process.py.                                                          *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

import Logger
import Monitor


# Director
class Process:
    def __init__(self, js_file_path):
        self.builder = None
        self.mode = None
        self.js_file_path = js_file_path

    # def execute_mode(self, mode):
    #     print("Step: select mode")
    #     self.mode = mode
    #     return self.mode

    def gen_js_text(self, text):
        with open(self.js_file_path, "w+", encoding="utf-8") as fp:
            fp.write(text)
        return self.js_file_path

    def replace_js_var(self, replace_params_dict):
        with open(self.js_file_path, 'r', encoding='utf8') as rf:
            js_text = rf.read()
        complex_js_text = js_text
        for replace_key, replace_value in replace_params_dict.items():
            complex_js_text = complex_js_text.replace(replace_key, replace_value)
        with open(self.js_file_path, 'w+', encoding='utf8') as wf:
            wf.write(complex_js_text)
        Logger.ulogger.fusion_log('JS file refactoring complete', level=Logger.U_DEBUG)
        return 0

    @Monitor.Monitor.ExceptionMonitor.check_js_file_create
    def construct_building(self, cls, emulator_param_dict, function_param_dict, end_param_dict):
        self.builder = cls()
        emulator_context = self.builder.emulator_init(emulator_param_dict)
        function_context = self.builder.function(function_param_dict)
        end_context = self.builder.end_process(end_param_dict)
        complex_js_text = emulator_context + function_context + end_context
        js_file_path = self.gen_js_text(complex_js_text)
        Logger.ulogger.fusion_log('JS file construct complete', level=Logger.U_DEBUG)
        Logger.ulogger.fusion_log(js_file_path, level=Logger.U_DEBUG)
        return js_file_path

    # Product
    # @property
    # def building(self):
    #     return self.builder
