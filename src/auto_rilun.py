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


class Rilun(Autogui):
    def __init__(self, win_name='阴阳师-网易游戏', yys_config=None):
        Autogui.__init__(self, win_name, yys_config)
        # 设置当前副本的类型，设置之后优先查找御灵对应的截图
        self.screenshot.set_current_setion('rilun')  # 设置优先的截图信息
        self.config.set_current_setion('rilun')  # 设置当前配置信息
        self.pre_loop_times = self.config.cur_config.get('pre_loop_times', 20)
        self.loop_times = self.config.cur_config.get('loop_times', 20)
        self.change_fodder = self.config.cur_config.get('change_fodder', True)
        self.fodder_type = self.config.cur_config.get('fodder_type', 'fodder')
        self.drag = self.config.general.get('drag_dis', 5)  # 拖动距离
        self.players = self.config.cur_config.get('players', 1)
        self.captain = self.config.cur_config.get('captain', True)
        self.prepare_click_times = 0
        if self.players > 1:
            self.display_msg('组队挑战时不更换狗粮')
            self.change_fodder = False

        # 预览时式神区域
        self.preinstall_locs = [
            [460, 360, 160, 200],  # 左到右第三个式神
            [620, 360, 160, 200],  # 左到右第四个式神
            [780, 360, 160, 200]  # 左到右第五个式神
        ]
        # 交换界面的式神区域
        self.exchange_locs = [
            [160, 160, 130, 300],  #  左到右第 1 个式神
            [290, 160, 190, 300],  #  左到右第 2 个式神
            [450, 160, 190, 300]  #  左到右第 3 个式神
        ]
        # 锁定第四个式神
        self.second_role_inc_box = [620, 360, 160, 200]
        self.second_click_inc_pos = (730, 515)
        self.already_select_layer = False

        prepare_callback = [
            ('search', self.click_loc_one_and_move_uncover),
            ('yuhun', self.click_loc_one_and_move_uncover),  # 组队挑战暂不考虑自动邀请的问题
            ('rilun', self.click_loc_one_and_move_uncover),
        ]
        loop_callback = [
            ('task_accept', self.task_accept_callback),
            ('yes', self.yes_callback),  # 确认，队长默认邀请队员，队员默认接受邀请
            ('always_accept', self.always_accept_callback),
            ('accept', self.accept_callback),  # 队员默认接受邀请
            ('fight', self.fight_callback),
            ('team_fight', self.team_fight_callback),  # 组队挑战
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

    def fight_callback(self, loc):
        if self.already_select_layer:
            self.click_loc_one_and_move_uncover(loc)
            return

        loc_tmp = self.locate_im(self.get_image('layer3'))
        if loc_tmp:
            self.cur_key = 'layer3'
            self.already_select_layer = True
            self.click_loc_one_and_move_uncover(loc_tmp)
            time.sleep(0.5)

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
                    self.display_msg('点击挑战时无法进入，保存临时图片，作为校验确认')
                    im_yys.save('absent_{0:.0f}.jpg'.format(time.time()))
                    time.sleep(2)
                else:
                    time.sleep(0.5)
                    return
            time.sleep(1)
        else:
            self.display_msg('队员需要等待队长点击开始')
            time.sleep(5)

    def __prepare_team_fodder_callback(self, loc):
        if self.prepare_click_times < 3:
            self.click_loc_one_and_move_uncover(loc)
            self.prepare_click_times += 1
            time.sleep(1)
            self.wait_keys(['prepare'], self.prepare_callback)
            return
        else:
            # 如果 3s 后还没有开始，可能是有其他失败场景引起的需要重新点击
            time.sleep(4)
            if self.locate_im(self.get_image('prepare')):
                self.click_loc_one_and_move_uncover(loc)
            return

    def prepare_callback(self, loc):
        if self.change_fodder is False:
            if self.players == 1:
                self.click_loc_one_and_move_uncover(loc)
            else:
                self.__prepare_team_fodder_callback(loc)
            return

        # 预设界面：刚进入挑战，含有预设的界面
        im_yys = self.screenshot_exact()
        loc_tmp = self.locate_im(self.get_image('preinstall'), im_yys)
        if loc_tmp:
            locations = self.get_all_images_by_locs(['man'],
                                                    self.preinstall_locs)
            man_nums = len(locations) if locations else 0
            if man_nums > 0:
                random_x = uniform(-10, 10)
                random_y = uniform(-10, 10)
                self.cur_key = 'exchange_preinstall'
                self.click_loc_inc(628 + random_x, 540 + random_y, 1)
                time.sleep(2.5)
            else:
                self.display_msg('当前不需要更换狗粮')
                self.click_loc_one_and_move_uncover(loc)
                time.sleep(2)
                self._mark_callback()
            return

        # 交换式神界面
        loc_tmp = self.locate_im(self.get_image('exchange'), im_yys)
        if loc_tmp:
            locations = self.get_all_images_by_locs(['man'],
                                                    self.exchange_locs)
            man_nums = len(locations)
            if man_nums > 0:
                self.cur_key = 'change_fodder_type'
                self.change_fodder_type(self.fodder_type)
                self.cur_key = 'exchange_fodder'
                self.exchange_fodder(locations, self.drag)
                self.display_msg('狗粮替换完成')
            else:
                self.click_loc_one_and_move_uncover(loc)
                time.sleep(2)
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

        if self.is_inc_box_has_key('marked', self.second_role_inc_box[0],
                                   self.second_role_inc_box[1],
                                   self.second_role_inc_box[2],
                                   self.second_role_inc_box[3]):
            self.display_msg('已经标记完成')
        else:
            self.cur_key = 'marked'
            random_y = random_x = uniform(-10, 10)
            self.click_loc_inc(self.second_click_inc_pos[0] + random_x,
                               self.second_click_inc_pos[1] + random_y, 1)
            time.sleep(2)

    def yes_callback(self, loc):
        loc_tmp = self.locate_im(self.get_image('default_invite'))
        if loc_tmp:
            self.display_msg('设置为默认邀请队友')
            self.cur_key = 'default_invite'
            self.click_loc_inc(loc_tmp.left - 20, loc_tmp.top + 9, 1)
            # self.click_loc_inc(loc_tmp.left, loc_tmp.top, 1)
            self.cur_key = 'yes'
            time.sleep(0.5)
            self.click_loc_one(loc)
            self.prepare_click_times = 999  # 默认邀请之后不需要重新点击准备
            return

        loc_tmp = self.locate_im(self.get_image('no_attention'))
        if loc_tmp:
            self.display_msg('不再提示，默认接受邀请')
            self.cur_key = 'no_attention'
            self.click_loc_inc(loc_tmp.left - 20, loc_tmp.top + 9, 1)
            self.cur_key = 'yes'
            time.sleep(0.5)
            self.click_loc_one(loc)
            self.prepare_click_times = 999  # 默认邀请之后不需要重新点击准备
            return

        # 只有确定
        self.click_loc_one(loc)

    def accept_callback(self, loc):
        self.prepare_click_times = 0  # 非默认邀请，需要重新归零，重新点击准备
        self.cur_key = 'accept'
        self.click_loc_one(loc)

    def always_accept_callback(self, loc):
        self.prepare_click_times = 999  # 默认邀请之后不需要重新点击准备
        self.cur_key = 'always_accept'
        self.click_loc_one(loc)


if __name__ == '__main__':
    autogui = Rilun()
    autogui.run('rilun')
    logger.debug(str(autogui.prepare_image_callback))
    logger.debug(str(autogui.loop_image_callback))

# %%
