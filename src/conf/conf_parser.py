# /usr/bin/python
# -*- coding: utf-8 -*-
'''
    用来解析配置文件
'''

# !/usr/bin/python
# -*- coding: utf-8 -*

# %% 先加载对应的库
import configparser
import os
import sys
import logging
from enum import Enum

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    cur_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
    CONF_DIR = cur_dir
else:
    cur_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
    CONF_DIR = os.path.join(cur_dir, 'conf')
CONF_PATH = os.path.join(CONF_DIR, 'config.ini')


# %% key 和类型构建映射
class KeyType(Enum):
    KeyInt = 1,
    KeyFloat = 2,
    KeyStr = 3,
    KeyBool = 4,
    KeyWords = 5,
    KeyMax = 6,


# option 与对应的解析类型的映射
OP_TYPE_MAP = {
    'gitpath': KeyType.KeyStr,
    'description': KeyType.KeyStr,
    'username': KeyType.KeyStr,
    'email': KeyType.KeyStr,
    'is_opensource': KeyType.KeyBool,
    'download': KeyType.KeyBool,
    'dir': KeyType.KeyWords,
}

OPTION_TYPE_VALUE_LIST = [
    ('xxxint', KeyType.KeyInt, 5),
    ('xxxfloat', KeyType.KeyFloat, 5.0),
    ('xxxstr', KeyType.KeyStr, 'xxx'),
    ('xxxbool', KeyType.KeyBool, True),
    ('xxxwords', KeyType.KeyWords, ['xxxint', 'xxxint2']),
    ('username', KeyType.KeyStr, 'username'),
    ('download', KeyType.KeyStr, True),
]


# %% 定义配置解析类
# ini 文件 -> 按 KeyType 映射解析函数 -> 解析配置 -> 按需要的类型存储
class Config:
    # 不作为单例模式
    # def __new__(cls, *args, **kwargs):
    #     # 将一个类的实例绑定到类变量_instance上
    #     # 构建父类，该父类的内存空间内最多允许相同名字子类的实例对象存在1个
    #     if not hasattr(cls, '_instrance'):
    #         orig = super(Config, cls)
    #         cls._instrance = orig.__new__(cls)
    #     return cls._instrance

    def __init__(self, confpath=CONF_PATH, op_type_map=None):
        self.confpath = confpath
        self.config_parser = configparser.RawConfigParser()
        self.op_type_map = OP_TYPE_MAP if op_type_map is None else op_type_map
        # 设置不同类型的配置对应的解析函数
        self.type_parser_map = {
            KeyType.KeyInt: self.config_parser.getint,
            KeyType.KeyFloat: self.config_parser.getfloat,
            KeyType.KeyStr: self.read_and_parse_str,
            KeyType.KeyBool: self.config_parser.getboolean,
            KeyType.KeyWords: self.read_and_parse_keywords,
        }
        self.parser_created = self.read_file()

    def read_file(self):
        parser_created = False
        if os.path.exists(self.confpath) is False:
            logging.debug('读取配置文件失败：{0} 路径不存在'.format(self.confpath))
            return False

        try:
            self.config_parser.read(self.confpath, encoding='utf-8')
            parser_created = True
        except Exception as error:
            logging.debug('读取配置文件失败：{0},{1}'.format(self.confpath, str(error)))
            raise error
        finally:
            return parser_created

    def is_read_file_success(self):
        return self.parser_created

    def read_option_by_type(self, section, option, op_default=None):
        if option not in self.op_type_map:
            logging.debug('没有找到 {0} 对应的操作类型，使用默认值 {1}'.format(
                option, op_default))
            return op_default

        # 指定类型，使用对应的默认值
        if op_default is None:
            if self.op_type_map[option] == KeyType.KeyInt:
                op_default = 0
            elif self.op_type_map[option] == KeyType.KeyFloat:
                op_default = 0.0
            elif self.op_type_map[option] == KeyType.KeyStr:
                op_default = ''
            elif self.op_type_map[option] == KeyType.KeyBool:
                op_default = False
            elif self.op_type_map[option] == KeyType.KeyWords:
                op_default = []

        # 获取到对应类型的解析函数
        parser = self.type_parser_map[self.op_type_map[option]]
        if self.parser_created is False:
            return op_default
        try:
            return parser(section, option)
        except Exception as error:
            logging.debug('获取{0},{1}失败, {2}'.format(section, option,
                                                    str(error)))
            return op_default

    def read_and_parse_keywords(self, section, option):
        try:
            return self.config_parser.get(section, option).split(',')
        except Exception as error:
            logging.debug('获取{0},{1}失败, {2}'.format(section, option,
                                                    str(error)))
            raise error

    def read_and_parse_str(self, section, option):
        try:
            return self.config_parser.get(section, option).strip('"')
        except Exception as error:
            logging.debug('获取{0},{1}失败, {2}'.format(section, option,
                                                    str(error)))
            raise error

    def add_section_option(self, section, option, value):
        # TODO: 可能需要将值也加到 self.parser 中
        is_new_section = False
        if self.config_parser.has_section(section) is False:
            setattr(self, section, {})
            is_new_section = True
        cur_section = getattr(self, section)
        cur_section[option] = value
        if is_new_section:
            cur_section['name'] = section
            self.config_parser.add_section(section)

    def get_section_option(self, section, option, default=None):
        if hasattr(self, section):
            cur_section = getattr(self, section)
            if option in cur_section:
                return cur_section[option]
            else:
                logging.debug('找不到 option{0}, 返回默认值'.format(option))
        else:
            logging.debug('找不到section{0}, 返回默认值'.format(section))
            return default

    def modify_section_option(self, section, option, value, write_file=True):
        '''write_file 参数表示是否修改后直接同步到文件'''
        sections = self.get_sections()
        if section not in sections:
            logging.debug('找不到section{0}, 返回默认值'.format(section))
            return

        # 不能简单设置，需要根据类型进行设置
        option_found = False
        for cur_option in self.op_type_map:
            if cur_option == option:
                option_found = True
                break
        if option_found and self.op_type_map[cur_option] == KeyType.KeyWords:
            value = ','.join(value)
            self.config_parser.set(section, option, value)
        else:
            self.config_parser.set(section, option, value)
        # 写之后，注释会丢失， section 的顺序也可能发生变化
        if write_file:
            with open(self.confpath, 'w', encoding='utf-8') as write_fd:
                self.config_parser.write(write_fd)

    def get_sections(self):
        return self.config_parser.sections()

    def read_all_sections(self, op_type_v=None):
        '''OPTION_TYPE_VALUE_LIST 是 [option type op_default] 类型的列表'''
        sections = self.config_parser.sections()
        for section in sections:
            self.read_one_section_config(section, op_type_v)
            # logging.debug(str(getattr(self, section)))

    def read_one_section_config(self, section: str, op_type_v=None):
        '''OPTION_TYPE_VALUE_LIST 是 [option type op_default] 类型的列表'''
        logging.debug('正在解析： section {0}'.format(section))
        if op_type_v is None:
            op_type_v = OPTION_TYPE_VALUE_LIST

        if hasattr(self, section):
            logging.debug('{0} 类型已经读取过了，不需要重新读入'.format(section))
            return
        else:
            if hasattr(self, section) is False:
                setattr(self, section, {})  # 新增一个字典，直接加可能会有问题

            cur_section = getattr(self, section)
            cur_section['name'] = section

            # 先把默认配置全部添加进来，默认配置的话，可以不用添加到 confparser 中
            # option, op_type, op_default
            for each in op_type_v:
                cur_section[each[0]] = each[2]

            # 把配置里面的 section 对应的所有数据全部读出来
            conf_options = self.config_parser.options(section)
            for option in conf_options:
                cur_section[option] = self.read_option_by_type(section, option)


if __name__ == '__main__':
    yys_config = Config(confpath=CONF_PATH)
    logging.debug(str(yys_config.is_read_file_success()))

    # 测试展示所有key
    yys_config.read_all_sections()
    for section in yys_config.get_sections():
        logging.debug(str(section))
        logging.debug(str(getattr(yys_config, section)))

    # 测试更新部分key
    logging.debug(str(getattr(yys_config, 'general')))
    yys_config.get_section_option('general', 'dir')
    # yys_config.modify_section_option('general', 'dir', 'general', False)
    # yys_config.modify_section_option('general', 'xxxwords', ['A', 'B', 'C'])
