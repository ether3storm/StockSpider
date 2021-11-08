# !/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
爬虫调用主程序，定时提供服务
'''

__author__ = '刘星河'

import os
import sys
import time
import spider
import argparse


def check_time(t: str) -> bool:
    return (t.isdecimal()) and (t >= '1800') and (t <= '2300') and (t[2:] < '60')


if __name__ == '__main__':
    os.chdir(sys.path[0])
    parser = argparse.ArgumentParser(description='spider program for getting stock data using netease api')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-u', '--updatestock', action='store_true', help='更新股票代码')
    group.add_argument('-g', '--getdata', action='store_true', help='获取历史行情数据')
    group.add_argument('-t', '--time', help='指定每日更新时间（1800后2300前）')
    args = parser.parse_args()
    if (args.time != None) and (not check_time(args.time)):
        raise ValueError('invalid time set')

    # print(args.updatestock)
    # print(args.getdata)
    # print(args.time)
    
    if (not args.updatestock) and (not args.getdata) and (args.time==None):
        while True:
            state = input('请输入指定模式[u, g, t, e]：\nu：更新股票代码\ng：获取历史行情数据\nt：指定每日更新时间\ne：退出\n')
            if state == 'u':
                args.updatestock = True
                break
            elif state == 'g':
                args.getdata = True
                break
            elif state == 't':
                args.time = input('请输入每日更新时间（1800后2300前）')
                if not check_time(args.time):
                    print('invalid time set')
                    args.time = None
                    continue
                break
            elif state == 'e':
                exit()
            else:
                print('输入指定模式有误')
    
    if args.updatestock:
        print('开始更新股票代码')
        spider.get_stockcode()
    if args.getdata:
        print('开始获取历史行情数据')
        spider.get_historical_data()
    if args.time:
        print('开始部署实盘每日更新，更新时间为每日%s' % args.time)
        while True:
            now = time.strftime('%Y%m%d%H%M', time.localtime())
            if now[-4:] == args.time:
                spider.update_data(now[:8])
                time.sleep(72000)
            time.sleep(60)
