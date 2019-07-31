#!/usr/bin/env python
# -*- coding:utf-8 -*-

need_modules = ["requests", "lxml", "csv"]


for module in need_modules:
    try:
        __import__(module)
    except:
        print("你需要安装库：%s"%module)


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

        self.__getIP_ip = "http://www.89ip.cn/"
        self.__filename = "Proxy_IP.csv"
        self.__writeInfo = writeproxy


    def __query_ip(self):
        """ 请求IP代理的网址 """

        res = requests.get(self.__getIP_ip)
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
        res_text = self.__query_ip()
        et = etree.HTML(res_text)
        ip_selectors = et.xpath('//table[@class="layui-table"]//tr/td[1]')
        port_selectors = et.xpath('//table[@class="layui-table"]//tr/td[2]')
        location_selectors = et.xpath('//table[@class="layui-table"]//tr/td[3]')
        servicer_selectors = et.xpath('//table[@class="layui-table"]//tr/td[4]')
        last_detect_selectors = et.xpath('//table[@class="layui-table"]//tr/td[5]')

        ip_info_list = []
        ip_proxy = []

        for index in range(1, len(ip_selectors)):
            e_ip_info_dict = {}
            ip_e_proxy = "https://" + ip_selectors[index].xpath('normalize-space(text())') + ":" + port_selectors[index].xpath('normalize-space(text())')
            e_ip_info_dict['IP地址:端口'] = ip_e_proxy
            e_ip_info_dict['运营商'] = servicer_selectors[index].xpath('normalize-space(text())')
            e_ip_info_dict['地理位置'] = location_selectors[index].xpath('normalize-space(text())')
            e_ip_info_dict['最后检测'] = last_detect_selectors[index].xpath('normalize-space(text())')
            ip_proxy.append(ip_e_proxy)
            ip_info_list.append(e_ip_info_dict)

        if self.__writeInfo:
            self.__write_ip(ip_info_list)

        return ip_proxy

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



    
