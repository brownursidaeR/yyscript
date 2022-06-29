# -*- coding: utf-8 -*-
'''
    环境自动配置文档
    1. 请确保可以连得上网
'''

import os
import logging

logger = logging.getLogger('kiddo')
logger.setLevel(logging.DEBUG)
BASIC_FORMAT = '%(asctime)s - %(levelname)s: %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
chlr = logging.StreamHandler()  # 输出到控制台的handler
chlr.setFormatter(formatter)
logger.addHandler(chlr)

'库名称，检查的关键字，部分库关键字跟库名不一致'
req_libs = [
    ['pyinstall', 'pyinstall'],
    ['pywin32', 'pywin32'],
    ['pyautogui', 'autogui'],
    ['numpy', 'numpy'],
    ['opencv-python', 'opencv-python'],
    ['opencv-contrib-python', 'opencv-contrib-python'],
    ['pyqt5', 'pyqt5'],
    ['pyqt5-tools', 'pyqt5-tools'],
]

pip_install_format = 'pip install {0}'
pip_list_format = 'pip list | grep {0}'


def do_shell_command(command):
    res = os.popen(command).readlines()
    return res


def check_lib(check_lib):
    lib_name = check_lib[0]
    lib_check_name = check_lib[1]

    res = do_shell_command(pip_list_format.format(lib_check_name))
    if len(res) > 0 and lib_check_name in res[0]:
        logger.debug('{} already installed'.format(lib_name))
        return True
    else:
        logger.debug('install {}'.format(lib_name))
        do_shell_command(pip_install_format.format(lib_name))

    return False


if __name__ == '__main__':
    for cur_lib in req_libs:
        check_lib(cur_lib)
