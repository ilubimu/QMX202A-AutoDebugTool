# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: DssRhino.py.                                                         *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

import Logger
import os.path
import subprocess


class CallDssRhino:
    def __init__(self, dssbat_path):
        self.dssbat_path = dssbat_path

    def dss_call_debug(self, js_file):
        dss_cmd = (r"call {} -dss.debug {}".format(self.dssbat_path, js_file))
        Logger.ulogger.fusion_log(dss_cmd, level=Logger.Logger.logging.DEBUG)
        subprocess.getoutput(dss_cmd)
        runtime_flagpath = os.path.split(js_file)[0]
        runtime_flag = open(r"{}\flag.txt".format(runtime_flagpath), 'w+')
        runtime_flag.close()
        # subprocess.run(dss_cmd)
        return runtime_flagpath

    def dss_call(self, js_file):
        dss_cmd = (r"call {} {}".format(self.dssbat_path, js_file))
        Logger.ulogger.fusion_log(dss_cmd, level=Logger.Logger.logging.DEBUG)
        subprocess.getoutput(dss_cmd)
        # subprocess.run(dss_cmd)
        runtime_flag_path = os.path.split(js_file)[0]
        runtime_flag = r"{}\flag.flg".format(runtime_flag_path)
        with open(runtime_flag, 'w') as f:
            # print(f.read())
            pass
        # subprocess.run(dss_cmd)
        return runtime_flag
