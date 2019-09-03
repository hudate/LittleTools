#!/usr/bin/env python3
# -*- coding:utf-8 -*-

need_modules = ["requests", "lxml", "csv"]
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

class GetProxy(object):

    """ 为了获取代理IP. """

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
        self.__ip_proxy_ot = {}     # 国外高匿代理


    def __query_ip(self, ip, **kwargs):
        """ 请求IP代理的网址 """
        headers = {}
        params = {}
        data = {}

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

        res = requests.get(ip, headers=headers, params=params, data=data)
        return res.text

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

        for e_proxy in self.__get_proxy_dict:
            if e_proxy == '国内高匿代理':     # 默认使用该网站
                self.__get_proxy(self.__get_proxy_dict[e_proxy])

        ip_proxy_dict = {
            '国内': self.__ip_proxy_cn,
            '国外': self.__ip_proxy_ot
        }

        return ip_proxy_dict

    def __get_proxy(self, ip):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        proxy_ip_infos = []
        for index in range(1, 11):
            query_ip = ip + str(index)
            res_text = self.__query_ip(query_ip, headers=headers)
            et = etree.HTML(res_text)
            trs = et.xpath('//table[@id="ip_list"]//tr')[1:]

            for tr in trs:
                if float(tr.xpath('td//div[@class="bar"]/@title')[0].split('秒')[0]) < 0.5:
                    tds_text_list = [e_text for e_text in tr.xpath('td//text()') if '\n' not in e_text]
                    if tds_text_list[3] == '高匿':
                        print(tds_text_list)
                        e_ip_info = {}
                        proxy_type = tds_text_list[4]
                        proxy_ip = tds_text_list[0]
                        proxy_port = tds_text_list[1]
                        addr = tds_text_list[2]
                        alive_time = tds_text_list[5]  # 生存时间，alive time
                        self.assamble_proxy(proxy_type, proxy_ip, proxy_port)
                        e_ip_info['IP地址'] = proxy_ip
                        e_ip_info['端口'] = proxy_port
                        e_ip_info['类型'] = proxy_type
                        e_ip_info['服务器地址'] = addr
                        e_ip_info['生存时间'] = alive_time
                        e_ip_info['是否高匿'] = '高匿'
                        proxy_ip_infos.append(e_ip_info)

        # 是否将信息写入文件
        if self.__is_write_info == True:
            self.__write_ip(proxy_ip_infos)

        return

    def assamble_proxy(self, proxy_type, proxy_ip, proxy_port):
        proxy_type = str(proxy_type)
        proxy = proxy_ip + ":" + proxy_port
        try:
            self.__ip_proxy_cn[proxy_type].append(proxy)
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

    proxy = GetProxy()
    proxy_info = proxy.get_proxy()

    print('输出信息(该信息每次可能会不同)：\n\t%s\n\n' % proxy_info)

    print('说明：\n\t'
          '在使用上面的设置后，在该文件的 同级目录 下会生成一个文件： "Proxy_IP.csv" , '
          '如果不想生成该文件，则可以在实例化类（第三步）时，设置：proxy = GetProxy(writeproxy=False)\n\n')

    input('按"Enter"退出......')



    
