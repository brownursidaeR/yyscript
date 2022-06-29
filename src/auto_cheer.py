#!/usr/bin/python
# -*- coding: utf-8 -*

# %% 先加载对应的库
import os
import sys
import time
import logging
from random import randint, uniform

if __name__ == "__main__":
    cur_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
    sys.path.append(os.path.join(cur_dir, 'autogui'))
    sys.path.append(os.path.join(cur_dir, 'conf'))
logger = logging.getLogger('kiddo')

from autogui import Autogui, ImageCallback


class Cheer(Autogui):
    def __init__(self, win_name='阴阳师-网易游戏', yys_config=None):
        Autogui.__init__(self, win_name, yys_config)
        # 设置当前副本的类型，设置之后优先查找御灵对应的截图
        self.screenshot.set_current_setion('cheer')  # 设置优先的截图信息
        self.config.set_current_setion('cheer')  # 设置当前配置信息
        self.pre_loop_times = self.config.cur_config.get('pre_loop_times', 20)
        self.loop_times = self.config.cur_config.get('loop_times', 400)

        prepare_callback = []
        loop_callback = [
            ('yes', self.click_loc_one),  # 确认
            ('task_accept', self.task_accept_callback),
            ('wait_leader', self.wait_leader_callback),  # 等待馆主
            ('closing', self.closing_callback),  # 道馆结束
            ('victory', self.victory_callback),
            ('fail', self.fail_callback),
            ('continue', self.continue_callback),  # 3,6,9时用到
            ('cheer_on', self.cheer_on_callback),  # 助威
            ('cheer_off', self.cheer_off_callback),  # 助威冷却
            ('forward', self.cheer_on_callback),  # 前往，点击后进入助威界面
            ('report', self.report_callback),  # 前往，点击后进入助威界面
        ]

        self.init_image_callback(prepare_callback, loop_callback)

    def cheer_on_callback(self, loc):
        # 助威点击之后可以休眠久一点
        self.click_loc_one_and_move_uncover(loc)
        time.sleep(5)

    def cheer_off_callback(self, loc):
        # 助威冷却时休眠5s
        self.display_msg('冷却时休眠5s...')
        time.sleep(5)

    def wait_leader_callback(self, loc):
        # 助威冷却时休眠5s
        self.display_msg('等待馆主休眠5s...')
        time.sleep(5)

    def closing_callback(self, loc):
        # 助威冷却时休眠2s
        self.display_msg('道馆已经结束！正在退出...')
        self.stop = True

    def report_callback(self, loc):
        self.click_loc_one_and_move_uncover(loc)
        time.sleep(5)
        loc_tmp = self.locate_im(self.get_image('forward'))
        if loc_tmp:
            self.cur_key = 'forward'
            self.click_loc_one_and_move_uncover(loc_tmp)
            self.display_msg('进入观战界面')
        else:
            self.display_msg('暂时没有可观战的寮友，等待5秒')
            self.click_safely_loc(loc)
            time.sleep(5)


if __name__ == '__main__':
    autogui = Cheer()
    autogui.run('cheer')
    logger.debug(str(autogui.prepare_image_callback))
    logger.debug(str(autogui.loop_image_callback))
