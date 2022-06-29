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


class YysBreak(Autogui):
    def __init__(self, win_name='阴阳师-网易游戏', yys_config=None):
        Autogui.__init__(self, win_name, yys_config)
        # 设置当前副本的类型，设置之后优先查找御灵对应的截图
        self.screenshot.set_current_setion('yys_break')
        self.pre_loop_times = self.config.cur_config.get('pre_loop_times', 20)
        self.loop_times = self.config.cur_config.get('loop_times', 40)
        self.only_person = self.config.cur_config.get('only_person', False)
        self.need_mark = self.config.cur_config.get('mark', True)
        self.cur_type = 'group'
        self.group_done = self.only_person if self.only_person else False
        self.person_done = False
        self.person_inc_boxes = [  # 个人挑战的框体
            [140, 150, 300, 116],  # 第 1 行， 第 1 列
            [140, 270, 300, 116],  # 第 2 行， 第 1 列
            [140, 390, 300, 116],  # 第 3 行， 第 1 列
            [440, 150, 300, 116],  # 第 1 行， 第 2 列
            [440, 270, 300, 116],  # 第 2 行， 第 2 列
            [440, 390, 300, 116],  # 第 3 行， 第 2 列
            [740, 150, 300, 116],  # 第 1 行， 第 3 列
            [740, 270, 300, 116],  # 第 2 行， 第 3 列
            [740, 390, 300, 116],  # 第 3 行， 第 3 列
        ]
        self.group_inc_boxes = [  # 寮挑战的框体
            [400, 140, 290, 120],  # 第 1 行， 第 1 列
            [400, 260, 290, 120],  # 第 2 行， 第 1 列
            [400, 380, 290, 120],  # 第 3 行， 第 1 列
            [400, 500, 290, 120],  # 第 4 行， 第 1 列
            [690, 140, 290, 120],  # 第 1 行， 第 2 列
            [690, 260, 290, 120],  # 第 2 行， 第 2 列
            [690, 380, 290, 120],  # 第 3 行， 第 2 列
            [690, 500, 290, 120],  # 第 4 行， 第 2 列
        ]
        self.four_role_inc_box = [670, 190, 200, 250]
        self.four_click_inc_pos = (750, 400)
        # 异步时，除去了边框，横坐标左移15，纵坐标上移17
        if True:
            for box in self.person_inc_boxes:
                box[0] -= 15
                box[1] -= 20

            for box in self.group_inc_boxes:
                box[0] -= 15
                box[1] -= 20

        prepare_callback = [
            ('search', self.click_loc_one),
            ('break', self.click_loc_one),
        ]
        loop_callback = [
            ('yes', self.click_loc_one),  # 刷新时点击确认
            ('task_accept', self.task_accept_callback),
            ('reward_preview', self.click_safely_loc),
            ('blacklist', self.blacklist_callback),  # 个人信息页，拉黑名单
            ('weekend', self.person_callback),  # 个人挑战
            ('record', self.person_callback),  # 个人挑战-呱太活动时
            ('group', self.group_callback),  # 寮挑战
            ('prepare', self.prepare_callback),  # 负责后续打标记
            ('unselected', self.unselected_callback),  # 会长还未选择对抗寮
            ('victory', self.victory_callback),
            ('fail', self.fail_callback),
            ('award', self.award_callback),
            ('continue', self.continue_callback),  # 3,6,9时用到
            ('time', self.void_callback),
        ]

        self.init_image_callback(prepare_callback, loop_callback)

    def person_callback(self, loc):
        self.cur_type = 'Person'
        im_yys = self.screenshot_exact()
        # im_yys.save('{0}_{1:.0f}.jpg'.format('refresh', time.time()))
        # 先切换到寮突进行寮突破
        if self.group_done is False:
            loc_tmp = self.locate_im(self.get_image('group_transform'), im_yys)
            if loc_tmp:
                self.cur_key = 'group_transform'
                self.click_loc_one(loc_tmp)
            else:
                self.stop = True
            return

        loc_tmp = self.locate_im(self.get_image('award'), im_yys)
        if loc_tmp:
            # 挑战完 3 6 9 将之后可能会卡死在匹配上，做一层点击奖励的容错
            self.cur_key = 'award'
            self.display_msg('369次之后点击领取额外奖励')
            self.award_callback(loc_tmp)
            return

        some_box_failed = False
        if self.person_done is False:
            for box in self.person_inc_boxes:
                # self.show_im_by_inc(box[0], box[1], box[2], box[3])
                # continue
                if self.is_inc_box_has_key('broken', box[0], box[1], box[2],
                                           box[3]):
                    continue

                # 新失败的和旧失败的截图不一样
                if (self.is_inc_box_has_key(
                        'break_fail_person',
                        box[0],
                        box[1],
                        box[2],
                        box[3],
                ) or self.is_inc_box_has_key('break_fail_person2', box[0],
                                             box[1], box[2], box[3])):
                    some_box_failed = True
                    continue
                else:
                    self.cur_key = 'box_fight'
                    self._click_box_one(box)
                    return

        if some_box_failed:
            self.display_msg('本轮个人突破已经全部挑战完成')
            if self.locate_im(self.get_image('wait_refresh')):
                self.cur_key = 'wait_refresh'
                self.display_msg('检测到正常CD，过30s后再判断')
                time.sleep(30)
            else:
                loc_tmp = self.locate_im(self.get_image('refresh'))
                if loc_tmp:
                    self.display_msg('刷新进入下一轮判断')
                    self.cur_key = 'refresh'
                    self.click_loc_one_and_move_uncover(loc_tmp)
                    return

                # 有的时候会卡在最后一个格子失败
                loc_tmp = self.locate_im(self.get_image('weekend'))
                if loc_tmp:
                    self.display_msg('退出最后一次失败')
                    self.cur_key = 'weekend'
                    self.click_loc_one_and_move_uncover(loc_tmp)
                    return

                loc_tmp = self.locate_im(self.get_image('record'))
                if loc_tmp:
                    self.display_msg('退出最后一次失败')
                    self.cur_key = 'record'
                    self.click_loc_one_and_move_uncover(loc_tmp)
                    return
                # else:
                #     im_yys.save('{0}_{1:.0f}.jpg'.format('refresh', time.time()))

    def unselected_callback(self, loc):
        self.display_msg('寮突破还未选择突破寮，寮突结束，切换到个人突破')
        self.group_done = True
        self.group_callback(loc)

    def group_callback(self, loc):
        self.cur_type = 'group'
        if self.group_done:
            im_yys = self.screenshot_exact()
            loc_tmp = self.locate_im(self.get_image('person_transform'),
                                     im_yys)
            if loc_tmp:
                self.cur_key = 'person_transform'
                self.click_loc_one(loc_tmp)
                time.sleep(1)
            else:
                self.stop = True
            return

        if self.is_inc_box_has_key('broken', self.group_inc_boxes[0][0],
                                   self.group_inc_boxes[0][1],
                                   self.group_inc_boxes[0][2],
                                   self.group_inc_boxes[0][3]):
            self.display_msg('寮突破已经全部挑战完成，正在退出')
            self.group_done = True
            return

        for box in self.group_inc_boxes:
            # self.show_im_by_inc(box[0], box[1], box[2], box[3])
            # continue
            if self.is_inc_box_has_key('break_fail_group', box[0], box[1],
                                       box[2], box[3]):
                continue
            elif self.is_inc_box_has_key('broken', box[0], box[1], box[2],
                                         box[3]):
                continue
            else:
                self._click_box_one(box)
                time.sleep(3)  # 挑战进入比较慢，多等待3S
                return

        # 所有都失败了
        self.display_msg('寮突破已经全部失败，正在退出')
        self.group_done = True

    def _check_no_ticket(self):
        im_yys = self.screenshot_exact()
        loc_tmp = self.locate_im(self.get_image('no_ticket'), im_yys)
        if loc_tmp:
            return True
        return False

    def _check_in_cd(self):
        im_yys = self.screenshot_exact()
        loc_tmp = self.locate_im(self.get_image('cd'), im_yys)
        if loc_tmp:
            return True
        return False

    def fight_callback(self, loc):
        self.cur_key = 'fight'
        self.click_loc_one(loc)
        time.sleep(0.5)
        if self._check_no_ticket():
            self.person_done = True
            self.stop = True
            self.display_msg('挑战券都已经用完，正在退出个人模式的挑战')

        if self._check_in_cd():
            self.group_done = True
            self.display_msg('寮突破处于CD状态，切换到个人模式')

        time.sleep(2.5)  # 界面切换比较耗时，多等待2秒

    def _click_box_one(self, box_loc):
        im_yys = self.screenshot_exact()
        loc_tmp = self.locate_im(self.get_image('fight'), im_yys)
        if loc_tmp:
            self.fight_callback(loc_tmp)
        elif self.locate_im(self.get_image('continue'), im_yys):
            # 异常处理
            return
        else:
            # 只点击一次，然后重新进行判断
            self.cur_key = 'click_box_one'
            random_x = uniform(0.5 * box_loc[2], 0.75 * box_loc[2])
            random_y = uniform(0.3 * box_loc[3], 0.8 * box_loc[3])
            self.click_loc_inc(box_loc[0] + random_x, box_loc[1] + random_y, 1)
            time.sleep(1.5)
            self.wait_keys(['fight'], self.fight_callback)

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

    def blacklist_callback(self, loc):
        # 不小心点到个人信息页时，要点击其他位置退出
        loc_tmp = self.locate_im(self.get_image('group'))
        if loc_tmp:
            self.cur_key = 'group'
            self.click_loc_one_and_move_uncover(loc_tmp)
            time.sleep(2)
            self._mark_callback()
            return

        loc_tmp = self.locate_im(self.get_image('weekend'))
        if loc_tmp:
            self.cur_key = 'weekend'
            self.click_loc_one_and_move_uncover(loc_tmp)
            time.sleep(2)
            self._mark_callback()
            return


if __name__ == '__main__':
    autogui = YysBreak()
    autogui.run('yys_break')
    logger.debug(str(autogui.prepare_image_callback))
    logger.debug(str(autogui.loop_image_callback))
