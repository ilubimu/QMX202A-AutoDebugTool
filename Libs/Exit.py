# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: Exit.py.                                                             *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

import Logger
import msvcrt
import sys


class Exit:
    @staticmethod
    def exit_on_output(out_put_info=""):
        Logger.ulogger.terminal_logger.terminal_text_log(
            out_put_info, level=Logger.Logger.logging.INFO, formatter='%(message)s')
        Logger.ulogger.terminal_logger.terminal_text_log(
            "Please press any key to exit...", level=Logger.Logger.logging.INFO, formatter='%(message)s')
        ord(msvcrt.getch())
        sys.exit()

    @staticmethod
    def exit_on_f_in(out_put_message=""):
        """
        only exit with 'F' in
        """
        Logger.ulogger.terminal_logger.terminal_text_log(
            out_put_message, level=Logger.Logger.logging.INFO, formatter='%(message)s')
        Logger.ulogger.terminal_logger.terminal_text_log(
            "Please press 'F' to exit...", level=Logger.Logger.logging.INFO, formatter='%(message)s')
        while True:
            if ord(msvcrt.getch()) in [102, 70]:
                sys.exit()
