#!/usr/bin/python
# -*- coding: utf-8 -*

# %% 先加载对应的库
import os
import sys
import logging
from conf_parser import Config, KeyType

# %% 取出配置对应的文件

if __name__ == '__main__':
    cur_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
    CONF_DIR = cur_dir
else:
    cur_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
    CONF_DIR = os.path.join(cur_dir, 'conf')
CONF_PATH = os.path.join(CONF_DIR, 'config.ini')
DEFAULT_SECTION = 'general'

logger = logging.getLogger('kiddo')

# 通用配置，具体配置对应的默认 type-value
OPTION_GENERAL_TYPE_VALUE_LIST = [
    ('title', KeyType.KeyStr, 'x笑cry-辅助工具'),  # 窗口标题
    ('version', KeyType.KeyStr, 'v1.0.0'),  # 版本信息
    ('gitpath', KeyType.KeyStr, '无'),  # 仓库的 git 路径
    ('win_name', KeyType.KeyStr, '阴阳师-网易游戏'),  # 游戏窗口名称
    ('win_hwnd', KeyType.KeyInt, -1),  # 游戏窗口的句柄
    ('width', KeyType.KeyInt, 8),  # 界面宽度
    ('height', KeyType.KeyInt, 8),  # 界面长度
    ('funcs', KeyType.KeyStr, '功能列表'),  # 界面显示的功能列表
    ('extern_config', KeyType.KeyWords, []),  # 额外需要加载的配置文件
    ('licence', KeyType.KeyStr, 'ABC'),  # 证书
    ('max_excute_time', KeyType.KeyInt, 120),  # 程序的最长执行时间
    ('max_serial_key_times', KeyType.KeyInt, 20),
    ('attention', KeyType.KeyStr, '无'),  # 注意事项
    ('drag_dis', KeyType.KeyInt, 8),  # 狗粮拖动距离
]

# 各个功能，具体配置对应的默认 type-value
OPTION_FUNC_TYPE_VALUE_LIST = [
    # ('xxxint', KeyType.KeyInt, 5),
    # ('xxxfloat', KeyType.KeyFloat, 5.0),
    # ('xxxstr', KeyType.KeyStr, 'xxx'),
    # ('xxxbool', KeyType.KeyBool, True),
    # ('xxxwords', KeyType.KeyWords, ['xxxint', 'xxxint2']),

    # 界内辅助显示配置，每个功能框的选项列表, menu1 固定为挑战次数
    # ('menu1', KeyType.KeyWords, ['参数1']),
    ('menu2', KeyType.KeyWords, ['参数2']),
    ('menu3', KeyType.KeyWords, ['参数3']),
    ('menu4', KeyType.KeyWords, ['参数4']),
    ('menu5', KeyType.KeyWords, ['参数5']),
    ('menu6', KeyType.KeyWords, ['参数6']),
    ('attention', KeyType.KeyStr, '无'),  # 注意事项

    # 一些功能使用的通用配置
    ('loop_times', KeyType.KeyInt, 200),  # 循环次数

    # 组队的选项
    ('players', KeyType.KeyInt, 1),  # 玩家数量
    ('captain', KeyType.KeyBool, True),  # 是否为队长

    # 更换狗粮的选项
    ('change_fodder', KeyType.KeyBool, False),  # 更换狗粮
    ('official_change_fodder', KeyType.KeyBool, False), # 更换狗粮
    ('fodder_type', KeyType.KeyStr, 'fodder'),  # 狗粮类型

    # 御灵相关
    ('type', KeyType.KeyStr, 'dragon'),  # 挑战类型
    ('layer', KeyType.KeyInt, 3),  # 挑战层数

    # 升级狗粮
    ('upgrade_stars', KeyType.KeyInt, 2),

    # 仅个人突破
    ('only_person', KeyType.KeyBool, False),
    ('mark', KeyType.KeyBool, False),  # 是否标记式神

    # 点击模式
    ('prepare_keys', KeyType.KeyWords, []),
    ('loop_keys', KeyType.KeyWords, []),
    ('sleep_seconds', KeyType.KeyInt, 2),
    ('end_key', KeyType.KeyStr, ''),
    ('win_name', KeyType.KeyStr, '阴阳师-网易游戏'),  # 游戏窗口名称

    # 自动斗技
    ('wait_complete_times', KeyType.KeyInt, 2),
]

# option 与对应的解析类型的映射
OP_GENERAL_TYPE_MAP = {}
OP_FUNC_TYPE_MAP = {}
for x in OPTION_GENERAL_TYPE_VALUE_LIST:
    OP_GENERAL_TYPE_MAP[x[0]] = x[1]
for x in OPTION_FUNC_TYPE_VALUE_LIST:
    OP_FUNC_TYPE_MAP[x[0]] = x[1]


class YysSectionConfig(Config):
    ''' 单个功能的配置: .ini 文件中 section 名为 section 值的所有配置组成的集合
        读取到的数据存放为 self.section
    '''

    def __init__(self,
                 section=DEFAULT_SECTION,
                 confpath=CONF_PATH,
                 op_type_map=None,
                 op_type_v=None):
        self.section_name = section
        # self.op_type_map = op_type_map  # 这一步在 init 中已经赋值过了
        self.op_type_v = op_type_v
        Config.__init__(self, confpath, op_type_map)
        if self.is_read_file_success():
            self.read_one_section_config(self.section_name, op_type_v)


class YysConfig():
    '''
        整合所有配置的类
        配置结构，其中 config.ini 是通用配置文件， section.ini 是具体的配置文件
        config.ini
            [general]
            extern_config=section
        section.ini
            [general]
            key=value

        配置解析属性
            self.config['general'] 类型为 YysSectionConfig 的通用配置解析结构
            self.config[section] 类型为 YysSectionConfig 的指定功能的配置结构

        具体配置值属性
            另将对应的 general 字典设置为本类的成员属性，方便使用
            self.general = self.config['general'].general
            self.section = self.config[section].general
    '''

    def __init__(self, cur_section_name=DEFAULT_SECTION, confpath=CONF_PATH):
        self.config = {}  # 存放所有配置文件的 YysSectionConfig 对象
        self.cur_config = {}  # 当前 section 的配置
        self.cur_section_name = cur_section_name  # 设置当前的 section_name

        # 先加载通用配置
        self.parser_created = True
        self.config[DEFAULT_SECTION] = YysSectionConfig(
            DEFAULT_SECTION, CONF_PATH, OP_GENERAL_TYPE_MAP,
            OPTION_GENERAL_TYPE_VALUE_LIST)
        self.general = self.config[DEFAULT_SECTION].general
        self.cur_config = self.general  # 并将通用配置设置为默认配置

        if self.config[DEFAULT_SECTION].is_read_file_success() is False:
            logging.error('general 配置解析错误')
            self.parser_created = False
            return

        # 取出额外的功能配置文件，并加载其中 general 标签下的所有值
        for section in self.general['extern_config']:
            confpath = os.path.join(CONF_DIR, section + '.ini')
            self.config[section] = YysSectionConfig(
                DEFAULT_SECTION, confpath, OP_FUNC_TYPE_MAP,
                OPTION_FUNC_TYPE_VALUE_LIST)

            if self.config[section].is_read_file_success() is False:
                logging.error('{0}配置解析错误'.format(section))
                self.parser_created = False
                return
            elif hasattr(self, section):
                logging.error('配置解析错误，重复加载了配置')
                self.parser_created = False
                return
            else:
                setattr(self, section, {})
                exec('self.{0} = self.config[section].general'.format(section))

        # 重新设置当前配置
        if self.cur_section_name != DEFAULT_SECTION:
            self.set_current_setion(self.cur_section_name)

    def is_read_file_success(self):
        return self.parser_created

    def set_current_setion(self, section):
        self.cur_config = getattr(self, section)


if __name__ == '__main__':
    # 通用配置解析
    # yys_section_config = YysSectionConfig(DEFAULT_SECTION, CONF_PATH,
    #                                       OP_GENERAL_TYPE_MAP,
    #                                       OPTION_GENERAL_TYPE_VALUE_LIST)
    # logger.debug(str(yys_section_config.is_read_file_success()))
    # logger.debug(str(getattr(yys_section_config, DEFAULT_SECTION)))
    # logger.debug('\n\n')

    config = YysConfig(DEFAULT_SECTION, CONF_PATH)
    # logger.debug(str(config.config['general'].general))
    # logger.debug('\n\n')
    # logger.debug(str(config.config['yuhun'].general))
    logger.debug(str(config.general))
    logger.debug('\n\n')
    logger.debug(str(config.yuhun))

    # yys_config.read_all_sections(OPTION_SECTION_TYPE_VALUE_LIST)
    # logger.debug(str(getattr(yys_config, 'general')))
