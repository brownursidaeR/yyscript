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


class Chapter(Autogui):
    def __init__(self, win_name='阴阳师-网易游戏', yys_config=None):
        Autogui.__init__(self, win_name, yys_config)
        # 设置当前副本的类型，设置之后优先查找御灵对应的截图
        self.screenshot.set_current_setion('chapter')  # 设置优先的截图信息
        self.config.set_current_setion('chapter')  # 设置当前配置信息
        self.pre_loop_times = self.config.cur_config.get('pre_loop_times', 20)
        self.loop_times = self.config.cur_config.get('loop_times', 20)
        self.is_captain = self.config.cur_config.get('captain', True)
        self.players = self.config.cur_config.get('players', 2)
        # 是否启用更换狗粮
        self.change_fodder = self.config.cur_config.get('change_fodder', False)
        # 是否启用官方轮换，官方轮换启用后没有准备按钮
        self.official_change_fodder = self.config.cur_config.get(
            'official_change_fodder', False)
        if self.is_captain is False and self.players == 1:
            self.is_captain = True
        self.is_member = True if (self.is_captain is False
                                  and self.players > 1) else False
        self.drag_times = 0  # 已经拖动了多少次
        self.drag_left = False  # 是否是往左拉界面
        self.fodder_type = self.config.cur_config.get('fodder_type', 'fodder')
        self.drag = self.config.general.get('drag_dis', 5)  # 拖动距离
        self.cur_monster_is_boss = False
        self.last_moster_is_boss = False
        self.cur_loop_times = 0
        self.wait_loops = 0  # 等待队友的次数

        # 预设界面，队长的两个狗粮位置信息
        self.captain_preinstall_locs = [
            [385, 210, 135, 250],  # 第 1 行第 2 列
            [610, 320, 160, 250]  # 第 1 行第 3 列
        ]
        # 交换界面队长的狗粮位置信息
        self.captain_exchange_locs = [
            [100, 120, 190, 280],  # 第 1 行第 1 列
            [490, 120, 180, 280]  # 第 1 行第 2 列
        ]
        # 预设界面，队员的两个狗粮位置信息
        self.captain_team_preinstall_locs = [
            [0, 260, 135, 240],  # 第 2 行第 1 列
            [440, 470, 160, 220]  # 第 2 行第 2 列
        ]
        # 交换界面队长的狗粮位置信息
        self.captain_team_exchange_locs = [
            [260, 160, 150, 220],  # 第 2 行第 1 列
            [800, 160, 150, 220]  # 第 2 行第 2 列
        ]

        prepare_callback = [
            ('search', self.click_loc_one_and_move_uncover),
        ]
        loop_callback = [
            ('award_box_after_chapter', self.award_box_after_chapter_callback),
            ('yes', self.click_loc_one_and_move_uncover),  # 确认继续邀请
            ('accept', self.click_loc_one_and_move_uncover),  # 确认接受邀请
            ('chapter', self.chapter_callback),  # 队员不用点
            ('task_accept', self.task_accept_callback),
            ('enter_chapter', self.fight_callback),  # 单人挑战，可见即为单 人
            
            ('team_fight', self.team_fight_callback),  # absent
            ('boss_fight', self.boss_fight_callback),  # boss，要考虑有悬赏时会闪
            ('empty_monster', self.empty_monster_callback),  # 空怪物列表
            ('monster_fight', self.monster_fight_callback),  # 挑战普通小怪
            ('chapter_award_box', self.click_loc_one_and_move_uncover),
            ('chapter_award_detail', self.click_safely_loc),
            ('prepare', self.prepare_callback),
            ('victory', self.victory_callback),
            ('fox', self.fox_drag), #拖动
            ('fail', self.fail_callback),
            ('award', self.award_callback),
            ('time', self.void_callback),
            
        ]

        self.init_image_callback(prepare_callback, loop_callback)

    def award_box_after_chapter_callback(self, loc):
        if self.locate_im(self.get_image('team_fight')):
            self.display_msg('队长时在组队页面点击宝箱')
            self.click_loc_one_and_move_uncover(loc)

        elif self.is_captain:
            self.display_msg('队长时可能需要忽略宝箱')
            if self.players == 1:
                loc_tmp = self.locate_im(self.get_image('cancel'))
                if loc_tmp:
                    self.click_loc_one_and_move_uncover(loc_tmp)
                self.click_loc_one_and_move_uncover(loc)  # 点击宝箱

            else:
                loc_tmp = self.locate_im(self.get_image('yes'))
                if loc_tmp:
                    self.click_loc_one_and_move_uncover(loc_tmp)

        else:
            self.display_msg('队员时直接点击宝箱')
            self.click_loc_one_and_move_uncover(loc)

    def victory_callback(self, loc):
        self.display_msg('当前进度：{0}/{1}'.format(self.cur_loop_times + 1,
                                               self.loop_times))
        self.click_loc_one_and_move_uncover(loc)
        time.sleep(0.3)
        self.click_loc_one_and_move_uncover(loc)
        time.sleep(0.8)

        if self.cur_monster_is_boss:
            if self.last_key != self.cur_key:
                self.cur_loop_times += 1
                self.cur_monster_is_boss = False
                self.last_moster_is_boss = True  # 用来判断是否要等待奖励页面
        else:
            self.last_moster_is_boss = False

    def team_fight_callback(self, loc):
        im_yys = self.screenshot_exact()
        loc_tmp = self.locate_im(self.get_image('team_fight'), im_yys)
        if loc_tmp:
            loc_absent = self.locate_im(self.get_image('absent'), im_yys)
            if self.is_captain is False or loc_absent:
                self.display_msg('等待队员来启后才能进入章节')
                time.sleep(2)
                self.team_fight_callback(loc_tmp)
            else:
                self.click_loc_one_and_move_uncover(loc_tmp)

    def chapter_callback(self, loc):
        if self.is_member:
            return
        self.click_loc_one_and_move_uncover(loc)

    def __waiting_player(self, loc):
        '''等待队友结算'''
        if self.is_captain and self.locate_im(
                self.get_image('waiting_player')):
            self.wait_loops += 1
            if self.wait_loops > 6:
                self.display_msg(
                    '等待{0}队员依然没有退出奖励领取，退出'.format(self.wait_loops + 1))
                self.stop = True
            else:
                self.display_msg('第{0}次等待队员退出奖励领取'.format(self.wait_loops + 1))
                time.sleep(2)

    def fight_callback(self, loc):
        if self.is_member:
            return
        self.click_loc_one_and_move_uncover(loc)
        time.sleep(0.8)
        loc_tmp = self.locate_im(self.get_image('prepare'))
        if loc_tmp:
            self.prepare_callback(loc_tmp)

    def boss_fight_callback(self, loc):
        self.init_drag_status()
        self.cur_monster_is_boss = True
        if self.is_member:
            return
        self.click_loc_one_and_move_uncover(loc)
        time.sleep(0.5)
        self.__waiting_player(loc)
        time.sleep(0.8)
        loc_tmp = self.locate_im(self.get_image('prepare'))
        if loc_tmp:
            self.prepare_callback(loc_tmp)
        time.sleep(3)
        im_yys = self.screenshot_exact()
        loc_tmp = self.locate_im(self.get_image('chapter_award_box'),im_yys)
        if loc_tmp:
            self.cur_key = 'chapter_award_box'
            self.click_loc_one_and_move_uncover(loc_tmp)
            return

    def monster_fight_callback(self, loc):
        self.init_drag_status()
        if self.is_member:
            return

        loc_tmp = self.locate_im(self.get_image('boss_fight'))
        if loc_tmp:
            self.cur_key = 'boss_fight'
            self.boss_fight_callback(loc_tmp)
            return
        else:
            self.cur_key = 'monster_fight'
            self.click_loc_one_and_move_uncover(loc)
            time.sleep(0.5)
            self.__waiting_player(loc)

        time.sleep(0.8)
        loc_tmp = self.locate_im(self.get_image('prepare'))
        if loc_tmp:
            self.prepare_callback(loc_tmp)
        # self.empty_monster_callback(loc)
    
    


    def __check_preinstall_man(self, loc):
        # 预设界面：刚进入挑战，含有预设的界面
        im_yys = self.screenshot_exact()
        loc_tmp = self.locate_im(self.get_image('preinstall'), im_yys)
        if loc_tmp:
            locations = self.get_all_images_by_locs(['man'],
                                                    self.preinstall_locs)
            man_nums = len(locations) if locations else 0
            if man_nums > 0:
                self.display_msg('发现有{0}只满级狗粮，需要进行式神配置'.format(man_nums))
                self.cur_key = 'exchange_preinstall'
                random_x = randint(10, 25)
                random_y = randint(10, 25)
                # 点击小晴明的位置  270, 490
                start_x = 450
                start_y = 520
                for i in range(5):
                    click_x = start_x + random_x * i
                    click_y = start_y + random_y * i
                    self.click_loc_inc(click_x, click_y, 2)
                    time.sleep(1.5)
                    im_yys = self.screenshot_exact()
                    if self.locate_im(self.get_image('exchange')):
                        break

                    if self.locate_im(self.get_image('change_fodder'), im_yys):
                        self.cur_key = 'change_fodder'
                        self.display_msg('误触进入狗粮更换界面，退出重新更换')
                        loc_tmp = self.locate_im(self.get_image('back'))
                        if loc_tmp:
                            self.click_loc_one_and_move_uncover(loc_tmp)
                        self.cur_key = 'exchange_preinstall'
                        break
                return True
            else:
                self.display_msg('不需要更换狗粮，直接进行准备')
                self.click_loc_one_and_move_uncover(loc)
        return False

    def __check_need_change(self, loc):
        # 交换式神界面，队长有”交替“字样，队员的话就判断狗粮类型了
        need_change_fodder = False
        im_yys = self.screenshot_exact()
        if self.is_captain:
            if self.locate_im(self.get_image('exchange'), im_yys):
                need_change_fodder = True
        elif self.locate_im(self.get_image('all'), im_yys) or self.locate_im(
                self.get_image('fodder'), im_yys):
            need_change_fodder = True

        return need_change_fodder

    def __change_fodder(self, loc):
        # man 和 ec_man 不通用，所以干脆用两份 man 的截图
        locations = self.get_all_images_by_locs(['man', 'ex_man'],
                                                self.exchange_locs)
        man_nums = len(locations)
        if man_nums > 0:
            self.display_msg('发现有{0}只满级狗粮，需要进行狗粮交换'.format(man_nums))
            self.cur_key = 'change_fodder_type'
            self.change_fodder_type(self.fodder_type)
            self.cur_key = 'exchange_fodder'
            self.exchange_fodder(locations, self.drag)
            self.display_msg('本轮狗粮替换完成，并再次检查是否替换成功')
            time.sleep(0.5)
            if self.locate_im(self.get_image(self.fodder_type)) is None:
                self.__change_fodder(loc)  # 重新再检查一遍
            return

        self.display_msg('交换界面没有找到满级狗粮，不需要进行狗粮交换')
        self.cur_key = 'prepare'
        self.click_loc_one_and_move_uncover(loc)

    def prepare_callback(self, loc):
        self.display_msg('已启用官方轮换，不再做轮换')
        if self.official_change_fodder:
            return

        if self.change_fodder is False:
            self.display_msg('未开启更换狗粮，建议锁定式神效率更高')
            self.click_loc_one_and_move_uncover(loc)
            return

        if self.is_captain:
            # 组队时，队长的位置信息会变化
            if self.players == 1:
                self.preinstall_locs = self.captain_preinstall_locs
                self.exchange_locs = self.captain_exchange_locs
            else:
                self.preinstall_locs = self.captain_team_preinstall_locs
                self.exchange_locs = self.captain_team_exchange_locs
        else:
            # 队员用的是单人组队时队长的位置信息
            self.preinstall_locs = self.captain_preinstall_locs
            self.exchange_locs = self.captain_exchange_locs

        im_yys = self.screenshot_exact()
        if self.locate_im(self.get_image('change_fodder'), im_yys):
            self.display_msg('误触进入狗粮更换界面，退出重新更换')
            loc_tmp = self.locate_im(self.get_image('back'))
            if loc_tmp:
                self.click_loc_one_and_move_uncover(loc_tmp)

        # 预设界面：刚进入挑战，含有预设的界面
        self.__check_preinstall_man(loc)  # 预设界面，确认是否需要更换狗粮
        if self.__check_need_change(loc):  # 狗粮界面，再次确认是否需要更换狗粮
            self.__change_fodder(loc)

    def init_drag_status(self):
        self.drag_times = 0
        self.drag_left = False

    def fox_drag(self, loc):
        im_yys = self.screenshot_exact()
        print('loc tmp 进去')
        loc_tmp = self.locate_im(self.get_image('chapter_award_box'),im_yys)
        print('loc tmp 出来')
        if loc_tmp:
            self.cur_key = 'chapter_award_box'
            self.click_loc_one_and_move_uncover(loc_tmp)
            return
        else:
            print('no award yet active fox_callback')
            # loc_tmp = self.locate_im(self.get_image('fox'))
            self.cur_key = 'fox'
            max_drag_times = 4
            
            start_x,start_y = loc
            self.drag_rel(start_x,start_y)
            if self.drag_times < max_drag_times:
                self.drag_times += 1
            elif self.drag_left is False:
                self.drag_times = 0  # 重新开始计数
                self.drag_left = True
            else:
                self.display_msg('左右来回各拖动了5次，依然没有找到妖怪，正在退出')
                self.stop = True
                return

    def empty_monster_callback(self, loc):
        print('active empty_monster_callback')
        # 队员时不需要拖动界面
        # if self.is_member:
        #     return

        # # 最多往右拉6次，之后再往左拉6次
        max_drag_times = 10
        # if self.drag_times < max_drag_times:
        #     self.drag_times += 1
        # elif self.drag_left is False:
        #     self.drag_times = 0  # 重新开始计数
        #     self.drag_left = True
        # else:
        #     self.display_msg('左右来回各拖动了10 次，依然没有找到妖怪，正在退出')
        #     self.stop = True
        #     return

        # loc_tmp = self.locate_im(self.get_image('monster_found'))
        # if loc_tmp:
        #     self.cur_key = 'monster_found'
        #     self.display_msg('恭喜你成功发现史前妖怪，图鉴+1！')
        #     self.click_loc_one_and_move_uncover(loc_tmp)

        # if self.last_moster_is_boss:
        #     self.display_msg('刚挑战完boss妖怪，此轮不拖动，等待奖励.{0}/{1}'.format(
        #         self.drag_times + 1, max_drag_times))
        #     return

        # # 移动到比较安全的拖拉位置（安全区域）
        random_x = uniform(0.2 * self.window.win_width,
                           0.4 * self.window.win_width)
        random_y = uniform(0.4 * self.window.win_height,
                           0.6 * self.window.win_height)

        if self.drag_left is False:
            # 往右拉时，
            self.drag_rel(random_x, random_y, random_x - 250, random_y)
            self.display_msg('向左拖拉，以显示右侧的小怪, {0}/{1}'.format(
                self.drag_times + 1, max_drag_times))
        else:
            self.drag_rel(random_x, random_y, random_x + 300, random_y)
            self.display_msg('向右拖拉，以再次显示左侧的小怪, {0}/{1}'.format(
                self.drag_times + 1, max_drag_times))


if __name__ == '__main__':
    autogui = Chapter()
    autogui.run('chapter')
    logger.debug(str(autogui.prepare_image_callback))
    logger.debug(str(autogui.loop_image_callback))
