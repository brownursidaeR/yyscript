#!/usr/bin/python
# -*- coding: utf-8 -*

# %% 先加载对应的库
import screenshot
from conf.yysconfig import YysConfig
import os
import sys
import time
import pyautogui
from PIL import ImageGrab
import logging
from win_gui import Yys_windows_GUI
from PyQt5.QtCore import pyqtSignal, QThread
from random import randint, uniform
import numpy as np
import cv2
import random
# SIFT = cv2.xfeatures2d.SIFT_create()
SIFT = cv2.SIFT_create()

# 将上一层目录添加到系统目录
cur_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
par_dir = os.path.split(os.path.abspath(cur_dir))[0]
sys.path.append(cur_dir)  # 打包时会放在同一个目录下，所以如果是加父的目录是不行的
sys.path.append(par_dir)
logger = logging.getLogger('kiddo')

# 使用opencv的图片匹配函数，如果不想用opencv可以使用 screenshot_pil.py 脚本

locate = screenshot.locate_image_cv2pil
YysScreenshot = screenshot.YysScreenshot


def ComputeScreenShot(screenShot):
    screenShot = cv2.cvtColor(screenShot, cv2.COLOR_BGR2GRAY)
    # CV_U8
    kp2, des2 = SIFT.detectAndCompute(screenShot, None)
    return kp2, des2


def GetLocation(target, kp2, des2):
    """
    获取目标图像在截图中的位置
    :param target:
    :param screenShot:
    :return: 返回坐标(x,y) 与opencv坐标系对应
    """
    MIN_MATCH_COUNT = 5
    img1 = target # cv2.cvtColor(target,cv2.COLOR_BGR2GRAY)# 查询图片 ##target   
    # img2 = cv2.resize(img2, dsize=None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
    # 用SIFT找到关键点和描述符

    kp1, des1 = SIFT.detectAndCompute(img1, None)
    # kp_1, desc_1 = sift.detectAndCompute(original, None)
    # kp_2, desc_2 = sift.detectAndCompute(image_to_compare, None)
    # FLANN_INDEX_KDTREE = 0
    # index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=4)
    # search_params = dict(checks=50)
    
    # flann = cv2.FlannBasedMatcher(index_params, search_params)
    matcher = cv2.DescriptorMatcher_create("BruteForce")
    matches = matcher.knnMatch(des1, des2, k=2)
    print('new matches apply')
    # matches = flann.knnMatch(des1, des2, k=2)
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    # result = cv2.drawMatches(screenShot, kp_1, target, kp_2, good, None)

    print(len(good))
    if len(good) >= MIN_MATCH_COUNT:
        print('in?in?in?in?in?in?in?in?in?in?in?in?in?')
        src_pts = np.float32(
            [kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32(
            [kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()
        h, w = img1.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1],
                         [w - 1, 0]]).reshape(-1, 1, 2)
        if M is not None:
            dst = cv2.perspectiveTransform(pts, M)
            arr = np.int32(dst)  #
            midPosArr = arr[0] + (arr[2] - arr[0]) // 2
            midPos = (midPosArr[0][0], midPosArr[0][1])
            return midPos
        else:
            print('这里return了11111111111111111111')
            return None
    else:
        print('这里return了2222222222222222')
        return None


def CheatPos(originPos, factor, direction):  # direction:12 横竖
    """
    对原始点击坐标进行随机偏移，防止封号
    :param originPos:原始坐标
    :return:
    """
    if direction == 1:
        x, y = random.randint(-factor, factor), random.randint(-factor, factor)
        newPos = (originPos[0] + x, originPos[1])
        return newPos
    elif direction == 2:
        x, y = random.randint(-factor, factor), random.randint(-factor, factor)
        newPos = (originPos[0], originPos[1]+y)
        return newPos
    else:
        x, y = random.randint(-factor, factor), random.randint(-factor, factor)
        newPos = (originPos[0] + x, originPos[1] + y)
        return newPos


def Click(targetPosition):
    """4
    点击屏幕上的某个点
    :param targetPosition:
    :return:
    """
    if targetPosition is None:
        print('未检测到目标')
    else:
        pyautogui.moveTo(targetPosition, duration=0.20)
        pyautogui.click()


class ImageCallback():
    def __init__(self, key, image, callback):
        self.key = key  # 回调函数
        self.image = image  # 图片文件
        self.callback = callback  # 回调函数


class Autogui(QThread):
    # 定义类属性为信号函数
    sendmsg = pyqtSignal(str, str)  # type, msg

    def __init__(self, win_name=None, yys_config=None):  # '阴阳师-网易游戏'
        super(Autogui, self).__init__(None)  # 初始化信号和槽的初始化
        self.win_name = win_name
        self.window = Yys_windows_GUI(self.win_name)
        # self.auto_type  # 当前执行的脚本类型，在外层设置
        self.config = yys_config
        self.init_config()  # 获取配置
        self.init_screenshot()  # 获取截图信息
        self.prepare_image_callback = []  # ImageCallback
        self.loop_image_callback = []  # ImageCallback
        self.stop = False  # 是否停止脚本
        self.cur_key = ''  # 当前匹配的key，用来输出日志
        self.cur_loop_times = 0  # 当前循环数
        self.last_key = ''  # 上一次循环的key，用来检测死循环
        self.safety_loc_click_times = 0  # 安全区域点击了多少次
        self.max_excute_time = self.config.general['max_excute_time']
        # 单个 key 连续匹配的最大次数，prepare 和 time 翻倍
        self.max_serial_key_times = self.config.general['max_serial_key_times']

    def init_config(self):
        if hasattr(self, 'config') and self.config is not None:
            self.display_msg('参数已经初始化完成')
            self.display_msg(str(self.config))
            return

        yys_config = YysConfig()
        if yys_config.is_read_file_success() is False:
            self.display_msg('配置解析失败')
            exit(1)
        self.config = yys_config
        self.init_logging_level()

    def init_logging_level(self):
        self.display_msg('程序正在初始化日志文件！')
        configs = self.config.general
        level = configs.get('log_level', 'INFO')
        if level == 'NONE':
            return
        elif level == 'INFO':
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.DEBUG)

        # BASIC_FORMAT= '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
        BASIC_FORMAT = '%(asctime)s - %(levelname)s: %(message)s'
        DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
        chlr = logging.StreamHandler()  # 输出到控制台的handler
        chlr.setFormatter(formatter)
        fhlr = logging.FileHandler('debug.log', 'a+')  # 输出到文件的handler
        fhlr.setFormatter(formatter)

        debug_log_bak = 'debug.log.bak'
        debug_log = 'debug.log'
        if os.path.exists(
                debug_log) and os.path.getsize(debug_log) > 10 * 1024 * 1024:
            os.remove(debug_log_bak)
            os.rename(debug_log, debug_log_bak)
            with open(debug_log) as fd:
                logger.debug('超过10M时，重新打开文件 debug.log: fd={0}'.format(fd))
        logger.addHandler(chlr)
        logger.addHandler(fhlr)

    def init_screenshot(self):
        self.screenshot = YysScreenshot('')

    def already_in_loop(self, im_yys):
        if len(self.prepare_image_callback) == 0:
            self.display_msg('默认状态就是可循环状态')
            return True

        if im_yys is None:
            im_yys = self.screenshot_exact()
        for callback in self.loop_image_callback:
            res = self.locate_im(callback.image, im_yys)
            if res:
                print(res)
                self.display_msg('匹配{0}，可以进入循环'.format(callback.key))
                return True
            else:
                print(res)
        self.display_msg(self.cur_key + ': 当前状态还不能进入到可循环状态')
        return False

    def stop_run(self):
        self.stop = True

    def run(self, auto_type='none'):
        self.auto_type = auto_type
        # 不检测窗体
        self.display_msg('当前窗体位置: {0}*{1}'.format(self.window.x_top,
                                                  self.window.y_top))
        if (self.window.win_width != self.config.general['width'] or
                self.window.win_height != self.config.general['height']):
            self.display_msg('当前窗体大小: {0}*{1}, 预期大小：{2}*{3}'.format(
                self.window.win_width, self.window.win_height,
                self.config.general['width'],
                self.config.general['height']))
            self.display_msg('--当前窗体大小和配置值不同，请谨慎使用！--\n' * 5)
            time.sleep(5)

        self.display_msg('正在尝试进入循环')
        if self.goto_loop() is False:
            self.display_msg('无法进入循环，请确认当前选择的功能后，再重新启动功能')
            return

        self.display_msg('成功进入循环脚本，正在打印当前功能的配置信息...')
        # 配置太多,仅输出到文件到
        # self.display_msg(str(self.config.cur_config))  # 打印配置信息
        with open('debug.log', 'a+') as fd:
            fd.write(str(self.config.cur_config))
        self.loop()

    def goto_loop(self):
        self.cur_loop_times = 0
        while self.stop is False and self.cur_loop_times < self.pre_loop_times:
            im_yys = self.screenshot_exact()
            found = False
            if self.already_in_loop(im_yys):
                return True

            im_yys = self.screenshot_exact()  # 执行操作之后需要重新获取截图
            for callback in self.prepare_image_callback:
                self.cur_loop_times += 1

                loc = self.locate_im(callback.image, im_yys)
                if loc is None:
                    logger.debug('{0} not match'.format(callback.key))
                    continue
                self.cur_key = callback.key
                new_pos = CheatPos(loc, random.randint(0, 3), 1)
                Click(new_pos)
                # callback.callback(loc)  # 执行对应的回调
                time.sleep(1)
                found = True
                break

            if found is False:
                time.sleep(1)
        return False

    def loop(self):
        self.cur_loop_times = 0
        not_match_times = 0  # 连续达到 100 次没有匹配就退出
        start_time = time.time()  # 启动时间
        cur_serial_key_times = 0

        while self.stop is False and self.cur_loop_times < self.loop_times:
            # 保护机制一：最大运行时间
            if time.time() - start_time > self.max_excute_time * 60:
                self.display_msg('程序运行总时长超时最大限制，正在退出')
                self.stop = True
                continue

            # 保护机制一：单个 key 循环次数
            if cur_serial_key_times > self.max_serial_key_times * 2:
                self.display_msg('{0}特殊key达到两倍单个key已经超过最大次数：{1}'.format(
                    self.cur_key, cur_serial_key_times * 2))
                self.stop = True
                continue

            elif cur_serial_key_times > self.max_serial_key_times:
                if self.cur_key not in ['prepare', 'time']:
                    self.display_msg('{0}key达到单个key已经超过最大次数：{1}'.format(
                        self.cur_key, cur_serial_key_times))
                    self.stop = True
                    continue

            im_yys = self.screenshot_exact()
            found = False

            im_yys = self.screenshot_exact()  # 执行操作之后需要重新获取截图
            # im_yys.show()
            for callback in self.loop_image_callback:
                if callback.image is None:
                    self.display_msg('请确认截图{}存在'.format(callback.key))
                    continue
                # GetLocation(obj, kp2, des2)
                loc = GetLocation(callback.image, im_yys[0], im_yys[1])
                if loc is None:
                    # print('loc is None')
                    continue
                not_match_times = 0  # 匹配上之后，初始化不匹配的次数
                self.display_msg('该轮匹配到图片：{0}'.format(callback.key))
                self.last_key = self.cur_key
                self.cur_key = callback.key
                # 统计 key 连续出现的次数
                cur_serial_key_times = 0 if self.last_key != self.cur_key else (
                    cur_serial_key_times + 1)
                new_pos = CheatPos(loc, random.randint(0, 3), 1)
                try:
                    callback.callback(loc)  # 执行对应的回调
                    print('执行对应的回调')
                except Exception as e:
                    self.display_msg('这里excep了，报错如下%s'%e)
                    print('这里excep了，报错如下%s'%e)
                    Click(new_pos)
                
                time.sleep(0.5)
                print('found!')
                found = True
                break

            if found is False:
                # self.display_msg('该轮匹配不到图片，等待下一轮匹配，非问题')
                time.sleep(1)

            # 保护机制三：不匹配次数达到一定值
            not_match_times += 1
            if not_match_times % 20 == 0:
                self.display_msg('连续超过 {0} 次没有匹配没有匹配到图片'.format(not_match_times))
                if not_match_times > 40:
                    screen = ImageGrab.grab()
                    screen.save('卡住了在这里!!!!!!.jpg')
                    self.display_msg('超过 300 次，正在退出')
                    self.stop = True
        self.display_msg('已经完成所有挑战次数，正在退出')

        # TODO: 统一关闭加成

        # 挑战完成，退出结算界面
        time.sleep(2)
        loc = self.locate_im(self.get_image('award'))
        if loc:
            self.display_msg('最后退出时，退出结算界面')
            self.award_callback(loc)

    def raise_msg(self, msg):
        '''输出日志到框内，且弹窗提醒错误'''
        logger.warn(msg)
        self.sendmsg.emit(msg, 'Error')

    def display_msg(self, msg):
        '''输出日志到框内'''
        logger.info(msg)
        self.sendmsg.emit(msg, 'Info')

    def get_window_handler(self):
        '''成功获取句柄时，返回True,否则返回None'''
        # hwnd = self.config.general['win_hwnd']
        # if hwnd == -1:
        #     return self.window.get_window_handler()
        # else:
        #     if self.window.get_handler_state(hwnd):
        #         self.display_msg('请确认窗体名称是否正确：{0}'.format(
        #             self.window.win_name))
        #         return True
        #     else:
        #         self.display_msg('通过 hwnd 获取窗体失败，正在使用窗体名称重新获取')
        #         return self.window.get_window_handler()
        return True

    def resize_window_size(self, width, height):
        return self.window.resize_window_size(width, height)

    def get_image(self, key):
        '''
            调试时打印： screenshot.show_cv2_image
        '''
        image = self.screenshot.get_jpg(key)
        if image is None:
            self.display_msg('can\'t not found ' + key)
        return image

    def init_image_callback(self, prepare_callback, loop_callback):
        '''格式化图片文件及对应的callback'''
        for each_callback in prepare_callback:
            callback = ImageCallback(each_callback[0],
                                     self.get_image(each_callback[0]),
                                     each_callback[1])
            self.prepare_image_callback.append(callback)
        for each_callback in loop_callback:
            callback = ImageCallback(each_callback[0],
                                     self.get_image(each_callback[0]),
                                     each_callback[1])
            self.loop_image_callback.append(callback)

    def screenshot_exact(self, x=0, y=0, w=0, h=0):
        '''默认截取yys整个页面，成功返回截图，失败返回None
            要打印时，用 im.show()
        '''
        # print(x,y,w,h)
        try:
            window = Yys_windows_GUI(None)
            window.get_window_handler()
            im = window.get_screenshot()
            # im.show()
            # 为了优化速度，把计算屏幕截图的特征提取出来，避免重复运算
            kp2, des2 = ComputeScreenShot(im)
            # im.save('test2.png')
            return kp2, des2

        except Exception as error:
            self.display_msg('截图失败：' + str(error))
            window = Yys_windows_GUI(None)
            window.get_window_handler()
            im = window.get_screenshot()
            kp2, des2 = ComputeScreenShot(im)
            print('卡这里3')
            # im.save('test3.png')
            return kp2, des2

    def screenshot_inc(self, x=0, y=0, w=0, h=0):
        '''默认截取yys相对位置，成功返回截图，失败返回None'''
        w = w if w != 0 else self.window.win_width
        h = h if h != 0 else self.window.win_height
        return self.screenshot_exact(x, y, w, h)

    def locate_im(self, check_im, im_yys):
        # im_yys = self.screenshot_exact()
        # print('看看其他的im_yys',im_yys)
        '''检查图片是否存在, (Image, Image) -> loc or None'''
        try:
            loc = GetLocation(check_im, im_yys[0], im_yys[1])
            print(loc)
            return loc
        except Exception as error:
            print('截图比对失败except了')
            self.display_msg('截图比对失败：' + str(error))
            return None

    def locate_im_exact(self, check_im, im_yys):
        '''通过坐标来获取截图并查看图片是否存在'''
        try:
            loc = GetLocation(check_im, im_yys[0], im_yys[1])
            return loc
        except Exception as error:
            self.display_msg('截图比对失败：' + str(error))
            return None

    def locate_im_inc(self, check_im, x, y, w, h):
        '''通过坐标来获取截图并查看图片是否存在'''
        return self.locate_im_exact(check_im, x, y, w, h)

    def locate_ims(self, check_ims):
        '''检验一组图片截图是否在界面当中，存在时返回对应的 loc'''
        im_yys = self.screenshot_exact()
        for im in check_ims:
            loc = self.locate_im(im, im_yys)
            if loc:
                return loc
        return None

    def show_im_by_inc(self, x, y, w, h):
        '''调试时使用，用来获取窗体的位置信息'''
        im_yys = self.screenshot_inc(x, y, w, h)
        im_yys.show()

    def show_im_by_loc(self, loc):
        '''调试时使用，用来获取窗体的位置信息'''
        im_yys = self.screenshot_inc(loc.left, loc.top, loc.width, loc.height)
        im_yys.show()

    def show_np_im_by_key(self, key):
        '''调试时使用，用来获取图片库的信息'''
        np_im = self.get_image(key)
        if np_im is not None:
            self.screenshot.show_jpg(key)
        else:
            self.display_msg('在图片库中没有找到图片：{0}'.format(key))

    # %% 移动鼠标(0.5S)，取截图位置的偏中间位置，并触发鼠标点击，点击2次，间隔随机0-1S

    def click_loc(self, loc, times=-1):
        random_x = uniform(loc.width * 0.35, loc.width * 0.75)
        random_y = uniform(loc.height * 0.35, loc.height * 0.75)
        interval = uniform(0.2, 0.5)
        # click_x = self.window.x_top + loc.left + random_x
        # click_y = self.window.y_top + loc.top + random_y
        # self.click_loc_exact(click_x, click_y, times, interval)
        self.click_loc_inc(loc.left + random_x, loc.top + random_y, times,
                           interval)

    def click_loc_exact(self, click_x, click_y, times=-1, interval=0.5):
        if times == -1:
            times = randint(2, 3)
        random_dis = uniform(-0.5, 0.5)
        click_x += random_dis
        click_y += random_dis
        self.display_msg('点击位置"{4}"进入下一步：({0:.2f},{1:.2f},{2:.2f},{3})'.format(
            click_x, click_y, interval, times, self.cur_key))
        self.window.click_loc_inc_by_handler(int(click_x), int(click_y))

    def click_loc_inc(self, inc_x, inc_y, times=-1, interval=0.5):
        '''点击阴阳师界面的相对位置'''
        click_x = self.window.x_top + inc_x
        click_y = self.window.y_top + inc_y
        self.display_msg('点击位置"{4}"进入下一步：({0:.2f},{1:.2f},{2:.2f},{3})'.format(
            click_x, click_y, interval, times, self.cur_key))

        for i in range(times):
            # 调试使用
            # im = self.screenshot_inc(click_x, click_y, 10, 20)
            # im.save('{0}_{1:.0f}.jpg'.format(self.cur_key, time.time()))
            # 通过 handler 点击
            self.window.click_loc_inc_by_handler(int(inc_x), int(inc_y))
            time.sleep(0.5)

    def click_loc_one(self, loc):
        self.click_loc(loc, 1)

    def click_loc_twice(self, loc):
        self.click_loc(loc, 1)
        time.sleep(0.3)
        self.click_loc_one_and_move_uncover(loc)

    def click_enlarge_loc_one(self, loc, width_mul=1.5, height_mul=1.5):
        '''放大一定倍数之后再点击，必须大于1，否则会出问题'''
        new_loc = loc
        new_loc.left = loc.left - loc.width * (width_mul - 1) / 2
        new_loc.top = loc.top - loc.height * (height_mul - 1) / 2
        new_loc.width = loc.width * width_mul
        new_loc.height = loc.height * height_mul
        self.click_loc(new_loc, 1)

    def click_enlarge_loc_one_20_10(self, loc):
        '''长宽各扩大2倍'''
        self.click_enlarge_loc_one(loc, 2.0, 1.0)

    def click_enlarge_loc_one_20_20(self, loc):
        '''长宽各扩大2倍'''
        self.click_enlarge_loc_one(loc, 2.0, 2.0)

    def click_enlarge_loc_one_25_25(self, loc):
        '''长宽各扩大2.5倍'''
        self.click_enlarge_loc_one(loc, 2.5, 2.5)

    def click_enlarge_loc_one_30_20(self, loc):
        '''长宽各扩大3倍和2倍'''
        self.click_enlarge_loc_one(loc, 3, 2)

    def click_enlarge_loc_one_60_12(self, loc):
        '''长宽各扩大6倍和1.2倍'''
        self.click_enlarge_loc_one(loc, 6, 1.2)

    def move_uncover(self, loc):
        random_x = uniform(-2.0 * loc.width, -1.0 * loc.width)
        random_y = uniform(-2.0 * loc.height, -1.0 * loc.height)
        interval = uniform(0.1, 0.5)
        move_x = self.window.x_top + loc.left + random_x
        move_y = self.window.y_top + loc.top + random_y
        self.display_msg('偏移位置以防遮挡：({0:.2f},{1:.2f})'.format(move_x, move_y))
        pyautogui.moveTo(move_x, move_y, duration=interval)

    def click_loc_one_and_move_uncover(self, loc):
        print(loc)
        self.click_loc(loc, 1)
        # self.move_uncover(loc)

    def click_loc_one_and_sleep(self, loc, seconds=2):
        self.click_loc(loc, 1)
        time.sleep(seconds)

    def move_loc_exact(self, move_x, move_y, interval=0):
        interval = interval if interval != 0 else uniform(0.1, 0.5)
        self.display_msg('移动位置到：({0:.2f},{1:.2f})'.format(move_x, move_y))
        pyautogui.moveTo(move_x, move_y, duration=interval)

    def move_loc_inc(self, move_x, move_y, interval=0):
        '''移动相对于主界面的相对位置'''
        interval = interval if interval != 0 else uniform(0.1, 0.5)
        self.display_msg('移动位置到：({0:.2f},{1:.2f})'.format(move_x, move_y))
        pyautogui.moveTo(self.window.x_top + move_x,
                         self.window.y_top + move_y,
                         duration=interval)

    def scroll_loc_exact(self, clicks, move_x=0, move_y=0):
        '''滚动接口调用之后点击位置会不准
            clicks 参数表示滚动的格数。
            正数则页面向上滚动
            负数则向下滚动
        '''
        self.display_msg('滚动鼠标幅度：{0}'.format(clicks))
        pyautogui.scroll(clicks=clicks, x=move_x, y=move_y)

    # def dragRel_loc_exact(self, x_offset, y_offset, du=0.5):
    #     '''
    #         @x_offset： 正数为按住一个点向右拖动，负数按住一个点向左拖动
    #         @y_offset： 正数为按住一个点向下拖动，负数按住一个点向上拖动，大小表示拖动幅度
    #         @du, 表示拖动使用的时间间隔滚动
    #     '''
    #     self.display_msg('拖动鼠标幅度：{0:.2f}, {1:.2f}'.format(x_offset, y_offset))
    #     pyautogui.dragRel(x_offset, y_offset, duration=du)

    def drag_rel(self, start_x, start_y, duration=0.5):
        print('auto_gui_drag')

        '''拖拉鼠标，从A点到B点
            界面向左拖动的话，应该是 end_x < start_x, 显示右侧的空间
            界面向右拖动的话，应该是 end_x > start_x, 显示左侧的空间
        '''
        self.display_msg('拖拉鼠标幅度：{0:.2f}, {1:.2f}'.format(
            start_x, start_y))
        self.window.drag_rel(start_x, start_y, duration)

    def void_callback(self, loc):
        self.display_msg('识别到{0}：进行空操作，并等待1S'.format(self.cur_key))
        time.sleep(1)

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

        # 确定
        # TODO: 还需要忽略妖气挑战时的邀请，没截到图，所以先不添加
        if self.locate_im(self.get_image('break_invite')):
            self.display_msg('结界邀请时不点击接受')
        elif self.locate_im(self.get_image('monster_invite')):
            self.display_msg('妖怪挑战邀请时不点击接受')
        elif self.locate_im(self.get_image('juexing_invite')):
            self.display_msg('收到接受觉醒组队的邀请')
            self.click_loc_one(loc)
        else:
            # 其他确定的场景
            self.click_loc_one(loc)

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

    def prepare_callback(self, loc):
        self.click_loc_one_and_move_uncover(loc)
        time.sleep(1)
        self.wait_keys(['prepare'], self.prepare_callback)

    def continue_callback(self, loc):
        self.click_loc_one_and_move_uncover(loc)
        time.sleep(2)

    def click_safely_loc(self, loc):
        '''安全点击指定区域
            安全区域： 1. 界面右侧
           参数信息： loc 没有用上，保持回调格式一致
        '''
        right_safely_box = [1040, 180, 70, 290]

        # 选择点击区域
        selected_box = right_safely_box
        one_loop_click_times = 6

        self.safety_loc_click_times += 1
        self.safety_loc_click_times %= (one_loop_click_times * 3)

        # 触发随机点击
        loc_tmp = screenshot.Location(selected_box[0], selected_box[1],
                                      selected_box[2], selected_box[3])
        if self.cur_key in ['fail', 'victory', 'award']:
            self.click_loc_twice(loc_tmp)
        else:
            self.click_loc_one(loc_tmp)

    def victory_callback(self, loc):
        self.display_msg('当前进度：{0}/{1}'.format(self.cur_loop_times + 1,
                                               self.loop_times))
        self.click_loc_one_and_move_uncover(loc)
        time.sleep(0.3)
        self.click_loc_one_and_move_uncover(loc)
        time.sleep(0.8)
        if self.last_key != self.cur_key:
            self.cur_loop_times += 1

    def fail_callback(self, loc):
        self.click_loc_one_and_move_uncover(loc)
        time.sleep(0.3)
        self.click_loc_one_and_move_uncover(loc)
        time.sleep(1.5)

    def award_callback(self, loc):
        self.click_loc_one_and_move_uncover(loc)
        time.sleep(0.3)
        self.click_loc_one_and_move_uncover(loc)
        time.sleep(0.8)

    def wait_keys(self, keys, callback, wait_times=2):
        '''每隔 1s 检查 key 是否出现，重复等待 wait_times
            callback 的回调必须是一个传入位置信息的回调函数
        '''
        self.display_msg('wait_keys: {0}, 次数：{1}'.format(keys, wait_times))
        for i in range(wait_times):
            im_yys = self.screenshot_exact()
            for key in keys:
                loc_tmp = self.locate_im(self.get_image(key), im_yys)
                if loc_tmp:
                    self.display_msg('wait_keys: 命中了：{0}'.format(key))
                    self.cur_key = key
                    callback(loc_tmp)
                    return
            time.sleep(1)  # 先 sleep 再等待

    def wait_no_keys(self, keys, callback, wait_times=2):
        '''每隔 1s 检查 key 是否出现，重复等待 wait_times
            callback 的回调必须是一个传入位置信息的回调函数
        '''
        self.display_msg('wait_no_keys: {0}, 次数：{1}'.format(keys, wait_times))
        for i in range(wait_times):
            im_yys = self.screenshot_exact()
            for key in keys:
                loc_tmp = self.locate_im(self.get_image(key), im_yys)
                if loc_tmp is None:
                    self.display_msg('wait_no_keys: 没有命中了：{0}'.format(key))
                    callback(loc_tmp)
                    return
            time.sleep(1)

    def fight_callback(self, loc):
        pass

    def is_inc_box_has_key(self, key, x, y, w, h):
        return self.locate_im_inc(self.get_image(key), x, y, w, h) is not None

    def get_all_images(self, key, im_yys=None, confidence=0.8):
        if im_yys is None:
            im_yys = self.screenshot_exact()
        locs = screenshot.locate_im_cv2pil(self.get_image(key),
                                           im_yys,
                                           confidence,
                                           multi_loc=True)
        if locs is None:
            return 0
        else:
            return locs

    def change_fodder_type(self, fodder_type: str):
        im_yys = self.screenshot_exact()
        loc_tmp = self.locate_im(self.get_image(fodder_type), im_yys)
        if loc_tmp:
            self.display_msg('已经是选中的狗粮类型')
            return

        # ex_xxx 是交替界面的 sp, sp 点击交替之后的截图，目前就 sp 不通用
        # 调出选择类型的界面
        all_types = [
            'all', 'fodder', 'ncard', 'rcard', 'srcard', 'ssrcard', 'spcard',
            'ex_sp'
        ]
        all_types.remove(fodder_type)
        for each in all_types:
            loc_tmp = self.locate_im(self.get_image(each), im_yys)
            if loc_tmp:
                self.click_loc_one(loc_tmp)
                time.sleep(1)
                break

        # 具体去指定类型
        im_yys = self.screenshot_exact()
        loc_tmp = self.locate_im(self.get_image(fodder_type), im_yys)
        if loc_tmp:
            self.click_loc_one(loc_tmp)
            self.display_msg('切换到选中的狗粮类型')

    def move_button(self, im_yys=None, drag=10):
        '''狗粮的条拖动一定距离'''
        if im_yys is None:
            im_yys = self.screenshot_exact()
        loc_tmp = self.locate_im(self.get_image('move_button'), im_yys)
        if loc_tmp:
            random_x = uniform(0, 5)
            random_y = uniform(0, 5)
            start_x = loc_tmp.left + random_x
            start_y = loc_tmp.top + random_y
            self.drag_rel(start_x, start_y, start_x + drag, start_y)

    def move_button_to_safe_fodder(self, drag=10):
        im_yys = self.screenshot_exact()
        loc_tmp = self.locate_im(self.get_image('prepare'), im_yys)
        if loc_tmp is None:
            self.display_msg('不是交换界面，不需要进行拖动')

        # 拖动一定距离，直到折叠情况下也看不到红蛋，说明拖动的距离到位了
        while True:
            im_yys = self.screenshot_exact()
            loc_red_egg = self.locate_im(self.get_image('red_egg'), im_yys)
            if loc_red_egg and drag > 0:
                self.move_button(im_yys, drag)  # 还需要继续拖动
                time.sleep(0.5)
                continue
            else:
                # 存在狗粮是正在挑战中时，也要进行看拖动
                loc_tmp = self.locate_im(self.get_image('fodder_already_in'),
                                         im_yys)
                if loc_tmp and drag > 0:
                    self.move_button(im_yys, drag)  # 还需要继续拖动
                    time.sleep(0.5)
                    continue
                break

    def exchange_fodder(self, locations: list, drag=10):
        # 每次仅交换一只式神
        for i in range(len(locations)):
            # 更换大于2个狗粮时可能会因为前面两个交替互换导致交换异常
            self.move_button_to_safe_fodder(drag)
            im_yys = self.screenshot_exact()
            flower_loc = self.locate_im(self.get_image('flower'), im_yys)
            if flower_loc:
                random_x = randint(-5, 5)
                random_y = randint(-5, 5)
                start_x = flower_loc.left - 50 + random_x
                start_y = flower_loc.top + 80 + random_y
                end_x = locations[i].left + random_x
                end_y = locations[i].top + 40 + random_y

                self.display_msg('drag from ({0},{1}) to ({2},{3})'.format(
                    start_x, start_y, end_x, end_y))
                self.drag_rel(start_x, start_y, end_x, end_y, 2)
                return

    def get_all_images_by_locs(self, keys, locs, try_times=2):
        '''从各个locs数组中获取到，key 对应的图片的位置信息
            key 是指要查找的图片字符串
            locs 是指每个矩形框的四个要素： 相对的 x_left, x_top, x_width, x_height
            try_times 指总共要进行几次判断，因为可能存在前后匹配，因为匹配多次结果可能不同，假设前后两次结果相同，即可返回
        '''
        pre_match = []  # 上一轮匹配状态
        cur_match = []  # 当前匹配的状态
        for try_time in range(try_times):
            cur_match = []  # 每一轮开始时都为空
            for i in range(len(locs)):
                im_tmp = self.screenshot_inc(locs[i][0], locs[i][1],
                                             locs[i][2], locs[i][3])
                # 降低一下匹配率，更容易命中
                loc_tmp = None
                key = ''
                for key in keys:
                    loc_tmp = self.locate_im(self.get_image(key),
                                             im_tmp,
                                             confidence=0.6)
                    if loc_tmp:
                        break

                if loc_tmp:
                    self.display_msg('第{2}轮，第{0}个位置含有key:{1}'.format(
                        i + 1, key, try_time + 1))
                    loc_tmp.left += locs[i][0]
                    loc_tmp.top += locs[i][1]
                    cur_match.append(loc_tmp)
                else:
                    # 调试使用
                    # im_tmp.show()
                    # if 'ex_man' in keys or 'man' in keys:
                    #     im_tmp.save('{0}_{1:.0f}.jpg'.format(
                    #         self.cur_key, time.time()))
                    pass

            if (try_time == 0 and len(cur_match) == 0):
                # 首次匹配为 0 时， CD 一秒后再次匹配
                self.display_msg('首轮匹配为空，继续匹配一轮进行确认')
            else:
                # 至少匹配两轮，如果本轮跟前一轮结果一样，即可返回了
                if len(cur_match) == len(pre_match):
                    self.display_msg('匹配{0}总数：{1}'.format(
                        keys, len(cur_match)))
                    return cur_match
                pre_match = cur_match
            time.sleep(1)
        return cur_match
