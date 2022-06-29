#!/usr/bin/python
# -*- coding: utf-8 -*

# %% 先加载对应的库
from autogui import Autogui, ImageCallback
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


class Activity(Autogui):
    def __init__(self, win_name='阴阳师-网易游戏', yys_config=None):
        Autogui.__init__(self, win_name, yys_config)
        self.screenshot.set_current_setion('activity')  # 设置优先的截图信息
        self.config.set_current_setion('activity')  # 设置当前配置信息
        self.pre_loop_times = self.config.cur_config.get('pre_loop_times', 20)
        self.loop_times = self.config.cur_config.get('loop_times', 400)
        self.need_mark = self.config.cur_config.get('mark', False)

        self.four_role_inc_box = [670, 190, 200, 250]
        self.four_click_inc_pos = (750, 400)

        prepare_callback = []
        loop_callback = [
            ('yes', self.click_loc_one),  # 刷新时点击确认
            ('task_accept', self.task_accept_callback),
            ('prepare', self.prepare_callback),  # 负责后续打标记
            ('limit', self.limit_callback),  # 达到上限
            # ('xunfu', self.xunfu_callback),
            ('fight_activity', self.click_loc_one_and_sleep),  # 负责后续打标记
            ('victory', self.victory_callback),
            ('fail', self.fail_callback),
            ('award', self.award_callback),
            ('continue', self.continue_callback),  # 3,6,9时用到
            ('time', self.void_callback),
        ]

        self.init_image_callback(prepare_callback, loop_callback)

    def limit_callback(self, loc):
        self.display_msg('已经达到上限，正在退出')
        self.stop = True

    # def xunfu_callback(self, loc):
    #     # 放大倍数来点击
    #     self.click_enlarge_loc_one(loc, 1.2, 6)
    #     time.sleep(2)

    def prepare_callback(self, loc):
        self.cur_key = 'prepare'
        self.click_loc_one_and_move_uncover(loc)
        time.sleep(2)
        self.wait_keys(['prepare'], self.click_loc_one_and_move_uncover)
        time.sleep(2)
        if self.need_mark:
            self._mark_callback()

    def _mark_callback(self):
        self.display_msg('正在尝试进行标记')
        im_yys = self.screenshot_exact()
        loc_tmp = self.locate_im(self.get_image('prepare'), im_yys)
        if loc_tmp:
            self.cur_key = 'prepare'
            self.click_loc_one_and_move_uncover(loc_tmp)
            time.sleep(2)
            self._mark_callback()
            return

        if self.is_inc_box_has_key('marked', self.four_role_inc_box[0],
                                   self.four_role_inc_box[1],
                                   self.four_role_inc_box[2],
                                   self.four_role_inc_box[3]):
            self.display_msg('已经标记完成')
        else:
            self.cur_key = 'marked'
            random_y = random_x = uniform(-10, 10)
            self.click_loc_inc(self.four_click_inc_pos[0] + random_x,
                               self.four_click_inc_pos[1] + random_y, 1)
            time.sleep(2)


if __name__ == '__main__':
    autogui = Activity()
    autogui.run('activity')
    logger.debug(str(autogui.prepare_image_callback))
    logger.debug(str(autogui.loop_image_callback))
