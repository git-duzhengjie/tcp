# coding:utf-8
# description:
# python version:
# version:v1.0
# author:杜政颉
# time:2016/6/29 10:50
# Copyright 成都简乐互动远景科技公司版权所有®


import socket
import traceback
import sys


def highlight(s):
    return "%s[30;2m%s%s[1m" % (chr(27), s, chr(27))


def in_red(s):
    return highlight('') + "%s[31;2m%s%s[0m" % (chr(27), s, chr(27))


def in_green(s):
    return highlight('') + "%s[32;2m%s%s[0m" % (chr(27), s, chr(27))


def get_16_int(integer):
    i = str(integer)
    return i.ljust(16, '0')


class Server:
    conn = None
    addr = None

    def __init__(self, host, port, nonblock=False):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((host, port))
            if nonblock:
                self.s.setblocking(0)
            self.s.listen(5)
            print(in_green(u'初始化服务器:{0}:{1}成功'.format(host, port)))
        except:
            traceback.print_exc()
            print(in_red(u'初始化服务器失败'))
            sys.exit()

    def accept(self):
        self.conn, self.addr = self.s.accept()
        print(in_green(u'接受到{0}请求'.format(self.addr)))
        return self.conn, self.addr

    def __del__(self):
        try:
            self.s.close()
        except:
            traceback.print_exc()


class SClient:
    def __init__(self, conn):
        self.conn = conn

    def recv_data(self, file_mode=False):
        recv = ''
        recv_length = int(self.conn.recv(16).strip())
        if recv_length == 0:
            return ''
        current_length = 0
        while 1:
            data = self.conn.recv(((recv_length-current_length) >= 1024 and 1024 or (recv_length-current_length)))
            current_length += len(data)
            recv += data
            if current_length == recv_length:
                break
        if not file_mode:
            print(in_green('recv data {0}'.format(recv)))
        return recv

    def send_data(self, data, file_mode=False):
        if not file_mode:
            print(in_green('send data {0}'.format(data)))
        self.conn.send(get_16_int(len(data)))
        self.conn.sendall(data)

    def close(self):
        self.conn.close()

    def __del__(self):
        self.conn.close()


class Client:
    host = None
    port = None

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.s.settimeout(None)
        # print(self.s.gettimeout())

    def conn(self, host, port):
        try:
            self.host = host
            self.port = port
            self.s.connect((host, port))
            print(in_green('connect {0}:{1}'.format(host, port)))
            return True
        except:
            print(in_red('connect {0}:{1}'.format(host, port)))
            traceback.print_exc()
            return False

    def reconnect(self):
        try:
            self.s.close()
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.s.connect((self.host, self.port))
            print(in_green('reconnect {0}:{1}'.format(self.host, self.port)))
            return True
        except:
            print(in_red('reconnect {0}:{1}'.format(self.host, self.port)))
            traceback.print_exc()
            return False

    def recv_data(self, file_mode=False):
        recv = ''
        recv_length = int(self.s.recv(16).strip())
        if recv_length == 0:
            return ''
        current_length = 0
        while 1:
            data = self.s.recv(((recv_length-current_length) >= 1024 and 1024 or (recv_length-current_length)))
            current_length += len(data)
            recv += data
            if current_length == recv_length:
                break
        if not file_mode:
            print(in_green('recv data {0}'.format(recv)))
        return recv

    def send_data(self, data, file_mode=False):
        if not file_mode:
            print(in_green('send data {0}'.format(data)))
        self.s.send(get_16_int(len(data)))
        self.s.sendall(data)

    def __del__(self):
        self.s.close()
