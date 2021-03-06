# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uuid_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_main_win(object):
    def setupUi(self, main_win):
        main_win.setObjectName("main_win")
        main_win.resize(412, 213)
        self.verticalLayoutWidget = QtWidgets.QWidget(main_win)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 391, 171))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.main_lout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.main_lout.setContentsMargins(0, 5, 5, 5)
        self.main_lout.setSpacing(5)
        self.main_lout.setObjectName("main_lout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lb_uuid = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lb_uuid.setObjectName("lb_uuid")
        self.horizontalLayout.addWidget(self.lb_uuid)
        self.le_uuid = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.le_uuid.setObjectName("le_uuid")
        self.horizontalLayout.addWidget(self.le_uuid)
        self.pbtn_uuid = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pbtn_uuid.setObjectName("pbtn_uuid")
        self.horizontalLayout.addWidget(self.pbtn_uuid)
        self.main_lout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lb_valid_time = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lb_valid_time.setObjectName("lb_valid_time")
        self.horizontalLayout_2.addWidget(self.lb_valid_time)
        self.rbtn_day_3 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.rbtn_day_3.setChecked(True)
        self.rbtn_day_3.setObjectName("rbtn_day_3")
        self.horizontalLayout_2.addWidget(self.rbtn_day_3)
        self.rbtn_day_7 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.rbtn_day_7.setChecked(False)
        self.rbtn_day_7.setObjectName("rbtn_day_7")
        self.horizontalLayout_2.addWidget(self.rbtn_day_7)
        self.rbtn_day_31 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.rbtn_day_31.setChecked(False)
        self.rbtn_day_31.setObjectName("rbtn_day_31")
        self.horizontalLayout_2.addWidget(self.rbtn_day_31)
        self.rbtn_day_100 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.rbtn_day_100.setObjectName("rbtn_day_100")
        self.horizontalLayout_2.addWidget(self.rbtn_day_100)
        self.rbtn_day_365 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.rbtn_day_365.setObjectName("rbtn_day_365")
        self.horizontalLayout_2.addWidget(self.rbtn_day_365)
        self.main_lout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.le_licence = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.le_licence.setObjectName("le_licence")
        self.horizontalLayout_3.addWidget(self.le_licence)
        self.pbtn_generate = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pbtn_generate.setObjectName("pbtn_generate")
        self.horizontalLayout_3.addWidget(self.pbtn_generate)
        self.main_lout.addLayout(self.horizontalLayout_3)
        self.te_msg = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.te_msg.setObjectName("te_msg")
        self.main_lout.addWidget(self.te_msg)
        self.main_lout.setStretch(0, 2)
        self.main_lout.setStretch(1, 1)
        self.main_lout.setStretch(2, 2)

        self.retranslateUi(main_win)
        self.pbtn_uuid.clicked.connect(main_win.slot_ptbn_uuid_clicked)
        self.pbtn_generate.clicked.connect(main_win.slot_pbtn_generate_clicked)
        QtCore.QMetaObject.connectSlotsByName(main_win)

    def retranslateUi(self, main_win):
        _translate = QtCore.QCoreApplication.translate
        main_win.setWindowTitle(_translate("main_win", "??????????????????"))
        self.lb_uuid.setText(_translate("main_win", "????????????"))
        self.le_uuid.setText(_translate("main_win", "??????????????????"))
        self.pbtn_uuid.setText(_translate("main_win", "?????????????????????"))
        self.lb_valid_time.setText(_translate("main_win", "???????????????"))
        self.rbtn_day_3.setText(_translate("main_win", "3"))
        self.rbtn_day_7.setText(_translate("main_win", "7"))
        self.rbtn_day_31.setText(_translate("main_win", "31"))
        self.rbtn_day_100.setText(_translate("main_win", "100"))
        self.rbtn_day_365.setText(_translate("main_win", "365"))
        self.pbtn_generate.setText(_translate("main_win", "???????????????"))
