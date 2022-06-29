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


class UpgradeFodder(Autogui):
    def __init__(self, win_name='阴阳师-网易游戏', yys_config=None):
        Autogui.__init__(self, win_name, yys_config)
        # 设置当前副本的类型，设置之后优先查找御灵对应的截图
        self.screenshot.set_current_setion('upgrade')  # 设置优先的截图信息
        self.config.set_current_setion('upgrade')  # 设置当前配置信息
        self.pre_loop_times = self.config.cur_config.get('pre_loop_times', 20)
        self.loop_times = self.config.cur_config.get('loop_times', 20)
        self.stars_upgrade = self.config.cur_config.get('upgrade_stars', 2)
        self.fodder_type = self.config.cur_config.get('fodder_type', 'ncard')
        self.cur_loop_times = 0
        self.already_arrange_relax = False  # 宽松排列
        self.already_arrange_stars = False  # 按星级排列
        self.already_select_stars = False  # 选择升级的狗粮星级
        self.already_arrange_fodder = False  # 用来升级的狗粮排列类型
        self.already_change_rarity = False  # 用来设置狗粮的稀有度，即用N卡还是白蛋来喂
        self.already_in_forster = False  # 已经进入育成状态
        # 折叠式神时，育成造成祭品的狗粮会变成第1行第2列，影响判断，所以用竖形排列
        self.roles_boxes = [
            [60, 195, 100, 140],  # 第 1 行 , 第 1 列
            [60, 335, 100, 140],  # 第 2 行 , 第 1 列
            [60, 475, 100, 140],  # 第 3 行 , 第 1 列
            [160, 195, 100, 140],  # 第 1 行 , 第 2 列
            [160, 335, 100, 140],  # 第 2 行 , 第 2 列
            [160, 475, 100, 140],  # 第 3 行 , 第 2 列
            [260, 195, 100, 140],  # 第 1 行 , 第 3 列
            [260, 335, 100, 140],  # 第 2 行 , 第 3 列
            [260, 475, 100, 140],  # 第 3 行 , 第 3 列
            [360, 195, 100, 140],  # 第 1 行 , 第 4 列
            [360, 335, 100, 140],  # 第 2 行 , 第 4 列
            [360, 475, 100, 140],  # 第 3 行 , 第 4 列
        ]

        prepare_callback = [
            ('roles', self.click_loc_one),
        ]
        loop_callback = [
            ('task_accept', self.task_accept_callback),
            ('not_enough', self.not_enough_callback),  # 狗粮不足时，停止
            ('confirm', self.confirm_callback),  # 确认
            ('yes', self.click_loc_one),  # 确定
            ('foster', self.foster_callback),
        ]

        self.init_image_callback(prepare_callback, loop_callback)

    def _arrage_relax(self):
        '''选择宽松排列'''
        loc_tmp = self.locate_im(self.get_image('order_type'))
        if loc_tmp:
            self.click_loc_one(loc_tmp)
            time.sleep(1)
            self.cur_key = 'order_relax'
            loc_relax = self.locate_im(self.get_image('order_relax'))
            if loc_relax:
                self.display_msg('标记宽松排列')
                self.already_arrange_relax = True
                self.click_loc_one(loc_relax)
            time.sleep(1)

    def _arrage_stars(self):
        '''选择按星级排列'''
        if self.already_arrange_stars and self.locate_im(
                self.get_image('star2')):
            return

        loc_stars = self.locate_im(self.get_image('order_by_star'))
        if loc_stars:
            self.cur_key = 'order_by_star'
            self.display_msg('标记按星级排列')
            self.already_arrange_stars = True
            self.click_loc_one(loc_stars)
            time.sleep(0.5)
            return

        loc_type = self.locate_im(self.get_image('order_type'))
        if loc_type:
            self.cur_key = 'order_type'
            self.click_loc_one(loc_type)
            time.sleep(1)
            self._arrage_stars()
            time.sleep(1)

    def _select_stars(self):
        '''选择要升级的狗粮星级'''
        self.display_msg('选择星级：{0}'.format(self.stars_upgrade))
        if self.stars_upgrade == 3:
            loc_star = self.locate_im(self.get_image('star3'), confidence=0.9)
        else:
            loc_star = self.locate_im(self.get_image('star2'))
        self.already_select_stars = True
        self.display_msg('选择要升级的狗粮星级,{0}->{1}'.format(self.stars_upgrade,
                                                      self.stars_upgrade + 1))
        self.cur_key = 'select_stars'
        self.click_loc_one(loc_star)
        time.sleep(0.5)

    def not_enough_callback(self, loc):
        '''狗粮不足时，自动退出升级'''
        self.display_msg('狗粮不足，正在退出')
        time.sleep(0.5)
        self.stop = True

    def foster_callback(self, loc):
        # 每一次点击育成时，都重新选择狗粮类型
        self.already_change_rarity = False

        roles_boxes = self.roles_boxes
        # 先选择宽松排列
        if self.already_arrange_relax is False:
            self._arrage_relax()
            return

        # 再按星级排序
        if self.already_arrange_stars is False:
            self._arrage_stars()
            return

        # 选择星级
        if self.already_select_stars is False:
            self._select_stars()
            return

        if self.already_in_forster is False:
            no_foster = True
            for i in range(len(roles_boxes)):
                '''
                    |     |
                    | man |
                    |     |
                    点击位置： (x_left * [0.3,0.8], x_top * [0.2,0.7])
                '''
                # self.show_im_by_inc(roles_boxes[i][0], roles_boxes[i][1],
                #                     roles_boxes[i][2], roles_boxes[i][3])
                loc_tmp = self.locate_im_inc(self.get_image('man'),
                                             roles_boxes[i][0],
                                             roles_boxes[i][1],
                                             roles_boxes[i][2],
                                             roles_boxes[i][3])
                if loc_tmp:
                    random_x = uniform(roles_boxes[i][2] * 0.3,
                                       roles_boxes[i][2] * 0.8)
                    random_y = uniform(roles_boxes[i][3] * 0.2,
                                       roles_boxes[i][3] * 0.7)
                    self.display_msg('选择第{0}个狗粮, 位置：({1}，{2})'.format(
                        i, roles_boxes[i][0] + random_x,
                        roles_boxes[i][1] + random_y))
                    self.cur_key = 'select_fodder'
                    self.click_loc_inc(roles_boxes[i][0] + random_x,
                                       roles_boxes[i][1] + random_y, 1)
                    time.sleep(0.5)
                    no_foster = False  # 标记需要点击育成
                    break

            if no_foster:
                self.display_msg('已经没有满级狗粮可以拿来升级，退出')
                self.stop = True
                return

            loc_tmp = self.locate_im(self.get_image('foster'))
            if loc_tmp:
                self.cur_key = 'foster'
                self.display_msg('已经选中要升级的狗粮，点击育成')
                self.click_loc_one(loc_tmp)

    def confirm_callback(self, loc):
        '''选择要作为狗粮的N卡或者白蛋'''
        roles_boxes = self.roles_boxes
        if self.already_change_rarity is False:
            self.already_change_rarity = True
            '''如果已经是按稀有度排序，就不再重新选择了'''
            if self.locate_im(self.get_image('already_rarity')):
                self.confirm_callback(loc)
                return

            loc_tmp = self.locate_im(self.get_image('fodder_select'))
            if loc_tmp:
                self.cur_key = 'fodder_select'
                self.click_loc_inc(loc_tmp.left + 10, loc_tmp.top + 10, 1)
                time.sleep(0.5)
            loc_tmp = self.locate_im(self.get_image('rarity'))
            if loc_tmp:
                self.display_msg('按稀有度排序作为狗粮的式神')
                self.cur_key = 'order_by_rarity'
                self.click_loc_one(loc_tmp)
                time.sleep(0.5)

            loc_tmp = self.locate_im(self.get_image(self.fodder_type))
            if loc_tmp:
                self.display_msg('选择{0}作为狗粮'.format(self.fodder_type))
                self.cur_key = 'select ' + self.fodder_type
                self.click_loc_one(loc_tmp)
                time.sleep(0.5)
        ''' ||| 形状的排序，田字型时需要替换成 ||| 排列'''
        if self.already_arrange_fodder is False:
            self.already_arrange_fodder = True
            loc_tmp = self.locate_im(self.get_image('fodder_relax'))
            if loc_tmp:
                self.display_msg('宽松排列作为狗粮的式神')
                self.cur_key = 'fodder_relax'
                self.click_loc_one(loc_tmp)
                time.sleep(0.5)

        for i in range(self.stars_upgrade):
            random_x = uniform(roles_boxes[i][2] * 0.3,
                               roles_boxes[i][2] * 0.8)
            random_y = uniform(roles_boxes[i][3] * 0.2,
                               roles_boxes[i][3] * 0.7)
            self.display_msg('选择狗粮{0}, ({1}，{2})'.format(
                i, roles_boxes[i][0] + random_x, roles_boxes[i][1] + random_y))
            self.cur_key = 'select_fodder'
            self.click_loc_inc(roles_boxes[i][0] + random_x,
                               roles_boxes[i][1] + random_y, 1)
            time.sleep(0.5)
        '''点击确认升级狗粮，并初始化状态位'''
        self.cur_key = 'upgrade'
        self.cur_loop_times += 1
        self.display_msg('升级第{0}/{1}只狗粮'.format(self.cur_loop_times,
                                                self.loop_times))
        self.click_loc_one(loc)
        self.already_in_forster = False  # 将正在升级的标记清空掉
        self.already_change_rarity = False  # 将已经调整为稀有度排序重置，重选N卡
        time.sleep(0.5)
        loc_tmp = self.locate_im(self.get_image('not_enough'))
        if loc_tmp:
            self.not_enough_callback(loc_tmp)
        else:
            time.sleep(2)  # 休息 2s 等待响应


if __name__ == '__main__':
    autogui = UpgradeFodder()
    autogui.run('upgrade')
    logger.debug(str(autogui.prepare_image_callback))
    logger.debug(str(autogui.loop_image_callback))
