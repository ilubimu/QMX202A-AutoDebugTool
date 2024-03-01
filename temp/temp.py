# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: temp.py.                                                             *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

import collections
import copy
import os.path
import shutil
import socket
import unittest
import inspect
import traceback
import subprocess
from typing import Optional

import requests
import time
import random
import tempfile

from functools import wraps

list1 = ['1', '2', '3', '4', '5', '6', '7', '8', '8', '9', '10']
list2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
print(list((collections.Counter(list1) - collections.Counter(list2)).elements()))

memorydata = [{'Name': 'M0', 'StartAddress': '0x0000', 'AddressLength': '0x200'},
              {'Name': 'M1', 'StartAddress': '0x0400', 'AddressLength': '0x200'},
              {'Name': 'L0', 'StartAddress': '0x8000', 'AddressLength': '0x800'},
              {'Name': 'L1', 'StartAddress': '0x9000', 'AddressLength': '0x800'},
              {'Name': 'L2', 'StartAddress': '0xA000', 'AddressLength': '0x800'},
              {'Name': 'L3', 'StartAddress': '0xB000', 'AddressLength': '0x800'},
              {'Name': 'L4', 'StartAddress': '0xC000', 'AddressLength': '0x800'},
              {'Name': 'L5', 'StartAddress': '0xD000', 'AddressLength': '0x800'},
              {'Name': 'L6', 'StartAddress': '0xE000', 'AddressLength': '0x800'},
              {'Name': 'L7', 'StartAddress': '0xF000', 'AddressLength': '0x800'}]
t = [x['Name'] for x in memorydata]
print(t)

running_stop_flag = {'RightStop_flag': 'RightStop', 'ErrorStop_flag': 'ErrorStop'}
_breakpoint_add_frame = '''
var {0} = debugSession_0.symbol.getAddress("{1}");
var {2} = {0}.toString(16);
debugSession_0.breakpoint.add("{1}");
'''
right_stop_break = _breakpoint_add_frame.format('Right_Stop_addr', running_stop_flag.pop('RightStop_flag'), 'right_pc')
_other_stop_break = '\n'.join([_breakpoint_add_frame.format(
    '{}_addr'.format(key), value, key) for key, value in running_stop_flag.items()])
print(right_stop_break)
print(_other_stop_break)

memory_result_folder = 'D:\\test'.replace('\\', '/')
memory_save_frame = 'debugSession_0.memory.saveData2( {0}, 0, {1}, "{2}/{3}.dat", 15, false);'
_memory_save_context = '\n'.join([memory_save_frame.format(
    x['StartAddress'], x['AddressLength'], memory_result_folder, x['Name'])
    for x in memorydata])
print(_memory_save_context)

print('\n'.join(map(lambda ie: '{} - {}'.format(*ie),
                    enumerate([r'D:\test1\test1.out', r'D:\test1\test2.out', r'D:\test1\test3.out']))))


class Test:
    pass


print(type(eval('Test')), type(Test))
print(issubclass(eval('Test'), Test))
print(isinstance(eval('Test'), Test))
print(type(Test()).__name__)

dic = {'0': 1, '1': 2, '2': 3}
keys, values = zip(*dic.items())
print(keys, values, keys[values.index(2)])


def check_main_test_function(func):
    """ 单次运行实时错误监测 """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        sig = inspect.signature(func)
        msg_head = 'test_msg'
        msg = sig.parameters.get(msg_head).default if msg_head in sig.parameters.keys() else '执行异常'
        if msg_head in kwargs.keys():
            msg = kwargs.get(msg_head)
        print(sig, sig.parameters)
        # print(sig.parameters.get('test_msg'))
        # for name, param in sig.parameters.items():
        #     print(type(param))
        #     print(name, param.kind, param.default)
        # bound_args = sig.bind(self, *args, **kwargs)
        # print(bound_args)
        # bound_args.apply_defaults()
        # print(tuple(bound_args.arguments.values()))
        try:
            print(msg, type(msg))
            print(args)
            print(kwargs)
            return func(self, *args, **kwargs)
        except AssertionError as e:
            print('错误详情是: {}'.format(e))
            print('错误函数是: {}'.format(func.__name__))
        except Exception as e:
            print('错误详情是: {}'.format(e))
            print('错误函数是: {}'.format(func.__name__))
            unittest.TestCase().assertTrue(False, msg)
            # raise e

    return wrapper


class T:
    @check_main_test_function
    def t(self, out_path, test_msg='执行异常'):
        print(out_path)
        print(self.__class__)
        # raise Exception('error')
        unittest.TestCase().assertTrue(False, msg=test_msg)


T().t('staea', test_msg='异常')
T().t('staea')

json_path = r"TestDDT.json"
print(json_path)
print(*json_path)

print(list1[1 - 1:4])

try:
    raise ValueError
except ValueError:
    print(traceback.format_exc())
    _log_text = '\t*** {} ***\n\t{}'.format(
        '文件名拆分呢异常，请检查拆分操作', '\n\t'.join(traceback.format_exc().split('\n')))
    print(_log_text)

_ping_cmd = 'ping {} -n 1'.format('192.168.2.204')
_ping_ret = subprocess.run(_ping_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(_ping_ret)
# print(os.system(_ping_cmd))

url = 'https://beijing-time.org'
# url = 'https://www.360.cn'
# socket.setdefaulttimeout(20)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}
request_result = requests.get(url=url, headers=headers)

if request_result.status_code == 200:
    net_date = request_result.headers.get('date')
    print(net_date)
    _url_time_str = ' '.join(net_date.split(',')[-1].split(' ')[:-1]).strip()
    print(_url_time_str)
    gmt_timer = time.strptime(_url_time_str, '%d %b %Y %H:%M:%S')
    print(gmt_timer)
    gmt8_timer = time.localtime(int(time.mktime(gmt_timer)) + 8 * 60 * 60)
    print(gmt8_timer)
    gmt8_time_str = time.strftime('%Y%m%d%H%M%S', gmt8_timer)
    print(gmt8_time_str, int(gmt8_time_str))

temp_base = tempfile.gettempdir()
with tempfile.TemporaryDirectory(suffix='_CCS_CONNECTION', prefix='TEST_', dir=temp_base) as tempdir:
    print(tempdir)
# tempdir = tempfile.mkdtemp(suffix='_CCS_CONNECTION', prefix='TEST_', dir=temp_base)
# print(tempdir)
# input('delete:')
# shutil.rmtree(tempdir, ignore_errors=True)

from JsCreator.JsCreator import RunningModeArch

cls = RunningModeArch(-1)
# print(cls)
# time.sleep(1)
print(cls, cls.mode_cls(), cls.mode_name())
from typing import Union
def a(aa: Union[int, None]):
    print(aa)

a(3)
a('ss')
a(None)
