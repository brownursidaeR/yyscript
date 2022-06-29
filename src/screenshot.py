#!/usr/bin/python
# -*- coding: utf-8 -*

# %% 先加载对应的库
import os
import sys
from PIL import Image
import cv2
import numpy as np
import logging
from matplotlib import pyplot as plt

# %% 取出图片对应的截图文件，文件的目录结构
cur_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
IMAGES_PATH = os.path.join(cur_dir, 'screenshot')
logger = logging.getLogger('kiddo')
'''
图片类型1：
    图片1.jpg
    图片2.jpg
图片类型2：
    图片1.jpg
    图片2.jpg
'''


def pil2cv(image, transform=cv2.COLOR_BGR2GRAY):
    ''' PIL型 -> OpenCV型
    cv2.COLOR_BGR2GRAY 将BGR格式转换成灰度图片
    cv2.COLOR_BGR2RGB 将BGR格式转换成RGB格式 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:
        pass
    elif new_image.shape[2] == 3:
        new_image = cv2.cvtColor(new_image, transform)
    elif new_image.shape[2] == 4:
        new_image = cv2.cvtColor(new_image, transform)
    return new_image


def cv2pil(image, transform=cv2.COLOR_BGR2GRAY):
    ''' OpenCV型 -> PIL型
    cv2.COLOR_BGR2GRAY 将BGR格式转换成灰度图片
    cv2.COLOR_BGR2RGB 将BGR格式转换成RGB格式 '''
    new_image = image.copy()
    if new_image.ndim == 2:
        pass
    elif new_image.shape[2] == 3:
        new_image = cv2.cvtColor(new_image, transform)
    elif new_image.shape[2] == 4:
        new_image = cv2.cvtColor(new_image, transform)
    new_image = Image.fromarray(new_image)
    return new_image


class Location:
    def __init__(self, x, y, w, h):
        self.left = x
        self.top = y
        self.width = w
        self.height = h


def locate_im_cv2cv(template, target_rgb_gray, confidence=0.8,
                    multi_loc=False):
    h, w = template.shape[0], template.shape[1]
    res = cv2.matchTemplate(target_rgb_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= confidence)

    locations = []
    for pt in zip(*loc[::-1]):  # zip(*loc[::-1]) 等价于 zip(loc[1], loc[0])
        # cv2.rectangle(target_rgb_gray, pt, (pt[0] + w, pt[1] + h), (0, 0, 255),
        #               2)
        if multi_loc is False:
            return Location(pt[0], pt[1], w, h)
        locations.append(Location(pt[0], pt[1], w, h))

    if len(locations) > 0:
        return locations
    else:
        return None


def locate_im_cv2pil(template, target, confidence=0.8, multi_loc=False):
    return locate_im_cv2cv(template, pil2cv(target), confidence, multi_loc)


def locate_image_pil2pil(template: Image, target: Image, confidence=0.8):
    return locate_im_cv2cv(pil2cv(template), pil2cv(target), confidence)


def locate_image_cv2pil(template: np.ndarray,
                        target: Image,
                        confidence=0.8,
                        use_rgb=False):
    if use_rgb:
        return locate_im_cv2cv(template, pil2cv(target, cv2.COLOR_BGR2RGB),
                               confidence)
    else:
        return locate_im_cv2cv(template, pil2cv(target), confidence)


def locate_image_cv2cv(template: np.ndarray,
                       target: np.ndarray,
                       confidence=0.8):
    return locate_im_cv2cv(template, pil2cv(target), confidence)


def show_cv2_image(img: np.ndarray):
    cv2.imshow('Image', img)
    cv2.waitKey(0) & 0xFF
    cv2.destroyAllWindows()


def show_pil_image(img: Image):
    img.show()


class Screenshot:
    def __init__(self, image_path=IMAGES_PATH):
        self.path = image_path
        print('image_path',image_path)
        self.path_exists = os.path.exists(IMAGES_PATH)
        self.cur_section = None

        if (self.path_exists):
            print('path',self.path)
            self.sections = [
                x for x in os.listdir(self.path)
                if os.path.isdir(os.path.join(self.path, x))
            ]

    def is_path_exists(self):
        return self.path_exists

    def open_image_file(self, image_path) -> np.ndarray:
        try:
            return cv2.imread(image_path, 0)  # 直接读取灰度后的图片
        except Exception as error:
            logger.debug('打开图片失败，{0}, msg:{1}'.format(image_path, error))
            return None

    def read_section_jpg(self, section):
        if hasattr(self, section):
            logger.debug(
                'find_all_jpg: already has section:{0}'.format(section))
            return False

        setattr(self, section, {})  # 添加对应的副本分类的字典
        new_attr = getattr(self, section)

        # 递归遍历目录及子目录下的所有文档 (root, ds, fs)
        dirpath = os.path.join(self.path, section)
        jpg_files = {}
        for each_walk in os.walk(dirpath):
            for file in each_walk[2]:
                if file.endswith('.jpg'):
                    jpg_files[file[:-4:]] = self.open_image_file(
                        os.path.join(each_walk[0], file))
        new_attr.update(jpg_files)
        return True

    def read_all_sections(self):
        for section in self.sections:
            # print(section)
            self.read_section_jpg(section)

    def get_section_jpg(self, section, key):
        if hasattr(self, section):
            imags = getattr(self, section)
            if key in imags:
                return imags[key]

        imags = getattr(self, 'general')
        if key in imags:
            return imags[key]
        return None

    def set_current_setion(self, section: str):
        self.cur_section = section


class YysScreenshot(Screenshot):
    def __init__(self, section, image_path=IMAGES_PATH):
        Screenshot.__init__(self, image_path)
        self.read_all_sections()
        self.set_current_setion(section)

    def get_jpg(self, key):
        return self.get_section_jpg(self.cur_section, key)

    def show_jpg(self, key):
        return show_cv2_image(self.get_jpg(key))

    def show_section_key_jpg(self, section, key):
        return show_cv2_image(self.get_section_jpg(section, key))

    def get_jpgs(self, keys):
        images = {}
        for key in keys:
            images[key] = self.get_jpg(key)
        return images


if __name__ == '__main__':
    screenshot = Screenshot()
    if screenshot.is_path_exists():
        screenshot.read_section_jpg('yeyuanhuo')
        logger.debug(str(getattr(screenshot, 'yeyuanhuo')))

        screenshot.read_section_jpg('yuling')
        logger.debug(str(getattr(screenshot, 'yuling')))

        screenshot.read_section_jpg('general')
        logger.debug(str(getattr(screenshot, 'general')))
        show_cv2_image(screenshot.get_section_jpg('general', 'search'))


    #     screenshot.get_section_jpg('yeyuanhuo', 'absent').show()
    screenshot = YysScreenshot('yeyuanhuo')
    jpgs = screenshot.get_jpgs(['absent', 'chi'])
    images = [x[1] for x in jpgs.items()]
    logger.debug(str(images))
    screenshot.show_jpg('chi')
