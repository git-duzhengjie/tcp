# coding:utf-8
# description:
# author:duzhengjie
# time:2017/8/5 0005 下午 12:05
# Copyright 成都正扬科技有限公司版权所有®
import socket

import chardet
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMessageBox, QFont
from PyQt4.QtCore import QTimer

from ip import checkIPv4
from ui.ui_tcp import Ui_MainWindow
from PyQt4 import QtGui, QtCore


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.plainTextEdit.setAlignment(QtCore.Qt.AlignHCenter)
        self.plainTextEdit.setStyleSheet("QLabel { color : red; }")
        font = QFont()
        font.setBold(True)
        font.setPointSize(72)
        self.plainTextEdit.setFont(font)
        self.hide_()
        self.setWindowTitle(u"UDPRunner")
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.stop)
        self.thread_group = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateUi)
        self.run_time = None
        self.n = 0
        self.isRunning = False

    @pyqtSlot()
    def start(self):
        try:
            if self.isRunning:
                msg_box = QMessageBox(QMessageBox.Warning, u"警告", u"当前程序正在运行")
                msg_box.exec_()
                return
            ip = unicode(self.lineEdit_5.text())
            port = int(unicode(self.lineEdit_6.text()))
            num = int(unicode(self.lineEdit_7.text()))
            self.run_time = int(unicode(self.lineEdit_8.text()))
            if ip.strip() == "" or not checkIPv4(ip):
                msg_box = QMessageBox(QMessageBox.Warning, u"警告", u"IP输入不合法")
                msg_box.exec_()
            else:
                self.run(ip, port, num)
        except ValueError:
            msg_box = QMessageBox(QMessageBox.Warning, u"警告", u"输入不合法")
            msg_box.exec_()

    def run(self, ip, port, num):
        for i in range(num):
            run_thread = RunThread(ip, port)
            self.thread_group.append(run_thread)
            run_thread.start()
        self.show_()
        self.timer.start(1000)
        self.isRunning = True

    @pyqtSlot()
    def stop(self):
        self.finish()

    def finish(self):
        for th in self.thread_group:
            th.stop()
            del th
        self.timer.stop()
        self.hide_()
        self.n = 0
        self.plainTextEdit.clear()
        self.isRunning = False
        self.thread_group = []

    @pyqtSlot()
    def updateUi(self):
        if self.n <= self.run_time:
            self.plainTextEdit.setText(u'{0}s'.format(self.run_time - self.n))
            self.n += 1
        else:
            self.finish()

    def show_(self):
        self.label_9.show()
        self.plainTextEdit.show()

    def hide_(self):
        self.label_9.hide()
        self.plainTextEdit.hide()


class RunThread(QtCore.QThread):
    def __init__(self, ip, port):
        super(RunThread, self).__init__()
        self.ip = ip
        self.port = port
        self.running = True

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.1)
        while self.running:
            sock.sendto('\377\377\377\377TSource Engine Query\0', (self.ip, self.port))
            # sock.sendto('\377\377\377\3775454121455785454874545487454578554487454875465487456487454785478547454\0'
            #             '\377\377\377\3775454121455785454874545487454578554487454875465487456487454785478547454\0'
            #             '\377\377\377\3775454121455785454874545487454578554487454875465487456487454785478547454\0'
            #             '\377\377\377\3775454121455785454874545487454578554487454875465487456487454785478547454\0'
            #             '\377\377\377\3775454121455785454874545487454578554487454875465487456487454785478547454\0'
            #             '\377\377\377\3775454121455785454874545487454578554487454875465487456487454785478547454\0'
            #             '\377\377\377\3775454121455785454874545487454578554487454875465487456487454785478547454\0'
            #             '\377\377\377\3775454121455785454874545487454578554487454875465487456487454785478547454\0'
            #             '\377\377\377\3775454121455785454874545487454578554487454875465487456487454785478547454\0'
            #             '\377\377\377\3775454121455785454874545487454578554487454875465487456487454785478547454\0'
            #             '\377\377\377\3775454121455785454874545487454578554487454875465487456487454785478547454\0'
            #             '\377\377\377\3775454121455785454874545487454578554487454875465487456487454785478547454\0'
            #             '', (self.ip, self.port))
            text = sock.recv(1024)
            # print(text)
            parsing(text)

    def stop(self):
        self.running = False


def parsing(txt):
    txt = txt.replace('\377', '')
    if txt.find('m') == 0:
        serv_name = txt.split('\0')[1]
        serv_map = txt.split('\0')[2]
        serv_engine = txt.split('\0')[3]
        serv_game = txt.split('\0')[4]
        print 'Server name:', serv_name.decode(chardet.detect(serv_name)['encoding'])
        print 'Game:', serv_game.decode(chardet.detect(serv_name)['encoding']), '(' + serv_engine + ')'
        print 'Map:', serv_map
        print(txt.split('\0'))[0]
    else:
        for l in txt.split('\0'):
            encoding = chardet.detect(l)['encoding']
            if encoding:
                try:
                    print(l.decode(encoding))
                except:
                    pass
