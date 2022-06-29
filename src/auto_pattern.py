#!/usr/bin/python
# -*- coding: utf-8 -*

# %% 先加载对应的库
import os
import sys
import time
import logging

if __name__ == "__main__":
    cur_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
    sys.path.append(os.path.join(cur_dir, 'autogui'))
    sys.path.append(os.path.join(cur_dir, 'conf'))
logger = logging.getLogger('kiddo')

from autogui import Autogui, ImageCallback


class Pattern(Autogui):
    def __init__(self, win_name='阴阳师-网易游戏', yys_config=None):
        Autogui.__init__(self, win_name, yys_config)
        # 设置当前副本的类型，设置之后优先查找御灵对应的截图
        self.screenshot.set_current_setion('pattern')  # 设置优先的截图信息
        self.config.set_current_setion('pattern')  # 设置当前配置信息
        self.end_key = self.config.cur_config.get('end_key', '')
        self.pre_loop_times = self.config.cur_config.get('pre_loop_times', 20)
        self.sleep_seconds = self.config.cur_config.get('sleep_seconds', 2)
        self.loop_times = self.config.cur_config.get('loop_times', 500)
        self.loop_keys = self.config.cur_config.get('loop_keys', [])
        self.prepare_keys = self.config.cur_config.get('prepare_keys', [])
        if self.loop_keys == '':
            self.display_msg('正在退出，请先设置loop_keys')
            self.stop = True
            return

        # prepare_callback = [
        #     ('search', self.click_loc_one),
        # ]
        # loop_callback = [
        #     ('victory', self.victory_callback),
        #     ('fail', self.fail_callback),
        #     ('award', self.award_callback),
        # ]
        tmp_generator = zip(self.prepare_keys,
                            [self.click_loc_one_and_move_uncover] *
                            len(self.prepare_keys))
        prepare_callback = [x for x in tmp_generator]
        tmp_generator = zip(self.loop_keys,
                            [self.click_loc_one_and_move_uncover] *
                            len(self.loop_keys))
        loop_callback = [x for x in tmp_generator]
        self.init_image_callback(prepare_callback, loop_callback)

    def click_loc_one_and_move_uncover(self, loc):
        self.click_loc_one(loc)
        print('click_loc_oneclick_loc_oneclick_loc_oneclick_loc_oneclick_loc_one')
        if self.cur_key == self.end_key and self.cur_key != self.last_key:
            self.cur_loop_times += 1
            self.display_msg('识别到结束图片{0}，循环次数+1'.format(self.cur_key))
        # self.show_im_by_loc(loc)
        # self.show_np_im_by_key(self.cur_key)
        time.sleep(self.sleep_seconds)


if __name__ == '__main__':
    autogui = Pattern()
    autogui.window.set_only_getwin(True)
    autogui.run('pattern')
    logger.debug(str(autogui.prepare_image_callback))
    logger.debug(str(autogui.loop_image_callback))
