# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: Analysis.py.                                                         *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

import Logger
import Monitor
import os.path
import time

from lxml import etree


class FileAnalysis:
    def __init__(self):
        pass

    @Monitor.Monitor.ExceptionMonitor.check_xml_status
    def xml_result_parsing(self, xml_files_list, extrac_status=True):
        """
        对 CCS 运行生成的 xml 文件进行提取解析，最后写回到指定文件
        :param xml_files_list 源 xml 文件路径列表
        :param extrac_status 提取标记，标记是否需要对提取的信息进行记录
        :return: 操作状态，目标提取路径列表
        """
        start_time = time.perf_counter()
        monitor_status = False
        xml_files_extrac = []
        for xml_src_path in xml_files_list:
            xml_dst_path = os.path.splitext(xml_src_path)[0] + ".data"
            xml_dst_path = xml_dst_path.replace("\\", "/")
            with open(xml_dst_path, 'w', encoding='utf-8') as wf:
                wf.write('')
            for event, elem in etree.iterparse(xml_src_path, tag='message'):
                # print(event)
                # print(elem.text)
                message_text = elem.text
                if "right_stop_pc" in message_text.lower():
                    monitor_status = True
                if extrac_status:
                    with open(xml_dst_path, 'a+', encoding='utf-8') as xaf:
                        xaf.write(message_text + "\n")
                # = 元素清理，释放内存
                elem.clear()
                while elem.getparent() is not None:
                    del elem.getparent()[0]
            end_time = time.perf_counter()
            spend_time = end_time - start_time
            _output = "操作状态: {0}, 结果文件路径: {1}".format(monitor_status, xml_dst_path)
            Logger.ulogger.fusion_log(spend_time, level=Logger.U_DEBUG)
            Logger.ulogger.fusion_log(_output, level=Logger.U_DEBUG)
            xml_files_extrac.append(xml_dst_path)
        return monitor_status, xml_files_extrac

    @Monitor.Monitor.ExceptionMonitor.check_memory_status
    def memory_result_check(self, memory_folder_path, stand_memory_file_list):
        """
        初步分析 memory 文件存在性及 memory 文件格式修订
        :param memory_folder_path: memory 文件保存路径
        :param stand_memory_file_list 标准 memory 文件列表
        :return: memory 文件状态
        """
        start_time = time.perf_counter()
        check_status = False
        memory_file_list = os.listdir(memory_folder_path)
        if sorted(memory_file_list) == sorted(stand_memory_file_list):
            for memory_file in memory_file_list:
                memory_path = os.path.join(memory_folder_path, memory_file)
                # = memory 文件去头
                with open(memory_path, 'r', encoding='utf-8') as rf:
                    rf.readline()
                    text = rf.readlines()
                with open(memory_path, 'w+', encoding='utf-8') as wf:
                    wf.writelines(text)
            check_status = True
        end_time = time.perf_counter()
        spend_time = end_time - start_time
        _output = "操作状态: {0}, 结果文件路径: {1}".format(check_status, memory_folder_path)
        Logger.ulogger.fusion_log(spend_time, level=Logger.U_DEBUG)
        Logger.ulogger.fusion_log(_output, level=Logger.U_DEBUG)
        return check_status
