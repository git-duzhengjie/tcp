# coding:utf-8
#
# 该模块用于处理与IP相关的主题功能
# 包括查询ISP、city、其他信息等
#
import urllib2
import json
import socket

socket.setdefaulttimeout(1)

def highlight(s):
    return "%s[30;2m%s%s[1m" % (chr(27), s, chr(27))


def in_red(s):
    return highlight('') + "%s[31;2m%s%s[0m" % (chr(27), s, chr(27))


def lookup_isp(ip):
    """

    :param ip: 查询的IP
    :return: IP的ISP（运营商）名
    """
    url = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" % ip
    try:
        sock = urllib2.urlopen(url, timeout=1)
        data = json.loads(sock.read())
        if data['code'] == 0:
            return data['data']['isp']
        else:
            return None
    except urllib2.URLError, e:
        print "Url Error:", str(e)
        print in_red(url)
        return None
    except socket.timeout:
        print "Timed out!"
        return None


def lookup_city(ip):
    """

    :param ip: 查询的IP
    :return: IP对应的城市
    """
    url = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" % ip
    try:
        sock = urllib2.urlopen(url, timeout=1)
        data = json.loads(sock.read())
        if data['code'] == 0:
            return data['data']['city']
        else:
            return None
    except urllib2.URLError, e:
        print "Url Error:", str(e)
        print in_red(url)
        return None
    except socket.timeout:
        print "Timed out!"
        return None


def lookup_detail(ip):
    """

    :param ip: 查询的IP
    :return: IP对应的国家、地区（西南、华中、华南、华北、华东、东北、西北）、省、市
    """
    url = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" % ip
    try:
        sock = urllib2.urlopen(url, timeout=1)
        data = json.loads(sock.read())
        if data['code'] == 0:
            data = data['data']
            return data['country'] + data['area'] + data['region'] + data['city']
        else:
            return None
    except urllib2.URLError, e:
        print "Url Error:", str(e)
        print in_red(url)
        return None
    except socket.timeout:
        print "Timed out!"
        return None


def lookup_all(ip):
    """

    :param ip: 查询的IP
    :return: IP所对应的所有信息
    """
    url = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" % ip
    try:
        sock = urllib2.urlopen(url, timeout=1)
        data = json.loads(sock.read())
        if data['code'] == 0:
            data = data['data']
            return data
        else:
            return None
    except urllib2.URLError, e:
        print "Url Error:", str(e)
        print in_red(url)
        return None
    except socket.timeout:
        print "Timed out!"
        return None


def checkIPv4(ipStr):
    print '+++++++++++++++++++++++++++++++++++++++'
    print 'The Input Ip String is =', ipStr
    IPv4List = ipStr.split('.')
    print 'Ip String convert to ip List is =', IPv4List
    IPv4Count = len(IPv4List)
    print 'The Num of IPv4List is =', IPv4Count

    if 4 != IPv4Count:
        return False

    for i in range(0, IPv4Count):
        Each_IPv4_List_Len = len(IPv4List[i])
        print IPv4List[i], Each_IPv4_List_Len
        if Each_IPv4_List_Len < 1 or Each_IPv4_List_Len > 3:
            print "Error: The Len of %s is %d" % (IPv4List[i], Each_IPv4_List_Len)
            return False

        for j in range(0, Each_IPv4_List_Len):
            if IPv4List[i][j] < '0' or IPv4List[i][j] > '9':
                print "Error: The %s is not only number" % IPv4List[i]
                return False

        value_of_each_IPv4_List = int(IPv4List[i])
        if value_of_each_IPv4_List < 0 or value_of_each_IPv4_List > 255:
            print "The Number of %s is overflow" % IPv4List[i]
            return False

    if int(IPv4List[0]) == 0:
        if int(IPv4List[1]) == 0 and int(IPv4List[2]) == 0 and int(IPv4List[3]) == 0:
            pass
        else:
            print "Error: Not all is Zero"
            return False

    return True
