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
from random import randint, uniform


class Yuling(Autogui):
    def __init__(self, win_name='阴阳师-网易游戏', yys_config=None):
        Autogui.__init__(self, win_name, yys_config)
        # 设置当前副本的类型，设置之后优先查找御灵对应的截图
        self.screenshot.set_current_setion('yuling')  # 设置优先的截图信息
        self.config.set_current_setion('yuling')  # 设置当前配置信息
        self.pre_loop_times = self.config.cur_config.get('pre_loop_times', 20)
        self.loop_times = self.config.cur_config.get('loop_times', 20)
        self.fight_type = self.config.cur_config.get('type', 'leopard')
        self.need_mark = self.config.cur_config.get('mark', False)
        self.already_select_layer = False
        self.remain_types = ['leopard', 'fox', 'phenix', 'dragon']

        self.remain_types.remove(self.fight_type)
        self.remain_types.insert(0, self.fight_type)  # 设置的挑战类型放在第一个
        # 位置跟结界突破不同，御灵的位置便左
        self.four_role_inc_box = [580, 190, 280, 250]
        self.four_click_inc_pos = (666, 400)

        prepare_callback = [
            ('search', self.click_loc_one),
            ('yuling', self.click_loc_one),
            ('unopened', self.unopened_callback),
            ('dragon', self.unopened_callback),
            ('fox', self.unopened_callback),
            ('leopard', self.unopened_callback),
            ('phenix', self.unopened_callback),
        ]
        loop_callback = [
            ('task_accept', self.task_accept_callback),
            ('fight', self.fight_callback),
            ('prepare', self.prepare_callback),
            ('victory', self.victory_callback),
            ('fail', self.fail_callback),
            ('award', self.award_callback),
            ('time', self.void_callback),
        ]

        self.init_image_callback(prepare_callback, loop_callback)

    def _fighttype_callback(self, fight_type):
        im_yys = self.screenshot_exact()
        loc_tmp = self.locate_im(self.get_image(fight_type), im_yys)
        if loc_tmp:
            self.cur_key = fight_type
            self.click_loc_one(loc_tmp)
        else:
            self.display_msg('无法切换到类型：{0}'.format(fight_type))

    def unopened_callback(self, loc):
        if len(self.remain_types) == 0:
            self.stop = True
            self.display_msg('所有类型都未开放')
        self.last_fight_type = self.remain_types[0]
        self.remain_types.remove(self.remain_types[0])
        self._fighttype_callback(self.last_fight_type)

    def fight_callback(self, loc):
        if self.already_select_layer is False:
            im_yys = self.screenshot_exact()
            loc_tmp = self.locate_im(self.get_image('layer3'), im_yys)
            if loc_tmp:
                self.click_loc_one(loc_tmp)
            else:
                self.display_msg('无法找到第三层：{0}'.format('layer3'))
                return
            self.already_select_layer = True
        else:
            self.click_loc_one_and_move_uncover(loc)
        time.sleep(2)

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
    autogui = Yuling()
    autogui.run('yuling')
    logger.debug(str(autogui.prepare_image_callback))
    logger.debug(str(autogui.loop_image_callback))
