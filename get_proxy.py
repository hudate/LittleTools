#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import time

need_modules = ["requests", "lxml", "csv", "pymongo"]
you_need_modules = []

for module in need_modules:
    try:
        __import__(module)
    except:
        you_need_modules.append(module)

print("你需要安装库：%s" % you_need_modules)
print("你可以使用: pip install %s 来安装你所需要的库。" % str(you_need_modules).replace("', '", ' ')[2:-2])

import requests
from lxml import etree
import csv
import pymongo

class GetProxy(object):
    """ 获取代理IP，包括国内的和国外的。"""

    def __init__(self, writeproxy=True):

        """
            self.__getIP_ip: 获取代理IP的网址，
            self.__filename: 保存代理IP，
            self.__writeInfo: 设置是否保存代理信息到本地csv文件
        """

        self.__get_proxy_dict = {
                '国内高匿代理': 'https://www.xicidaili.com/nn/',
                '西拉免费代理IP': 'http://www.xiladaili.com/gaoni/'
            }
        self.__filename = "Proxy_IP.csv"
        self.__is_write_info = writeproxy
        self.__ip_proxy_cn = {}     # 国内高匿代理
        self.__ip_proxy_fr = {}     # 国外高匿代理
        self.__collection = ''
        self.__set_mongodb()

    def __set_mongodb(self):
        mongo = pymongo.MongoClient()
        db = mongo['ProxyInfo']
        self.__collection = db['proxy']
        return

    def __query_ip(self, ip, **kwargs):
        """ 请求IP代理的网址 """
        headers = {}
        params = {}
        data = {}
        name = kwargs['name']
        page = kwargs['page']

        if len(kwargs) > 0:
            headers = kwargs['headers']

            try:
                params = kwargs['params']
            except:
                pass

            try:
                data = kwargs['data']
            except:
                pass

        failed_count: int = 1
        while 1:
            print('%s:第%s页, 第%s次爬取' % (name, page, failed_count))
            res = requests.get(ip, headers=headers, params=params, data=data)
            if res.status_code == 200:
                result = {'code': res.status_code, 'info': res.text}
                print('%s:第%s页, 第%s次爬取成功。' % (name, page, failed_count))
                return result
            elif res.status_code == 503:
                print('%s:第%s页, 第%s次爬取失败！！！' % (name, page, failed_count))
                if failed_count == 3:
                    return {'code': res.status_code, 'info': '服务器出错'}
                time.sleep(0.2)
                failed_count += 1


    def __write_ip(self, infos):
        """
        把获取到的代理IP信息写入到本地csv文件中。
        :param infos: 代理IP信息
        """
        headers = list(infos[0].keys())
        rows = infos

        with open(self.__filename, 'w', newline='')as f:
            f_csv = csv.DictWriter(f, headers)
            f_csv.writeheader()
            f_csv.writerows(rows)


    def get_proxy(self):
        """
        解析请求到的网页内容，包括IP地址，端口号，地理位置，运营商该信息，最后检测时间
        """
        proxy_ip_infos = []

        for e_proxy in self.__get_proxy_dict:
            code, proxy_ip_info = self.__get_proxy(self.__get_proxy_dict[e_proxy], e_proxy)
            if code == 200:
                proxy_ip_infos.extend(proxy_ip_info)
                print('"%s"爬取完成！' % e_proxy)
            else:
                print('请求错误代码：%s，爬取"%s"出错，出错原因：%s。' % (code, e_proxy, proxy_ip_info))

        ip_proxy_dict = {
            '国内': self.__ip_proxy_cn,
            '国外': self.__ip_proxy_fr
        }

        if self.__is_write_info:        # 是否将信息写入文件
            self.__write_ip(proxy_ip_infos)
        return ip_proxy_dict


    def __get_proxy(self, ip, name):
        proxy_info = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        res = {}
        for index in range(1, 5):
            query_ip = ip + str(index)
            res = self.__query_ip(query_ip, headers=headers, name=name, page=index)
            if res['code'] == 200:
                et = etree.HTML(res['info'])

                if name == '国内高匿代理':
                    trs = et.xpath('//table[@id="ip_list"]//tr')[1:]
                    for tr in trs:
                        if float(tr.xpath('td//div[@class="bar"]/@title')[0].split('秒')[0]) < 1.2:
                            tds_text_list = [e_text for e_text in tr.xpath('td//text()') if '\n' not in e_text]
                            if tds_text_list[3] == '高匿':
                                proxy_info = self.__assamble_proxy(tds_text_list, name)

                if name == '西拉免费代理IP':
                    trs = et.xpath('//table[@class="fl-table"]//tr')[1:]
                    for tr in trs:
                        tds_text_list = [e_text for e_text in tr.xpath('td//text()') if '\n' not in e_text]
                        if float(tds_text_list[4]) < 3.5:
                            if tds_text_list[2].startswith('高匿'):
                                proxy_info = self.__assamble_proxy(tds_text_list, name)

        if res['code'] == 200:
            return res['code'], proxy_info
        elif res['code'] == 503:
            return res['code'], res['info']


    def __assamble_proxy(self, tds_text_list, name):
        e_ip_info = {}
        proxy_info = []
        proxy_type = proxy_ip = proxy_port = addr = alive_time = ''
        if name == '国内高匿代理':
            proxy_type = tds_text_list[4]
            proxy_ip = tds_text_list[0]
            proxy_port = tds_text_list[1]
            addr = tds_text_list[2]
            alive_time = tds_text_list[5]  # 生存时间，alive time

        if name == '西拉免费代理IP':
            proxy_type = tds_text_list[1][:-2]
            proxy_ip = tds_text_list[0].split(':')[0]
            proxy_port = tds_text_list[0].split(':')[1]
            addr = tds_text_list[3]
            alive_time = tds_text_list[5]  # 生存时间，alive time

        self.__assamble_proxy_ip(proxy_type, proxy_ip, proxy_port,name)
        e_ip_info['IP地址'] = proxy_ip
        e_ip_info['端口'] = proxy_port
        e_ip_info['类型'] = proxy_type
        e_ip_info['服务器地址'] = addr
        e_ip_info['生存时间'] = alive_time
        e_ip_info['是否高匿'] = '高匿'
        proxy_info.append(e_ip_info)
        return proxy_info


    def __assamble_proxy_ip(self, proxy_type, proxy_ip, proxy_port, name):
        proxy_type = str(proxy_type)
        proxy = proxy_ip + ":" + proxy_port

        if name == '西拉免费代理IP':
            if len(proxy_type) == 4 or len(proxy_type) > 6:
                proxy_type = 'HTTP'
            if len(proxy_type) == 5 or len(proxy_type) > 6:
                proxy_type = 'HTTPS'

        try:
            self.__ip_proxy_cn[proxy_type].append(proxy)
            proxy_info = {'ip': proxy_ip, 'port': proxy_port, 'type': proxy_type}
            print(proxy_info)
            print(self.__collection)
            self.__collection.insert_one(proxy_info)
        except:
            self.__ip_proxy_cn[proxy_type] = []
            self.__ip_proxy_cn[proxy_type].append(proxy)


if __name__ == '__main__':
    print("使用说明： \n\t"
          "1.请确保安装了requests 和 lxml;\n\t"
          "2.把该文件放到需要代理的项目中;\n\t"
          "3.导入类名：from xxx.get_proxy import GetProxy; \n\t"
          "4.实例化对象：proxy = GetProxy();\n\t"
          "5.获取代理信息：proxy_list = proxy.get_proxy()\n\n")

    proxy = GetProxy(writeproxy=False)
    proxy_info = proxy.get_proxy()

    try:
        [print('\t共爬取%s个"%s:%s"代理，输出信息(该信息每次可能会不同)：\n\t\t%s\n\n' % (len(proxy_info[key1][key2]), key1,
            key2, proxy_info[key1][key2])) for key1 in proxy_info.keys() for key2 in proxy_info[key1]]
    except:
        print('未获取到任何代理ip.')

    print('说明：\n\t'
          '在使用上面的设置后，在该文件的 同级目录 下会生成一个文件： "Proxy_IP.csv" , '
          '如果不想生成该文件，则可以在实例化类时，设置：proxy = GetProxy(writeproxy=False)\n\n')

    input('按"Enter"退出......')