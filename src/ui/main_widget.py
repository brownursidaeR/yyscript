# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\gitee\gitmanage\B000_study\B100_language\python\new_yysscript\src\ui\main_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_yys_win(object):
    def setupUi(self, yys_win):
        yys_win.setObjectName("yys_win")
        yys_win.setEnabled(True)
        yys_win.resize(461, 589)
        self.centralwidget = QtWidgets.QWidget(yys_win)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 444, 541))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.cb_fuctions = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.cb_fuctions.setObjectName("cb_fuctions")
        self.cb_fuctions.addItem("")
        self.cb_fuctions.addItem("")
        self.cb_fuctions.addItem("")
        self.cb_fuctions.addItem("")
        self.cb_fuctions.addItem("")
        self.horizontalLayout_2.addWidget(self.cb_fuctions)
        self.pbt_autocheck = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pbt_autocheck.setObjectName("pbt_autocheck")
        self.horizontalLayout_2.addWidget(self.pbt_autocheck)
        self.pbt_restart = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pbt_restart.setObjectName("pbt_restart")
        self.horizontalLayout_2.addWidget(self.pbt_restart)
        self.pbt_start = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pbt_start.setObjectName("pbt_start")
        self.horizontalLayout_2.addWidget(self.pbt_start)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.cb_p1 = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.cb_p1.setObjectName("cb_p1")
        self.cb_p1.addItem("")
        self.cb_p1.addItem("")
        self.cb_p1.addItem("")
        self.horizontalLayout_3.addWidget(self.cb_p1)
        self.cb_p2 = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.cb_p2.setObjectName("cb_p2")
        self.cb_p2.addItem("")
        self.cb_p2.addItem("")
        self.horizontalLayout_3.addWidget(self.cb_p2)
        self.cb_p3 = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.cb_p3.setObjectName("cb_p3")
        self.cb_p3.addItem("")
        self.cb_p3.addItem("")
        self.horizontalLayout_3.addWidget(self.cb_p3)
        self.cb_p4 = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.cb_p4.setObjectName("cb_p4")
        self.cb_p4.addItem("")
        self.cb_p4.addItem("")
        self.cb_p4.addItem("")
        self.cb_p4.addItem("")
        self.horizontalLayout_3.addWidget(self.cb_p4)
        self.cb_p5 = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.cb_p5.setObjectName("cb_p5")
        self.cb_p5.addItem("")
        self.cb_p5.addItem("")
        self.horizontalLayout_3.addWidget(self.cb_p5)
        self.cb_p6 = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.cb_p6.setObjectName("cb_p6")
        self.cb_p6.addItem("")
        self.horizontalLayout_3.addWidget(self.cb_p6)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.pte_msg = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget)
        self.pte_msg.setReadOnly(True)
        self.pte_msg.setObjectName("pte_msg")
        self.verticalLayout.addWidget(self.pte_msg)
        self.ptn_clear = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.ptn_clear.setObjectName("ptn_clear")
        self.verticalLayout.addWidget(self.ptn_clear)
        spacerItem1 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.te_attention = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.te_attention.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.te_attention.setObjectName("te_attention")
        self.horizontalLayout.addWidget(self.te_attention)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pbtn_sponsor = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pbtn_sponsor.setObjectName("pbtn_sponsor")
        self.verticalLayout_2.addWidget(self.pbtn_sponsor)
        self.lb_qrcode = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lb_qrcode.setMaximumSize(QtCore.QSize(100, 100))
        self.lb_qrcode.setScaledContents(True)
        self.lb_qrcode.setObjectName("lb_qrcode")
        self.verticalLayout_2.addWidget(self.lb_qrcode)
        self.verticalLayout_2.setStretch(1, 5)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(3, 10)
        self.verticalLayout.setStretch(6, 4)
        yys_win.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(yys_win)
        self.statusbar.setEnabled(False)
        self.statusbar.setObjectName("statusbar")
        yys_win.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(yys_win)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 461, 23))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        yys_win.setMenuBar(self.menubar)
        self.ac_huntu_check = QtWidgets.QAction(yys_win)
        self.ac_huntu_check.setObjectName("ac_huntu_check")
        self.ac_feedback = QtWidgets.QAction(yys_win)
        self.ac_feedback.setObjectName("ac_feedback")
        self.actionv1_01_20200713 = QtWidgets.QAction(yys_win)
        self.actionv1_01_20200713.setObjectName("actionv1_01_20200713")
        self.ac_uuid = QtWidgets.QAction(yys_win)
        self.ac_uuid.setObjectName("ac_uuid")
        self.ac_sponsor = QtWidgets.QAction(yys_win)
        self.ac_sponsor.setObjectName("ac_sponsor")
        self.ac_help = QtWidgets.QAction(yys_win)
        self.ac_help.setObjectName("ac_help")
        self.ac_use = QtWidgets.QAction(yys_win)
        self.ac_use.setObjectName("ac_use")
        self.ac_input_uuid = QtWidgets.QAction(yys_win)
        self.ac_input_uuid.setObjectName("ac_input_uuid")
        self.ac_input_title = QtWidgets.QAction(yys_win)
        self.ac_input_title.setObjectName("ac_input_title")
        self.ac_show_yys_winname = QtWidgets.QAction(yys_win)
        self.ac_show_yys_winname.setObjectName("ac_show_yys_winname")
        self.ac_input_yys_winname = QtWidgets.QAction(yys_win)
        self.ac_input_yys_winname.setObjectName("ac_input_yys_winname")
        self.ac_input_win_hwnd = QtWidgets.QAction(yys_win)
        self.ac_input_win_hwnd.setObjectName("ac_input_win_hwnd")
        self.menuHelp.addAction(self.ac_uuid)
        self.menuHelp.addAction(self.ac_input_uuid)
        self.menuHelp.addAction(self.ac_input_title)
        self.menuHelp.addAction(self.ac_input_yys_winname)
        self.menuHelp.addAction(self.ac_input_win_hwnd)
        self.menu.addAction(self.ac_use)
        self.menu.addAction(self.ac_help)
        self.menu.addAction(self.ac_feedback)
        self.menu.addAction(self.ac_sponsor)
        self.menu.addAction(self.ac_show_yys_winname)
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(yys_win)
        self.pbt_start.clicked.connect(yys_win.btn_start_clicked)
        self.pushButton.clicked.connect(yys_win.btn_stop_clicked)
        self.cb_fuctions.currentIndexChanged['QString'].connect(yys_win.cb_functions_index_changed)
        self.ptn_clear.clicked.connect(self.pte_msg.clear)
        self.pbt_restart.clicked.connect(yys_win.btn_restart_clicked)
        self.ac_uuid.triggered.connect(yys_win.slot_ac_uuid_trigged)
        self.ac_feedback.triggered.connect(yys_win.slot_ac_feedback_trigged)
        self.ac_sponsor.triggered.connect(yys_win.slot_ac_sponsor_trigged)
        self.ac_help.triggered.connect(yys_win.slot_ac_help_trigged)
        self.ac_use.triggered.connect(yys_win.slot_ac_use_trigged)
        self.ac_input_uuid.triggered.connect(yys_win.sloc_ac_input_uuid_trigged)
        self.pbtn_sponsor.clicked.connect(yys_win.slot_pbtn_sponsor_clicked)
        self.ac_input_yys_winname.triggered.connect(yys_win.sloc_ac_input_yys_winname_trigged)
        self.ac_input_title.triggered.connect(yys_win.sloc_ac_input_title_trigged)
        self.ac_show_yys_winname.triggered.connect(yys_win.slot_ac_show_winname_trigged)
        self.ac_input_win_hwnd.triggered.connect(yys_win.slot_ac_input_win_hwnd_trigged)
        QtCore.QMetaObject.connectSlotsByName(yys_win)

    def retranslateUi(self, yys_win):
        _translate = QtCore.QCoreApplication.translate
        yys_win.setWindowTitle(_translate("yys_win", "x笑cry-辅助工具"))
        self.label.setText(_translate("yys_win", "功能："))
        self.cb_fuctions.setItemText(0, _translate("yys_win", "御魂"))
        self.cb_fuctions.setItemText(1, _translate("yys_win", "困28"))
        self.cb_fuctions.setItemText(2, _translate("yys_win", "御灵"))
        self.cb_fuctions.setItemText(3, _translate("yys_win", "业原火"))
        self.cb_fuctions.setItemText(4, _translate("yys_win", "结界突破"))
        self.pbt_autocheck.setText(_translate("yys_win", "设置参数"))
        self.pbt_restart.setText(_translate("yys_win", "重新开始"))
        self.pbt_start.setText(_translate("yys_win", "开始"))
        self.pushButton.setText(_translate("yys_win", "结束"))
        self.cb_p1.setItemText(0, _translate("yys_win", "双人"))
        self.cb_p1.setItemText(1, _translate("yys_win", "单人"))
        self.cb_p1.setItemText(2, _translate("yys_win", "三人"))
        self.cb_p2.setItemText(0, _translate("yys_win", "队长"))
        self.cb_p2.setItemText(1, _translate("yys_win", "队员"))
        self.cb_p3.setItemText(0, _translate("yys_win", "可能翻车"))
        self.cb_p3.setItemText(1, _translate("yys_win", "不会翻车"))
        self.cb_p4.setItemText(0, _translate("yys_win", "挂机次数"))
        self.cb_p4.setItemText(1, _translate("yys_win", "100"))
        self.cb_p4.setItemText(2, _translate("yys_win", "200"))
        self.cb_p4.setItemText(3, _translate("yys_win", "400"))
        self.cb_p5.setItemText(0, _translate("yys_win", "魂十一"))
        self.cb_p5.setItemText(1, _translate("yys_win", "魂十"))
        self.cb_p6.setItemText(0, _translate("yys_win", "参数6"))
        self.pte_msg.setPlainText(_translate("yys_win", "执行日志："))
        self.ptn_clear.setText(_translate("yys_win", "清空日志"))
        self.te_attention.setHtml(_translate("yys_win", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">注意事项说明：</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pbtn_sponsor.setText(_translate("yys_win", "如觉不错，可随缘打赏"))
        self.lb_qrcode.setText(_translate("yys_win", "接图片"))
        self.menuHelp.setTitle(_translate("yys_win", "工具"))
        self.menu.setTitle(_translate("yys_win", "帮助与反馈"))
        self.ac_huntu_check.setText(_translate("yys_win", "魂土验证"))
        self.ac_feedback.setText(_translate("yys_win", "意见反馈-加群"))
        self.actionv1_01_20200713.setText(_translate("yys_win", "v1.01.20200713"))
        self.ac_uuid.setText(_translate("yys_win", "生成机器码"))
        self.ac_sponsor.setText(_translate("yys_win", "打赏支持"))
        self.ac_help.setText(_translate("yys_win", "问题帮助"))
        self.ac_use.setText(_translate("yys_win", "使用方法"))
        self.ac_input_uuid.setText(_translate("yys_win", "输入认证码"))
        self.ac_input_title.setText(_translate("yys_win", "修改程序标题"))
        self.ac_show_yys_winname.setText(_translate("yys_win", "阴阳师窗体名称获取"))
        self.ac_input_yys_winname.setText(_translate("yys_win", "修改阴阳师窗体名称"))
        self.ac_input_win_hwnd.setText(_translate("yys_win", "输入阴阳师句柄"))