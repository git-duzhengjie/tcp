# coding:utf-8
# description:
# author:duzhengjie
# time:2017/8/5 0005 下午 12:00
# Copyright 成都正扬科技有限公司版权所有®


from form.control import Control
import sys
import ctypes

reload(sys)
sys.setdefaultencoding('utf-8')


ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

if __name__ == '__main__':
    Control()
