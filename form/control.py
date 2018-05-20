# coding:utf-8
# description:
# author:duzhengjie
# time:2017/8/5 0005 下午 12:01
# Copyright 成都正扬科技有限公司版权所有®


import traceback
import sys
from PyQt4 import QtGui
from PyQt4.QtCore import QTranslator
from form.main import MainWindow


class Control:

    def __init__(self):
        try:
            self.a = QtGui.QApplication(sys.argv)
            self.m = MainWindow()
            self.m.show()
            translator = QTranslator()
            translator.load('qt_zh_CN.qm')
            self.a.installTranslator(translator)
            sys.exit(self.a.exec_())
        except:
            traceback.print_exc()