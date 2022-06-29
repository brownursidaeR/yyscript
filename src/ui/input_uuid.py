import sys
import time
import os
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal, QObject, Qt

if __name__ == "__main__":
    cur_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
    sys.path.append(os.path.join(cur_dir, 'ui'))

from Ui_input_uuid_widget import Ui_uuid_win


class UuidWidget(QDialog):
    signal_input_result = pyqtSignal(str)

    def __init__(self, parent=None, win_name='阴阳师-网易游戏'):
        # Ui_yys_win.__init__(self)
        super(UuidWidget, self).__init__(parent)
        self.ui = Ui_uuid_win()
        self.ui.setupUi(self)
        # self.autogui.sendmsg.connect(self.display_msg)
        # self.stop_run.connect(self.autogui.stop_run)

    def slot_pbtn_ok_clicked(self):
        print('slot_pbtn_ok_clicked')
        self.emit_input_result(self.ui.le_uuid.text())
        self.accept()

    def slot_pbtn_cancel_clicked(self):
        print('slot_pbtn_cancel_clicked')
        self.emit_input_result('')
        self.reject()

    def emit_input_result(self, text):
        print('emit_input_result')
        self.signal_input_result.emit(text)
        time.sleep(0.2)


class SlotUuid(QObject):
    def __init__(self, win_name='get uuid', le_name='uuid'):
        super(SlotUuid, self).__init__(None)  # 初始化信号和槽的初始化
        self.uuid_win = UuidWidget()
        self.uuid_win.setWindowTitle(win_name)
        self.uuid_win.ui.lb_uuid.setText(le_name)
        self.uuid_win.signal_input_result.connect(
            self.slot_signal_input_result)
        self.text = ''

    def slot_signal_input_result(self, text):
        print('slot_signal_input_result: recv=' + text)
        self.text = text

    def get_uuid_from_win(self):
        # Qdialog 可以直接使用 exec_() 来显示模态形式
        self.uuid_win.exec_()
        print('get_uuid_from_win: recv=' + self.text)
        return self.text


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = SlotUuid()
    text = main_win.get_uuid_from_win()
    print(text)
    sys.exit(app.exec_())