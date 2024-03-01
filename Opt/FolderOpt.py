# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: FolderOpt.py.                                                        *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

import datetime
import Logger
import os.path
import shutil


class FolderSystem:
    def __init__(self, works_pace):
        self.workspace = works_pace
        self.running_result = r"{}\RunningResult".format(works_pace)
        self.project_result = r"{}\ProjectResult".format(works_pace)
        self.all_result = r"{}\AllResultSave".format(works_pace)
        self.folder_structure = ["CIO", "Memory", "XML", "JsScript", "ResultAddressData"]

    def folder_all_result_create(self):
        if os.path.exists(self.all_result):
            local_time = datetime.datetime.now()
            time_style = local_time.strftime("%Y%m%d(%H-%M-%S)")
            os.rename(self.all_result, '{}.{}.old'.format(self.all_result, time_style))
        os.makedirs(self.all_result)

    def folder_project_result_create(self):
        if os.path.exists(self.project_result):
            local_time = datetime.datetime.now()
            time_style = local_time.strftime("%Y%m%d(%H-%M-%S)")
            os.rename(self.project_result, '{}.{}.old'.format(self.project_result, time_style))
        os.makedirs(self.project_result)

    def folder_project_save(self, pro_name, runtime_clean=False):
        """
        程序运行完成后结果的保存
        :param pro_name:
        :param runtime_clean:
        :return:
        """
        save_first_folder = r"{0}\{1}".format(self.project_result, pro_name)
        if not os.path.exists(self.project_result):
            os.makedirs(self.project_result)
        shutil.move(self.running_result, save_first_folder)
        Logger.ulogger.fusion_log('Saving: {}'.format(save_first_folder), level=Logger.Logger.logging.DEBUG)

        if runtime_clean:
            Logger.ulogger.fusion_log('Cleaning: {}'.format(save_first_folder), level=Logger.Logger.logging.DEBUG)
            _clean_list = self.folder_structure[2:]
            for _clean_name in _clean_list:
                shutil.rmtree(os.path.join(save_first_folder, _clean_name), ignore_errors=True)
        # 待优化文件夹改名
        return 0

    def folder_project_multi_save(self, first_dir_name, sub_dir_name):
        """
        程序运行完成后结果的保存
        :param sub_dir_name:
        :param first_dir_name:
        :return:
        """
        save_first_folder = r"{0}\{1}".format(self.project_result, first_dir_name)
        save_result_folder = r"{0}\{1}".format(save_first_folder, sub_dir_name)
        if not os.path.exists(save_first_folder):
            os.makedirs(save_first_folder)
        if os.path.exists(save_result_folder):
            shutil.rmtree(save_result_folder)
        shutil.move(self.running_result, save_result_folder)
        # 待优化文件夹改名
        # return 0
        return save_result_folder

    def folder_all_save(self):
        local_time = datetime.datetime.now()
        time_style = local_time.strftime("%Y%m%d(%H-%M-%S)")
        all_result_path = '{}.{}'.format(self.all_result, time_style)
        shutil.move(self.all_result, all_result_path)
        return 0

    def folder_run_count_save(self, run_count):
        local_time = datetime.datetime.now()
        time_style = local_time.strftime("%Y%m%d(%H-%M-%S)")
        run_count_path = r"{}\Cnt.{}.{}".format(self.all_result, run_count, time_style)
        shutil.move(self.project_result, r"{}".format(run_count_path))
        return 0

    def folder_tree_create(self):
        file_path_list = []
        for name in self.folder_structure:
            makedir = r"{}\{}".format(self.running_result, name)
            if os.path.exists(makedir):
                shutil.rmtree(makedir)
            os.makedirs(makedir)
            file_path_list.append(makedir.replace('\\', '/'))
        return file_path_list

    # def folder_tree_create_test(self):
    #     """
    #     测试函数：此函数不会创建文件夹只是构建文件路径
    #     :return:返回一个文件路径
    #     """
    #     file_path_list = []
    #     folder_name = ["XML", "CIO", "Memory", "JsScript"]
    #     for name in folder_name:
    #         makedir = r"{}\{}".format(self.running_result, name)
    #         # os.makedirs(makedir)
    #         # try:
    #         #     os.makedirs(makedir)
    #         # except Exception as error:
    #         #     print(str(error))
    #         #     print("已有当前文件夹")
    #         #     exit()
    #         file_path_list.append(makedir)
    #     return file_path_list

    @staticmethod
    def runtime_result(folder_list):
        """
        文件构建，将后续结果需要的文件事先构建好其字符路径。
        :return:返回一个包含xml_path，cio_file，memory_file，js_file四个路径的字符串的列表
        """
        result_list = []
        cio_file = r"{}\CIOFile.txt".format(folder_list[0]).replace("\\", "/")
        memory_file = r"{}\MemoryFile.dat".format(folder_list[1]).replace("\\", "/")
        xml_file = r"{}\XML.xml".format(folder_list[2]).replace("\\", "/")
        js_file = r"{}\FirstVersion.js".format(folder_list[3]).replace("\\", "/")
        running_data_path = r"{}\Date.txt".format(folder_list[4]).replace("\\", "/")
        result_list.append(cio_file)
        result_list.append(memory_file)
        result_list.append(xml_file)
        result_list.append(js_file)
        result_list.append(running_data_path)
        return result_list

    def connect_folder_func(self):
        """
        链接文件功能的函数，组合使用的方式
        :return:返回一个列表
        """
        folder_tree_list = self.folder_tree_create()
        result_tree_list = self.runtime_result(folder_tree_list)
        # print(result_tree_list)
        return result_tree_list
