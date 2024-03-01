# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: FileOpt.py.                                                          *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

import os.path

prefix_indent = 4


class FileAnalysis:
    def __init__(self):
        pass

    @staticmethod
    def file_split(filepath_list, prefix_index=1):
        """
        拆分指定的路径列表为基路径和文件名
        Args:
            filepath_list: 待拆分文件路径列表
            prefix_index: 起始标号

        Returns: _base_path_list, _name_list

        """
        _base_path_list, _name_list = [], []
        for _index, _filepath in enumerate(filepath_list, start=prefix_index):
            _base_path, _name = os.path.split(_filepath)
            _base_path_list.append(_base_path)
            _name_list.append('A{}_{}'.format(str(_index).zfill(prefix_indent), _name))  # 添加区分符，避免键重复
        return _base_path_list, _name_list

    @staticmethod
    def find_extension_file(find_path, filename_extension='.out'):
        """
        索引一个路径下的某个后缀名，返回根据查找到的所有文件的路径组成的列表
        :param find_path:索引路径
        :param filename_extension:需要索引的文件拓展名
        :return: 返回索引路径下带文件拓展名文件路径的列表
        """
        list_pro_path = []
        for root, dirs, names in os.walk(find_path):
            for name in names:
                if os.path.splitext(name)[1] == filename_extension:
                    pro_name = os.path.join(root, name)
                    list_pro_path.append(pro_name)
        return list_pro_path

    # @Monitor.ExceptionMonitor.check_file_split
    # def file_split(self, filepath_list):
    #     """
    #     拆分指定的路径列表为基路径和文件名
    #     Args:
    #         filepath_list: 待拆分文件路径列表
    #
    #     Returns: _base_path_list, _name_list
    #
    #     """
    #     _base_path_list, _name_list = [], []
    #     for _filepath in filepath_list:
    #         _base_path, _name = os.path.split(_filepath)
    #         _base_path_list.append(_base_path)
    #         _name_list.append(_name)
    #     """添加拆分后的重复性检查，添加区分标签？"""
    #     return _base_path_list, _name_list

    # @Monitor.ExceptionMonitor.check_file_found
    # def find_extension_file(self, find_path, filename_extension='.out'):
    #     """
    #     索引一个路径下的某个后缀名，返回根据查找到的所有文件的路径组成的列表
    #     :param find_path:索引路径
    #     :param filename_extension:需要索引的文件拓展名
    #     :return: 返回索引路径下带文件拓展名文件路径的列表
    #     """
    #     list_pro_path = []
    #     for root, dirs, names in os.walk(find_path):
    #         for name in names:
    #             if os.path.splitext(name)[1] == filename_extension:
    #                 pro_name = os.path.join(root, name)
    #                 list_pro_path.append(pro_name)
    #     return list_pro_path
