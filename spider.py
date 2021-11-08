# !/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
使用网易财经api获取股票历史行情数据及更新数据
'''

__author__ = '刘星河'

import requests
import time
from tqdm import tqdm
import logging
logging.basicConfig(filename=__file__+'.log', format='%(asctime)s @ %(filename)s-%(levelname)s: %(message)s',
                    level=logging.INFO, filemode='a', datefmt='%Y-%m-%d %H:%M:%S')

__headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'
        }


def get_stockcode():
    base_url = 'http://quotes.money.163.com/'
    base_stock_pool = ['060', '100', '130', '068']
    with open('stockcode.csv', 'w') as f:
        for base_stock in base_stock_pool:
            for code in tqdm(range(10000), desc='getting stock code on %s' % base_stock):
                url = base_url+base_stock+'%04d'%code+'.html'
                time.sleep(0.01)
                try:
                    resp = requests.get(url=url, headers=__headers, timeout=60.0)
                    resp.raise_for_status()
                except Exception as e:
                    if resp.status_code == 404:
                        continue
                    else:
                        logging.error(e.__repr__())
                        raise e
                if '对不起!您所访问的页面不存在或者已删除。' not in resp.text:
                    f.write(base_stock+'%04d'%code+'\n')
    print('股票代码更新完成')
    logging.info('股票代码更新完成')


def get_historical_data():
    with open('stockcode.csv', 'r') as f:
        code_list = f.read().splitlines()
    for code in tqdm(code_list[3000:], desc='getting historical data'):
        url = 'http://quotes.money.163.com/service/chddata.html?code=%s' % code
        time.sleep(0.01)
        try:
            resp = requests.get(url=url, headers=__headers, timeout=60.0)
            resp.raise_for_status()
        except Exception as e:
            logging.error(e.__repr__())
            raise e
        resp_data = resp.content.decode('gbk').split('\n')
        with open('data/%s.csv'%code, 'w') as f:
            f.write(resp_data[0])
            for i in range(2, len(resp_data)):
                f.write(resp_data[-i])
    print('股票历史行情数据下载完成')
    logging.info('股票历史行情数据下载完成')


def update_data(date):
    with open('stockcode.csv', 'r') as f:
        code_list = f.read().splitlines()
    for code in tqdm(code_list, desc='updating data'):
        url = 'http://quotes.money.163.com/service/chddata.html?code=%s&start=%s&end=%s' % (code, date, date)
        time.sleep(0.01)
        try:
            resp = requests.get(url=url, headers=__headers, timeout=60.0)
            resp.raise_for_status()
        except Exception as e:
            logging.error(e.__repr__())
            raise e
        resp_data = resp.content.decode('gbk').split('\n')
        if len(resp_data) == 2:
            continue
        elif len(resp_data) == 3:
            with open('data/%s.csv'%code, 'r') as f:
                exist_data = f.read().splitlines()
                if resp_data[1][:-1] in exist_data:
                    continue
            with open('data/%s.csv'%code, 'a') as f:
                f.write(resp_data[1])
        else:
            logging.warning('wrong new data length while updating data @ %s on %s' % (code, date))
    print('股票%s数据更新完成' % date)
    logging.info('股票%s数据更新完成' % date)


if __name__ == '__main__':
    pass