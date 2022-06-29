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


class Douji(Autogui):
    def __init__(self, win_name='阴阳师-网易游戏', yys_config=None):
        Autogui.__init__(self, win_name, yys_config)
        # 设置当前副本的类型，设置之后优先查找御灵对应的截图
        self.screenshot.set_current_setion('douji')  # 设置优先的截图信息
        self.config.set_current_setion('douji')  # 设置当前配置信息
        self.pre_loop_times = self.config.cur_config.get('pre_loop_times', 20)
        self.loop_times = self.config.cur_config.get('loop_times', 400)
        self.need_mark = self.config.cur_config.get('mark', False)
        # 锁定之后等待的时间，不开放配置，仅可通过修改 ini 文件实现
        self.wait_complete_times = self.config.cur_config.get(
            'wait_complete_times', 50)

        self.four_role_inc_box = [670, 190, 200, 250]
        self.four_click_inc_pos = (700, 400)

        prepare_callback = []
        loop_callback = [
            ('yes', self.click_loc_one),  # 刷新时点击确认
            ('task_accept', self.task_accept_callback),
            ('douji', self.click_loc_one_and_move_uncover),
            ('shoudong', self.__shoudong_callback),  # 手动改自动
            ('level_up', self.click_safely_loc),  # 段位提升
            ('mvp', self.click_safely_loc),  # 拔得头筹
            ('auto_in', self.click_loc_one_and_move_uncover),  # 自动上阵
            ('prepare', self.__prepare_callback),  # 负责后续打标记
            ('already_prepare', self.__already_prepare_callback),  # 已准备
            ('fight', self.__fight_callback),  # 挑战后准备时间比较长
            ('victory', self.victory_callback),
            ('fail', self.fail_callback),
            ('continue', self.continue_callback),
            ('searching', self.void_callback),
        ]

        self.init_image_callback(prepare_callback, loop_callback)

    def __fight_callback(self, loc):
        self.click_loc_one_and_move_uncover(loc)
        time.sleep(6)

    def __shoudong_callback(self, loc):
        self.cur_key = 'shoudong'
        self.display_msg('从手动切换到自动')
        self.click_loc_one_and_move_uncover(loc)
        time.sleep(1)
        self.__already_prepare_callback(loc)

    def __prepare_callback(self, loc):
        self.display_msg('识别到准备，并点击进入已准备')
        self.cur_key = 'prepare'
        self.click_loc_one_and_move_uncover(loc)
        time.sleep(2)

        loc_tmp = self.locate_im(self.get_image('shoudong'))
        if loc_tmp:
            self.__shoudong_callback(loc_tmp)
            return

        loc_tmp = self.locate_im(self.get_image('already_prepare'))
        if loc_tmp:
            self.__already_prepare_callback(loc)
            return

    def __already_prepare_callback(self, loc):
        self.display_msg('识别到已准备，并点击进入识别锁定阶段')
        self.cur_key = 'already_prepare'

        while self.locate_im(self.get_image('already_prepare')):
            self.display_msg('已准备，但还没有开始，暂时不能进行标记')
            time.sleep(1.5)

        time.sleep(5)
        if self.locate_im(self.get_image('already_auto')) is None:
            self.display_msg('手动模式，需要切换自动模式')
            loc_tmp = self.locate_im(self.get_image('shoudong'))
            if loc_tmp:
                self.cur_key = 'shoudong'
                self.display_msg('从手动切换到自动')
                self.click_loc_one_and_move_uncover(loc_tmp)

        # 一定时间内判断是否符合其他退出条件
        already_complete_keys = ['mvp', 'fail', 'victory']
        wait_complete_times = self.wait_complete_times
        for i in range(wait_complete_times):
            time.sleep(1)
            if i > 0 and i % 5 == 0:
                self.display_msg('标记执行检测：{0}'.format(i))
            elif i == 2 and self.need_mark:
                # 判断是否需要进行标记
                self._mark_callback()

            im_yys = self.screenshot_exact()
            for check_key in already_complete_keys:
                if self.locate_im(self.get_image(check_key), im_yys):
                    self.display_msg('符合退出条件：成功，失败，mvp，直接进行下一轮')
                    return

        if self.locate_im(self.get_image('buff_up')):
            self.display_msg(
                '{0}S 后还没有完成挑战，退出进行下一轮'.format(wait_complete_times))
            loc_tmp = self.locate_im(self.get_image('return'))
            if loc_tmp:
                self.cur_key = 'return'
                self.click_loc_one_and_move_uncover(loc_tmp)
                time.sleep(1)

            loc_tmp = self.locate_im(self.get_image('confirm'))
            if loc_tmp:
                self.cur_key = 'confirm'
                self.click_loc_one_and_move_uncover(loc_tmp)
                time.sleep(0.5)

    def _mark_callback(self):
        self.display_msg('正在尝试进行标记')

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
    autogui = Douji()
    autogui.run('douji')
    logger.debug(str(autogui.prepare_image_callback))
    logger.debug(str(autogui.loop_image_callback))
