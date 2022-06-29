#-*- coding: utf-8 -*-
#!/usr/bin/python
'''
    文档说明：基础性的声明和定义
'''


def transform_func_name(func_name, from_cn_to_en=True):
    '''将功能转化成可识别的功能名称，如 御魂 -> yuhun'''
    func_name_map_cn_to_en = {
        '御魂': 'yuhun',
        '结界突破': 'yys_break',
        '自动助威': 'cheer',
        '困28': 'chapter',
        '御灵': 'yuling',
        '业原火': 'yeyuanhuo',
        '日轮之城': 'rilun',
        '妖气封印': 'yaoqi',
        '点击模式': 'pattern',
        '活动预留': 'activity',
        '升级狗粮': 'upgrade',
        '自动斗技': 'douji',
    }

    func_name_map_en_to_cn = {
        'yuhun': '御魂',
        'yys_break': '结界突破',
        'cheer': '自动助威',
        'chapter': '困28',
        'yuling': '御灵',
        'yeyuanhuo': '业原火',
        'rilun': '日轮之城',
        'yaoqi': '妖气封印',
        'pattern': '点击模式',
        'activity': '活动预留',
        'upgrade': '升级狗粮',
        'douji': '自动斗技',
    }

    if from_cn_to_en:
        funcs = func_name_map_cn_to_en
    else:
        funcs = func_name_map_en_to_cn

    if func_name in funcs:
        return funcs[func_name]
    else:
        return ''


def transform_cb_data(text):
    '''通过选项的内容来获取要设置配置的 key 和 value'''
    cb_text_key_value_map = {
        '单人': ('players', 1),
        '双人': ('players', 2),
        '三人': ('players', 3),
        '队长': ('captain', True),
        '队员': ('captain', False),
        '狗粮类型': ('fodder_type', 'fodder'),
        'N卡': ('fodder_type', 'ncard'),
        '白蛋': ('fodder_type', 'fodder'),
        '挑战类型': ('type', 'phenix'),
        '神龙': ('type', 'dragon'),
        '狐狸': ('type', 'fox'),
        '黑豹': ('type', 'leopard'),
        '凤凰': ('type', 'phenix'),
        '不挑战寮': ('only_person', True),
        '挑战寮': ('only_person', False),
        '升星等级': ('upgrade_stars', 2),
        '2->3': ('upgrade_stars', 2),
        '3->4': ('upgrade_stars', 3),
        '不更换狗粮': ('change_fodder', False),
        '更换狗粮': ('change_fodder', True),
        '官方轮换开启': ('official_change_fodder', True),
        '不标记': ('mark', False),
        '标记': ('mark', True),
        '妖怪类型': ('type', 'rihefang'),
        '椒图': ('type', 'jiaotu'),
        '海坊主': ('type', 'haifangzhu'),
        '鬼使黑': ('type', 'guishihei'),
        '小松丸': ('type', 'xiaosongwan'),
        '日和坊': ('type', 'rihefang'),
    }

    if text in cb_text_key_value_map:
        return cb_text_key_value_map[text]
    else:
        return ('unknown_key', 'unknown_value')

