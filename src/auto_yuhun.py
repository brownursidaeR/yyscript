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

from autogui import Autogui, ImageCallback

logger = logging.getLogger('kiddo')


class Yuhun(Autogui):
    def __init__(self, win_name='阴阳师-网易游戏', yys_config=None):
        Autogui.__init__(self, win_name, yys_config)
        # 设置当前副本的类型，设置之后优先查找御灵对应的截图
        self.screenshot.set_current_setion('yuhun')  # 设置优先的截图信息
        self.pre_loop_times = self.config.cur_config.get('pre_loop_times', 40)
        self.loop_times = self.config.cur_config.get('loop_times', 40)
        self.captain = self.config.cur_config.get('captain', True)
        self.players = self.config.cur_config.get('players', 2)
        self.prepare_click_times = 0
        self.already_auto_prepare = False

        prepare_callback = [
            ('search', self.click_loc_one),
            ('yuhun', self.click_loc_one),
        ]
        loop_callback = [
            ('task_accept', self.task_accept_callback),
            ('yes', self.yes_callback),  # 确认，队长默认邀请队员，队员默认接受邀请
            ('always_accept', self.always_accept_callback),
            ('accept', self.accept_callback),  # 队员默认接受邀请
            ('fight', self.fight_callback),  # 单人挑战
            ('team_fight', self.team_fight_callback),  # 组队挑战
            ('time', self.void_callback),
            ('confirm', self.yes_callback),  # 确认
            ('prepare', self.prepare_callback),
            ('victory', self.victory_callback),
            ('fail', self.fail_callback),
            ('award', self.award_callback),
            ('time', self.void_callback),
            ('continue', self.continue_callback),  # 防止点击到查看御魂详细
            ('black', self.click_safely_loc),  # 防止点击到查看队友信息
        ]

        self.init_image_callback(prepare_callback, loop_callback)

    def prepare_callback(self, loc):
        if self.prepare_click_times < 3:
            self.click_loc_one_and_move_uncover(loc)
            self.prepare_click_times += 1
            time.sleep(1)
            self.wait_keys(['prepare'], self.prepare_callback)
        else:
            # 如果 3s 后还没有开始，可能是有其他失败场景引起的需要重新点击
            time.sleep(4)
            if self.locate_im(self.get_image('prepare')):
                self.click_loc_one_and_move_uncover(loc)

    def task_accept_callback(self, loc):
        im_yys = self.screenshot_exact()
        # 接受组队邀请的接受
        loc_tmp = self.locate_im(self.get_image('accept'), im_yys)
        if loc_tmp:
            self.click_loc_one(loc_tmp)
        else:
            # 悬赏任务的接受
            loc_tmp = self.locate_im(self.get_image('accept_xs'), im_yys)
            if loc_tmp:
                self.click_loc_one(loc_tmp)

    def always_accept_callback(self, loc):
        self.prepare_click_times = 999  # 默认邀请之后不需要重新点击准备
        self.cur_key = 'always_accept'
        self.click_loc_one(loc)

    def accept_callback(self, loc):
        self.prepare_click_times = 0  # 非默认邀请，需要重新归零，重新点击准备
        self.cur_key = 'accept'
        self.click_loc_one(loc)

    def fight_callback(self, loc):
        self.click_loc_one(loc)

    def team_fight_callback(self, loc):
        need_wait_player = False
        if self.captain:
            im_yys = self.screenshot_exact()
            # 中间和最右边的图片不太一样，实际一张就可以了，保险起见
            if self.players == 1:
                pass
            elif self.players == 2:
                im_absent = self.screenshot_inc(480, 160, 200, 180)  # 取中间+号
                im_yys = im_absent
            elif self.players == 3:
                im_yys = im_yys

            if self.players > 1:
                if self.locate_im(self.get_image('absent'), im_yys):
                    need_wait_player = True
                    self.display_msg('组队挑战 absent，需要等待队友来齐')
                elif self.locate_im(self.get_image('absent2'), im_yys):
                    self.display_msg('组队挑战 absent2，需要等待队友来齐')
                    need_wait_player = True
                else:
                    pass

            if need_wait_player is False:
                self.display_msg('队员已来齐，确认开始挑战')
                self.click_loc_one_and_move_uncover(loc)
                if self.locate_im(self.get_image('need_player')):
                    self.display_msg('点击挑战时无法进入，保存临时图片，作为校task_accept_callback验确认')
                    # im_yys.save('absent_{0:.0f}.jpg'.format(time.time()))
                    time.sleep(2)
                else:
                    time.sleep(0.5)
                    return
            time.sleep(1)
        else:
            self.display_msg('队员需要等待队长点击开始')
            time.sleep(5)


if __name__ == '__main__':
    autogui = Yuhun()
    autogui.run('yuhun')
    logger.debug(str(autogui.prepare_image_callback))
    logger.debug(str(autogui.loop_image_callback))
