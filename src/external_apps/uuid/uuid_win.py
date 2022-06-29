# /usr/bin/dev python
# -*- coding: utf-8 -*-

import os
import sys
import time
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from uuid_dialog import Ui_main_win

if __name__ == "__main__":
    cur_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
    par_dir = os.path.split(cur_dir)[0]
    par_par_dir = os.path.split(par_dir)[0]
    sys.path.append(cur_dir)
    sys.path.append(os.path.join(par_par_dir, 'tools'))
else:
    cur_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
    par_dir = os.path.split(cur_dir)[0]
    par_par_dir = os.path.split(par_dir)[0]
    sys.path.append(os.path.join(par_par_dir, 'tools'))

from licence import get_machine_uuid, get_licence


GENEAL_UUID = '000000000000'

class MainWin(QDialog):
    stop_run = pyqtSignal()

    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        self.ui = Ui_main_win()
        self.ui.setupUi(self)
        # self.ui.setLayout(self.ui.main_lout)
        self.init_win()  # 初始化窗体相关的操作

    def init_win(self):
        # 绑定信号和槽
        # self.ui.pbt_autocheck.clicked.connect(self.btn_autocheck_clicked)
        pass

    def show_attention(self, content):
        self.ui.te_explain.setText(content)

    def slot_ptbn_uuid_clicked(self):
        uuid = get_machine_uuid()
        self.ui.le_uuid.setText(uuid)

    def slot_pbtn_generate_clicked(self):
        # 查看接口
        # print(str(dir(self.ui.rbtn_day_3)))

        uuid = self.ui.le_uuid.text()
        print(uuid)
        if len(uuid) == 0:
            self.display_msg('uuid 不能为空!')
            return

        valid_time = 3
        if self.ui.rbtn_day_3.isChecked():
            valid_time = 3
        elif self.ui.rbtn_day_7.isChecked():
            valid_time = 7
        elif self.ui.rbtn_day_31.isChecked():
            valid_time = 31
        elif self.ui.rbtn_day_100.isChecked():
            valid_time = 100
        elif self.ui.rbtn_day_365.isChecked():
            valid_time = 365

        msg = ''
        if get_machine_uuid() != GENEAL_UUID and valid_time > 99:
            valid_time = 31
            msg += '限制生成超过31天的认证码,自动修改为{0}天\n'.format(valid_time)

        end_timestamp = int(time.time()) + valid_time * 24 * 60 * 60
        msg += 'uuid:{0}, 有效日期:{1} 天\n当前时间:{2},{3}\n'.format(
            uuid, valid_time, end_timestamp,
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_timestamp)))
        licence = get_licence(uuid, end_timestamp)
        msg += 'licence: {0}'.format(licence)
        self.ui.le_licence.setText(licence)
        self.display_msg(msg)

    def display_msg(self, msg):
        # print(str(dir(self.ui.te_msg)))
        self.ui.te_msg.moveCursor(QTextCursor.End)
        self.ui.te_msg.setPlainText(msg + '\n')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWin()
    main_win.show()
    sys.exit(app.exec_())
