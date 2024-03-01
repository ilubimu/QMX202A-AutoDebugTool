# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: setup.py.                                                            *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

import os
import shutil
from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize(
    [r'./Config/*.py',
     r'./JsCreator/*.py',
     r'Libs/*.py',
     r'./Licenses/*.py',
     r'./Logger/*.py',
     r'./Monitor/*.py',
     r'./Opt/*.py',
     r'./RootManage/*.py',
     r'./suitetest/*.py'
     ]),
    )

# Cleanup the temporary files and directories
shutil.rmtree('build')
for filename in os.listdir():
    if filename.endswith('.c'):
        os.remove(filename)

# Rename the output file
for filename in os.listdir():
    if filename.endswith('.pyd'):
        os.rename(filename, filename.replace('.cp311-win_amd64', ''))
