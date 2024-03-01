# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: Current.py.                                                          *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

import Logger
import Monitor
import random
import requests
import subprocess
import time


class Current:
    def __init__(self):
        pass

    @staticmethod
    def __env_internet_ensure():
        _ping_url_lib = [
            'www.baidu.com'
        ]
        _ping_cmd = 'ping {} -n 1'
        for _ping_url in _ping_url_lib:
            try:
                _ping_ret = subprocess.run(_ping_cmd.format(
                    _ping_url), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if _ping_ret.returncode != 0:
                    Logger.ulogger.fusion_log('请保证有效的网络链接...', level=Logger.U_CRITICAL)
                    return False
                time.sleep(random.uniform(0.2, 1.5))
            except Exception as e:
                time.sleep(random.uniform(0.2, 1.5))
        return True

    @staticmethod
    def __env_time_ensure(expires: int):
        _time_url_lib = [
            'https://beijing-time.org', 'https://www.baidu.com',
            'https://www.taobao.com', 'https://www.360.cn'
        ]
        _headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.105 Safari/537.36'
        }
        _cookies = ''
        for _time_url in _time_url_lib:
            try:
                _request_result = requests.get(url=_time_url, headers=_headers, cookies=_cookies)
                if _request_result.status_code == 200:
                    _net_time = _request_result.headers.get('date')
                    _url_time_str = ' '.join(_net_time.split(',')[-1].split(' ')[:-1]).strip()
                    gmt_timer = time.strptime(_url_time_str, '%d %b %Y %H:%M:%S')
                    gmt8_timer = time.localtime(int(time.mktime(gmt_timer)) + 8 * 60 * 60)  # GMT+8
                    gmt8_time_int = int(time.strftime('%Y%m%d%H%M%S', gmt8_timer))
                    if gmt8_time_int > expires:
                        Logger.ulogger.fusion_log('您的许可证已过期, 请联系管理员...', level=Logger.U_CRITICAL)
                        return False
                    else:
                        return True
            except Exception as e:
                time.sleep(random.uniform(1.2, 2.5))
        Logger.ulogger.fusion_log('运行环境校验失败，请保证有效的网络连接...', level=Logger.U_CRITICAL)
        return False

    def runtime_env_ensure(self, expires: int, network=True, licenses=True):
        if len(str(expires)) < 12:
            _msg = 'expires must contains all the date message(ag: 19000101000000)'
            raise Monitor.UserException.LicenseFormatError(_msg)
            # Exit.Exit.exit_on_f_in(_msg)
        # 网络连接校验
        _net_status = self.__env_internet_ensure() if network else True
        if not _net_status:
            return False
        # 时间许可证校验
        _time_status = self.__env_time_ensure(expires) if licenses else True
        if not _time_status:
            return False
        return True
