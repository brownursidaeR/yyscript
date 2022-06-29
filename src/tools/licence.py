# -*- coding: utf-8 -*-
# %% 加载库

import time
import hashlib
import base64
import logging
import subprocess
import requests
from bs4 import BeautifulSoup
'''
#### 认证流程

根据 uuid 做认证

加密算法说明：

1. 先获取到机器主板的 uuid 信息
2. 获取到指定的过期时间
3. 将 uuid + 关键字做 md5 计算，得到 md5 校验串
4. 将 md5 串和时间做为原始的串，做 base64 加密，得到加密串

解密校验过程：

1. 获取加密串
2. base64 解密得到 md5 串 + 时间戳
3. 获取 uuid + 关键字，并做 md5 计算得到对比串，对比串和 md5 串做比较。如果串不匹配，再用通用的 uuid 串做比较，也不匹配，鉴权失败
  4. 用当前时间和时间戳比对
     1. 当前时间大于时间戳，表示过期，鉴权失败
     2. 当前时间小于时间戳，表示还有效，鉴权成功

本来是打算考虑跨平台，用 **pip install --upgrade iupdatable** 这个库，但是这个库兼容性有点问题，开始可以获取到 uuid ，后面就会报兼容性问题。而且跟 pyinstaller 不是很兼容。所以放弃了。
'''

GENEAL_UUID = '000000000000'
GENERAL_KEY = 'kiddo'
logger = logging.getLogger('kiddo')


def execute_cmd(cmd):
    '''涉及管道，用pyinstall不能设置console=False，解决方法来自（无效）
        参考链接：https://www.2nzz.com/thread-58453-1-1.html
    '''
    proc = subprocess.Popen(cmd,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            stdin=subprocess.PIPE)
    proc.stdin.close()
    proc.wait()
    result = proc.stdout.read().decode('gbk')  # 注意你电脑cmd的输出编码（中文是gbk）
    proc.stdout.close()
    return result


def get_machine_uuid():
    '''获取到 UUID 机器码'''
    result = execute_cmd('wmic csproduct get uuid')
    result = result.replace('UUID', '')
    result = result.replace(' ', '')
    result = result.replace('\r', '')
    result = result.replace('\n', '')
    # 这个库兼容性有问题
    # CSProduct.get()["UUID"][-12::]
    return result[-12::]


# %% 封装具体时间转时间戳
def transform_date_to_timestamp(year, month, day):
    '''转化成年-月-日 '''
    time_str = '{0}-{1}-{2}'.format(year, month, day)
    data_sj = time.strptime(time_str, "%Y-%m-%d")
    return int(time.mktime(data_sj))


# %% 封装获取md5算法的函数
def get_md5(orig_str):
    m = hashlib.md5()
    m.update(orig_str.encode('utf-8'))
    return m.hexdigest()


# %% 通过 url 获取网络上的当前时间
# 还有 javascript 运算,比较麻烦
def get_cur_timestamp():
    url = 'http://tool.chinaz.com/Tools/unixtime.aspx'
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text)
    '''
    <div class="mb20 PresentTxt">
        <p class="auto w570">
            <span class="fz16 col-blue02">现在的Unix时间戳(Unix timestamp)是：</span>
            <span class="utspan col-hint" id="currentunixtime">1629007640</span>
            <a href="javascript:" id="start" one-link-mark="yes">开始</a>
            <a href="javascript:" id="stop" one-link-mark="yes">停止</a>
            <a href="javascript:" id="refresh" one-link-mark="yes">刷新</a>
        </p>
    </div>
    '''
    div_list = soup.find_all("div", class_="mb20 PresentTxt")
    print(div_list)
    span_class = div_list[0].p.find("span", class_="utspan col-hint")


# %% 封装生成加密串的函数和解密串的函数
def get_licence(uuid, timestamp):
    # 获取md5
    md5 = get_md5(uuid + GENERAL_KEY)
    orig_str = '{0}_{1}'.format(md5, timestamp)

    # 获取base64编码
    encode_str = base64.b64encode(orig_str.encode('utf-8')).decode()
    logger.debug('加密用的关键信息：{0}，{1}，{2}，{3}'.format(uuid, timestamp, orig_str,
                                                   encode_str))
    return encode_str


def check_license(encode_str):
    # try:
    #     decode_str = base64.b64decode(encode_str.encode('utf-8')).decode()
    #     elements = decode_str.split('_')
    #     if len(elements) != 2:
    #         logger.debug('鉴权失败：解密串格式不对, {0}'.format(encode_str))
    #         return False
    # except Exception:
    #     logger.debug('鉴权失败：解密串格式不对, {0}'.format(encode_str))
    #     return False

    # md5, timestamp = elements[0], int(elements[1])
    # logger.debug('从licence中获取到的信息：str={0}, md5={1}, time={2}'.format(
    #     encode_str, md5, timestamp))

    # # 获取uuid，并根据关键字计算出md5
    # local_md5 = get_md5(get_machine_uuid() + GENERAL_KEY)
    # if md5 != local_md5:
    #     local_md5 = get_md5(GENEAL_UUID + GENERAL_KEY)
    #     if md5 != local_md5:
    #         logger.debug('鉴权失败：即不匹配uuid，也不匹配通用uuid,md5，{0} != {1}'.format(
    #             md5, local_md5))
    #         return False

    # # 检查时间戳
    # local_timestamp = int(time.time())
    # if local_timestamp > timestamp:
    #     logger.debug('鉴权失败：timestamp，{0} < {1}'.format(timestamp,
    #                                                    local_timestamp))
    #     return False
    # logger.debug(encode_str + '鉴权成功')
    return True


def get_remain_time(encode_str) -> str:
    '''不做鉴权，只校验时间，负数表示加密串异常，正数表示剩余时间'''
    decode_str = base64.b64decode(encode_str.encode('utf-8')).decode()
    elements = decode_str.split('_')
    if len(elements) != 2:
        logger.debug('鉴权失败：解密串格式不对, {0}'.format(encode_str))
        return '加密串异常'

    md5, timestamp = elements[0], int(elements[1])
    logger.debug('从licence中获取到的信息：str={0}, md5={1}, time={2}'.format(
        encode_str, md5, timestamp))

    # 检查时间戳
    local_timestamp = int(time.time())
    if local_timestamp > timestamp:
        logger.debug('鉴权失败：timestamp，{0} < {1}'.format(timestamp,
                                                       local_timestamp))
        return '加密串已经过期'
    else:
        remain_time = timestamp - local_timestamp
        expire_str = time.strftime('%Y-%m-%d %H:%M:%S',
                                   time.localtime(int(timestamp)))
        if remain_time > 365 * 24 * 60 * 60:
            return '离认证过期还有超过一年,过期时间:{0}'.format(expire_str)
        elif remain_time > 24 * 60 * 60:
            days = remain_time / (24 * 60 * 60)
            return '离认证过期还有{0}天,过期时间:{1}'.format(int(days), expire_str)
        else:
            return '离认证过期还有{0}秒,过期时间:{1}'.format(int(remain_time), expire_str)


if __name__ == '__main__':
    # 设置日志格式
    logger.setLevel(logging.DEBUG)
    BASIC_FORMAT = '%(asctime)s - %(levelname)s: %(message)s'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
    chlr = logging.StreamHandler()  # 输出到控制台的handler
    chlr.setFormatter(formatter)
    logger.addHandler(chlr)

    # 获取uuid
    logger.debug(get_machine_uuid())

    # 获取日期
    cur_timestamp = int(time.time())

    # 获取机器码
    uuid = get_machine_uuid()

    # 有限时间 3 天
    valid_day = 3
    end_timestamp = cur_timestamp + valid_day * 24 * 60 * 60
    licence = get_licence(uuid, end_timestamp)
    logger.debug('{0}天的licence: {1}，{2}'.format(valid_day, licence,
                                                check_license(licence)))

    # 有限时间 7 天
    valid_day = 7
    end_timestamp = cur_timestamp + valid_day * 24 * 60 * 60
    licence = get_licence(uuid, end_timestamp)
    logger.debug('{0}天的licence: {1}，{2}'.format(valid_day, licence,
                                                check_license(licence)))

    # 有限时间 31 天
    valid_day = 31
    end_timestamp = cur_timestamp + valid_day * 24 * 60 * 60
    licence = get_licence(uuid, end_timestamp)
    logger.debug('{0}天的licence: {1}，{2}'.format(valid_day, licence,
                                                check_license(licence)))

    # 有限时间 90 天
    valid_day = 90
    end_timestamp = cur_timestamp + valid_day * 24 * 60 * 60
    licence = get_licence(uuid, end_timestamp)
    logger.debug('{0}天的licence: {1}，{2}'.format(valid_day, licence,
                                                check_license(licence)))

    # 有限时间 365 天
    valid_day = 365
    end_timestamp = cur_timestamp + valid_day * 24 * 60 * 60
    licence = get_licence(uuid, end_timestamp)
    logger.debug('{0}天的licence: {1}，{2}'.format(valid_day, licence,
                                                check_license(licence)))

    # end_timestamp = transform_date_to_timestamp(2021, 1, 30)
    # logger.debug('{0},{1}'.format(cur_timestamp, end_timestamp))
