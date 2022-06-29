#!/usr/bin/python
# -*- coding: utf-8 -*

# %% 先加载对应的库
import os
import sys
import logging
import time

if __name__ == "__main__":
    cur_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
    sys.path.append(os.path.join(cur_dir, 'autogui'))
    sys.path.append(os.path.join(cur_dir, 'conf'))
logger = logging.getLogger('kiddo')

from autogui import Autogui


class Yaoqi(Autogui):
    def __init__(self, win_name='阴阳师-网易游戏', yys_config=None):
        Autogui.__init__(self, win_name, yys_config)
        # 设置当前副本的类型，设置之后优先查找御灵对应的截图
        self.screenshot.set_current_setion('yaoqi')  # 设置优先的截图信息
        self.config.set_current_setion('yaoqi')  # 设置当前配置信息
        self.pre_loop_times = self.config.cur_config.get('pre_loop_times', 20)
        self.loop_times = self.config.cur_config.get('loop_times', 20)
        self.fight_type = self.config.cur_config.get('type', 'rihefang')
        # self.fight_type = self.config.cur_config.get('type', 'jiaotu')

        prepare_callback = [
        ]
        loop_callback = [
            ('task_accept', self.task_accept_callback),
            ('closed_mainwin', self.click_loc_one),  # 展开主界面
            ('cd', self.cd_callback), # 冷却时直接退出
            ('cancel_match', self.waiting_team_callback),  # 取消匹配
            ('waiting_team', self.waiting_team_callback),
            ('build_team', self.click_loc_one_and_move_uncover),
            # 妖气封印界面： 1. 自动匹配，选择挑战类型
            ('yaoqi', self.yaoqi_callback),
            ('team_fight', self.click_loc_one_and_move_uncover),
            ('prepare', self.prepare_callback),
            ('victory', self.victory_callback),
            ('fail', self.fail_callback),
            ('award', self.award_callback),
            ('time', self.void_callback),
        ]

        self.init_image_callback(prepare_callback, loop_callback)

    def waiting_team_callback(self, loc):
        # 取消挑战和匹配中总是匹配不上，很奇怪
        self.display_msg('正在组队中，继续等待5s')
        time.sleep(5)

    def cd_callback(self, loc):
        self.display_msg('CD中,不再进行挑战')
        time.sleep(2)
        self.stop = True

    def yaoqi_callback(self, loc):
        loc_tmp = self.locate_im(self.get_image('auto_match'))
        if loc_tmp:
            # 识别到自动匹配，先切换到当前挑战类型
            self.click_loc_one_and_move_uncover(loc_tmp)
            return

        # 选择挑战的妖怪类型
        im_yys = self.screenshot_exact()
        loc_tmp = self.locate_im(self.get_image(self.fight_type), im_yys)
        if loc_tmp:
            self.display_msg('识别到{0}'.format(self.fight_type))
            self.click_loc_one_and_move_uncover(loc_tmp)
            time.sleep(0.5)  # 等待自动匹配的出现
        else:
            # 以饿鬼或者二口女为基准线，向上拖动距离 280
            loc_egui = self.locate_im(self.get_image('egui'), im_yys)
            loc_erkounv = self.locate_im(self.get_image('erkounv'), im_yys)
            if loc_egui:
                loc_tmp = loc_egui
                self.display_msg('识别到饿鬼')
            elif loc_erkounv:
                loc_tmp = loc_erkounv
                self.display_msg('识别到二口女')
            else:
                self.display_msg('未识别到饿鬼或者二口女')
                return

            # 以匹配到的图片为基准，向上拖动280
            self.display_msg('向上拖拉以识别挑战类型')
            start_x = loc_tmp.left + loc_tmp.width / 2
            start_y = loc_tmp.top + loc_tmp.height / 2
            end_y = start_y - 280
            self.drag_rel(start_x, start_y, start_x, end_y)
            time.sleep(1.5)


if __name__ == '__main__':
    autogui = Yaoqi()
    autogui.run('yaoqi')
    # logger.debug(str(autogui.prepare_image_callback))
    # logger.debug(str(autogui.loop_image_callback))
