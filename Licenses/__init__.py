# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: __init__.py.                                                         *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

from Licenses import Current

__license_expires = 20250101000000  # 年月日时分秒


def licenses_verify():
    # return Current.Current().runtime_env_ensure(__license_expires, network=False, licenses=False)
    return Current.Current().runtime_env_ensure(__license_expires)
