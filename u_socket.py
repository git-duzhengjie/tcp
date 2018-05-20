# coding:utf-8
# description:
# python version:
# version:v1.0
# author:杜政颉
# time:2016/8/17 15:53
# Copyright 成都简乐互动远景科技公司版权所有®
import socket

master = ('127.0.0.1', 5566)


def get_16_int(integer):
    return str(integer).rjust(16)


class Udp:
    def __init__(self, sock):
        self.sock = sock

    def set_timeout(self, timeout):
        self.sock.settimeout(timeout)

    def sendto(self, data, addr):
        data_length = len(data)
        self.sock.sendto(get_16_int(data_length), addr)
        current_length = 0
        while current_length < data_length:
            self.sock.sendto(data[current_length:current_length + 1024], addr)
            current_length += 1024

    def recv_data(self):
        recv = ''
        data, addr = self.sock.recvfrom(16)
        recv_length = int(data.strip())
        if recv_length == 0:
            return ''
        current_length = 0
        while 1:
            data, addr = self.sock.recvfrom(((recv_length-current_length) >= 1024 and 1024 or (recv_length-current_length)))
            current_length += len(data)
            recv += data
            if current_length == recv_length:
                break
        return recv, addr

udp = Udp(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
udp.set_timeout(1)