#!/usr/bin/python
# -*- coding: utf-8 -*

import time
import win32ui
import win32gui
import win32con
import logging
import win32api
from PIL import Image
import pyautogui
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PIL import ImageGrab
import cv2
import numpy
import numpy as np

logger = logging.getLogger('kiddo')

# def get_all_windows(win_name):
#     def print_window(hwnd, extra):
#         if win_name in win32gui.GetWindowText(hwnd):
#             print(win32gui.GetClassName(hwnd), win32gui.GetWindowText(hwnd))

#     win32gui.EnumWindows(print_window, None)

# win_name = '阴阳师-网易游戏'
# get_all_windows(win_name)


class Yys_GUI(QThread):
    # 定义类属性为信号函数
    sendmsg = pyqtSignal(str, str)  # type, msg

    def __init__(self, win_name='阴阳师-网易游戏'):
        self.win_name = win_name
        super(Yys_GUI, self).__init__(None)  # 需要初始化，否则会报异常

    def get_window_handler(self):
        pass

    def resize_window_size(self, width, height):
        pass

    def raise_msg(self, msg):
        '''输出日志到框内，且弹窗提醒错误'''
        logger.warn(msg)
        self.sendmsg.emit(msg, 'Error')

    def display_msg(self, msg):
        '''输出日志到框内'''
        # logger.info(msg)
        print(msg)
        self.sendmsg.emit(msg, 'Info')


class Yys_windows_GUI(Yys_GUI):

    sendmsg = pyqtSignal(str, str)  # type, msg

    def __init__(self, win_name='None', only_getwin=False):
        # 获取窗体的特性
        Yys_GUI.__init__(self, win_name)
        self.handler = None
        self.x_top = self.y_top = self.x_bottom = self.y_bottom = 0
        self.win_width = self.win_height = 0
        self.windows = []  # 过滤出来的窗体
        self.is_fullscreen = False  # 是否是全屏
        self.only_getwin = only_getwin  # 是否只取窗体信息

    def set_only_getwin(self, only_getwin):
        self.only_getwin = only_getwin

    def get_window_handler(self):
        '''获取到阴阳师窗体信息'''
        if self.win_name == 'None':
            print('yes!NOne')
            # 获取屏幕的全屏的分辨率
            width, height = win32api.GetSystemMetrics(
                0), win32api.GetSystemMetrics(1)
            self.x_top, self.y_top = 0, 0
            self.x_bottom, self.y_bottom = width, height
            self.win_width, self.win_height = width, height
            logger.info('使用全屏的分辨率，width:{0}, height:{1}'.format(width, height))
            return True
        # print(win_name)
        handler = win32gui.FindWindow(0, self.win_name)  # 获取窗口句柄
        if handler == 0:
            self.raise_msg('捕获不到程序：' + self.win_name)
            return False

        return self.get_handler_state(handler)

    def get_handler_state(self, handler):
        self.handler = handler
        # try:
        #     # 获取名称
        #     win_name = win32gui.GetWindowText(handler)
        #     if win_name == '':
        #         logger.error('通过句柄获取窗体失败，请输入正确的句柄')
        #         return False

        #     self.win_name = win_name  # 异常报错时还可以通过名称取 hwnd

        #     # 获取窗体位置和大小
        #     self.x_top, self.y_top, self.x_bottom, self.y_bottom = \
        #         win32gui.GetWindowRect(handler)
        #     self.win_width = self.x_bottom - self.x_top
        #     self.win_height = self.y_bottom - self.y_top
        #     self.display_msg('捕获到程序：{0},({1},{2}),{3},{4}'.format(
        #         self.win_name, self.x_top, self.y_top, self.win_width,
        #         self.win_height))

        #     logger.info(
        #         '位置信息：top({0},{1}), bottom({2},{3}), width:{4}, height:{5} '.
        #         format(self.x_top, self.y_top, self.x_bottom, self.y_bottom,
        #                self.win_width, self.win_height))

        # except Exception as error:
        #     logger.error(str(error))
        #     return False
        return True

    def resize_window_size(self, width=800, height=480):
        if self.win_name == 'None' or self.only_getwin:
            return self.get_window_handler()
        '''设置固定大小，方便后续截图和比对，这里比较有限制'''
        if self.get_window_handler() is False:
            self.raise_msg('请确认程序有开启' + self.win_name)
            return False

        # reset win and update win info
        try:
            win32gui.SetWindowPos(self.handler, win32con.HWND_NOTOPMOST,
                                  self.x_top, self.y_top, width, height,
                                  win32con.SWP_SHOWWINDOW)
            self.get_window_handler()
        except Exception as error:
            self.raise_msg('请确认你拥有管理员权限，否则无法重新设置大小，msg:{0}'.format(error))
            return False
        return True

    def click_loc_inc_by_handler(self, cx, cy):
        '''通过handler的相对位置来点击，默认 handler 不为空'''
        # print(cx, cy)
        pyautogui.moveTo((cx, cy), duration=0.20)
        pyautogui.click()
        # 采用直接点击而不是win32api点击，会比较实际
        

    def drag_rel(self, start_x, start_y, seconds=2):
        print('win_gui_drag')
        '''
            鼠标拖拉，从起始坐标，拖拉到终止坐标
            移动鼠标 -> 点击按下 -> 移动鼠标 -> 点击释放
            移动鼠标，先横向移，再纵向移，成功率最高
            seconds 表示分多少秒拖动，实际会略低于这个值，只是一个参考
        '''
        hwnd = self.handler

        # 入参需要是整型，共分为5次移动，用来计算每次要休息多少s，当前定死0.1s
        steps = 2
        early_interval = 0.05
        later_interval = (seconds - 0.3) * 1.0 / steps
        start_x, start_y = int(start_x), int(start_y)
        
        # tmp_x, tmp_y = start_x, start_y
        for i in range(steps):
            pyautogui.moveTo(start_x, start_y, later_interval)
            pyautogui.dragRel(-500,0,3,button='left')
            
        time.sleep(later_interval)

        # # win32api.SendMessage(hwnd, win32con.WM_MOUSEMOVE, 1, win32api.MAKELONG(tmp_x, tmp_y))
        # # time.sleep(0.05)
        # win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, 1,
        #                      win32api.MAKELONG(tmp_x, tmp_y))
        # time.sleep(0.05)

        # for i in range(steps):
        #     # print('from: {0},{1}'.format(tmp_x, start_y), end=' ')
        #     tmp_x += step_x
        #     # print('from: {0},{1}'.format(tmp_x, start_y), end=' ')
        #     win32api.SendMessage(hwnd, win32con.WM_MOUSEMOVE, 1,
        #                          win32api.MAKELONG(tmp_x, start_y))
        #     time.sleep(early_interval)
        # # 消除小数点差异
        # win32api.SendMessage(hwnd, win32con.WM_MOUSEMOVE, 1,
        #                      win32api.MAKELONG(end_x, start_y))
        # time.sleep(early_interval)

        # for i in range(steps):
        #     # print('from: {0},{1}'.format(end_x, tmp_y), end=' ')
        #     tmp_y += step_y
        #     # print('from: {0},{1}'.format(end_x, tmp_y), end=' ')
        #     win32api.SendMessage(hwnd, win32con.WM_MOUSEMOVE, 1,
        #                          win32api.MAKELONG(end_x, tmp_y))
        #     time.sleep(later_interval)

        # # 消除小数点差异
        # win32api.SendMessage(hwnd, win32con.WM_MOUSEMOVE, 1,
        #                      win32api.MAKELONG(end_x, end_y))
        # time.sleep(early_interval)

        # # 再释放鼠标左键
        # win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0,
        #                      win32api.MAKELONG(end_x, end_y))
        # time.sleep(0.1)
        
    def GetScreenShot():
        """
        获取屏幕截图
        :return:
        """
        screen = ImageGrab.grab()
        screen = cv2.cvtColor(numpy.asarray(screen), cv2.COLOR_RGB2BGR)
        logging.info('截屏成功')
        return screen

    def get_screenshot(self, inc_x=0, inc_y=0, w=0, h=0) -> Image:
        """原来的写法太拉了，改成截全图
        """
        screen = ImageGrab.grab()
        # screen.show()
        screen = cv2.cvtColor(numpy.asarray(screen), cv2.COLOR_RGB2BGR)
        return screen


def print_all_windows():
    # win_name = '画图'
    def print_window(hwnd, extra):
        # if win_name in win32gui.GetWindowText(hwnd):
        print(win32gui.GetClassName(hwnd), win32gui.GetWindowText(hwnd))

    win32gui.EnumWindows(print_window, None)


def get_all_related_handle(win_name):
    windows = []

    def print_window(hwnd, extra):
        if win_name in win32gui.GetWindowText(hwnd):
            windows.append((hwnd, win32gui.GetClassName(hwnd),
                            win32gui.GetWindowText(hwnd)))

    win32gui.EnumWindows(print_window, windows)
    return windows


def get_fullname_by_part_name(win_name):
    # win_name = '画图'
    windows = get_all_related_handle(win_name)
    if len(windows) > 0:
        print(windows[0][0], windows[0][1], windows[0][2])
        return windows[0][2]
    else:
        return ''


if __name__ == '__main__':
    win_name = 'None' #'阴阳师-网易游戏'
    # win_name = get_fullname_by_part_name('画图')
    # print_all_windows()
    window = Yys_windows_GUI(win_name)
    window.get_window_handler()

    # 测试后台截图，部分截图和完整截图
    # image = window.get_screenshot(10, 10, 100, 200)
    # image.show()
    image = window.get_screenshot()
    image.show()

    # 测试后台点击
    window.click_loc_inc_by_handler(200, 300)
    window.click_loc_inc_by_handler(500, 500)
    window.click_loc_inc_by_handler(500, 500)

    # 测试鼠标拖拉
    hwnd = window.handler
    # 移动鼠标 -> 点击按下 -> 移动鼠标 -> 点击释放
    window.drag_rel(500, 500, 200, 300)
