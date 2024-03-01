# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: __init__.py.                                                         *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

import RootManage

from Config import Config

running_config = Config.Config()
running_config.read_config(RootManage.root_manager.config_path)
