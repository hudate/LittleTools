#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from urllib.parse import urlencode
import requests
import sys
from lxml import etree


class YDDict(object):

    def __init__(self, content):
        self.__lookup_url = 'http://dict.youdao.com/w/eng/'
        self.__str = '/#keyfrom=dict2.index'
        self.__content = content
        self.__parse()

    def __get_first_html(self):
        dict = {'content': self.__content}
        content_uri = urlencode(dict).split('=')[1]
        res = requests.get(url=self.__lookup_url + content_uri + self.__str)
        return res.text

    def __is_chinese(self):
        for char in self.__content:
            uchar = char.encode('unicode_escape')
            """判断一个unicode是否是英文字母"""
            if uchar[2:] >= b'4e00' and uchar[2:] <= b'9fa5':
                return True
        else:
            return False

    # 解析原词为汉字的词汇的翻译意思
    def __parse_src_chinese(self, et):
        # print('汉译英')
        word_means = {}
        words_p = et.xpath('//div[@class="results-content"]//div[@class="trans-container"]//p['
                           '@class="wordGroup"]')
        for p in words_p:
            e_type = p.xpath('span/text()')[0]
            words = p.xpath('span//a/text()')
            word_means[e_type] = words
        return word_means, 'zh->en'

    # 解析原词为英语的词汇的翻译意思
    def __parse_src_english(self, et):
        # print('英译汉')
        means = et.xpath('//div[@class="results-content"]/div[@id="phrsListTab"]//ul/li/text()')
        types = [mean.split('.')[0] + '.' if '.' in mean else mean.split('.')[0] for mean in means]
        try:
            words = [mean.split('.')[1] if mean.split('.')[0] == '' else mean.split('. ')[1] for mean in means]
        except:
            words = [str(a) for a in range(len(types))]
        word_means = dict(zip(words, types))
        # print(word_means)
        return word_means, 'en->zh'

    # 解析被翻译的词汇极其语音
    def __parse_src(self, et):
        src_word = {}
        try:
            keywords: str = et.xpath('//div[@class="results-content"]/div/h2//span[@class="keyword"]/text()')[0]
        except:
            maykeywords = et.xpath('//div[@class="results-content"]/div/div//span/a/text()')
            print('输入有误, 也许你想查找:')
            [print(keyword) for keyword in maykeywords]
            exit()
        try:
            phonetic: str = et.xpath('//div[@class="results-content"]/div/h2//span[@class="phonetic"]/text()')[0]
        except:
            phonetic: str = ''
        src_word[keywords] = phonetic
        self.__print(src_word)

    # 解析基本的翻译词汇
    def __parse_baseTrans(self, et):
        is_chinese = self.__is_chinese()  # 判断查询的词是否是包含汉字
        if is_chinese:  # 包含汉字
            word_means = self.__parse_src_chinese(et)
        else:  # 没有汉字
            word_means = self.__parse_src_english(et)
        self.__print(word_means)

    def __parse_webTrans(self, et):
        pass


    # 解析翻译信息
    def __parse(self):
        req_text = self.__get_first_html()
        et = etree.HTML(req_text)
        self.__parse_src(et)    # 解析词汇和语音
        self.__parse_baseTrans(et)      # 解析基本的翻译意思
        self.__parse_webTrans(et)       # 解析网络词义

    # 输出信息
    def __print(self, word_means):
        if len(word_means) > 1:
            if word_means[1] == 'zh->en':   # 中文词汇->英文单词， {词性:英语单词}
                word_means = word_means[0]
                for a in word_means:
                    print(a, end=' ')
                    for b in word_means[a]:
                        print(b, end='; ')
                    print()
            else:   # 英文单词->中文词汇， {汉语词汇:汉字词汇词性}
                word_means = word_means[0]
                for a in word_means:
                    print(word_means[a], end=' ')
                    if not a.isdigit():
                        print(a)
                    else:
                        print()
        else:
            [print(a, word_means[a]) for a in word_means]


if __name__ == '__main__':
    content = sys.argv[1:]
    if len(content) != 0:
        if len(content) != 1:
            content = ' '.join(content)
        else:
            content = content[0]
    else:
        while 1:
            content = input('请输入您要翻译的内容：')
            if len(content) != 0:
                break

    yd = YDDict(content)

