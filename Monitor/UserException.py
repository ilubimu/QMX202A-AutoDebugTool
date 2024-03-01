# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: UserException.py.                                                    *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

class TestConnectionError(Exception):
    """ CCS connection test exception """

    def __init__(self, *args, **kwargs):
        pass


class LicenseVerifyError(Exception):
    """ Licenses verify exception """

    def __init__(self, *args, **kwargs):
        pass


class LicenseFormatError(Exception):
    """ Licenses format exception """

    def __init__(self, *args, **kwargs):
        pass


class RunningModeError(Exception):
    """ Running mode select exception """

    def __init__(self, *args, **kwargs):
        pass


class JsCreationError(Exception):
    """ JS file build exception """

    def __init__(self, *args, **kwargs):
        pass


class JsonCreationError(Exception):
    """ Running json file construction exception """

    def __init__(self, *args, **kwargs):
        pass


class MemDatError(Exception):
    """ Memory export data file match exception """

    def __init__(self, *args, **kwargs):
        pass


class XmlDatError(Exception):
    """ XML result file analysis exception """

    def __init__(self, *args, **kwargs):
        pass
