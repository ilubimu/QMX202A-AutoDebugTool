# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: Env.py.                                                              *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

import json
import Logger
import Opt
import random
import time


class EnvInit:
    def __init__(self):
        self.file_opt = Opt.FileOpt.FileAnalysis()

    def test_json_construct(self, workspace_prj, running_typeset, save_json, save_flg=True):
        """
        查找到 out 文件路径并编排成字典存放到 json 文件中
        """
        Logger.ulogger.fusion_log('Searching path: {}'.format(workspace_prj), level=Logger.U_DEBUG)
        __find_file_list = self.file_opt.find_extension_file(workspace_prj, ".out")

        _running_type = running_typeset['RunningType']
        if _running_type == 'Travel':
            _running_out_list = __find_file_list[:]
        elif _running_type == 'Special':
            _running_out_list = __find_file_list[int(running_typeset['StartPro']) - 1:int(running_typeset['EndPro'])]
        else:
            _running_out_list = []
            _warn_info = 'Please enter right config [RunningMode]-runningtypeset-RunningType param: Travel/Special'
            Logger.ulogger.fusion_log(_warn_info, level=Logger.U_WARNING)
            # Exit.Exit.exit_on_output()

        _, _list_out_index_name = self.file_opt.file_split(
            _running_out_list, prefix_index=int(running_typeset['StartPro']) if _running_type == 'Special' else 1)
        _find_file_dict = dict(zip(_list_out_index_name, _running_out_list))
        if save_flg:
            with open(save_json, "w+", encoding='utf8') as jf:
                jf.write(json.dumps(_find_file_dict, ensure_ascii=False, indent=4))
        Logger.ulogger.fusion_log('Status: {} - {}'.format(save_json, save_flg), level=Logger.U_DEBUG)
        return __find_file_list, _running_out_list, save_json

    @staticmethod
    def test_base_folder_system_construct(work_space_path):
        _folder_init = Opt.FolderOpt.FolderSystem(work_space_path)
        _folder_init.folder_all_result_create()
        _folder_init.folder_project_result_create()
        # _project_folder = _folder_init.project_result
        time.sleep(random.uniform(0.2, 0.5))
        return _folder_init
