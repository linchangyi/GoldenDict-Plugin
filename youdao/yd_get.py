#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

import requests
from lxml import etree
from sys import argv

URL = "http://dict.youdao.com/w/eng/{}"


def translate(words):
    """函数说明：
    因为采用 get 方式 url 中要过滤掉 / 换成全角。否则引起url的解析错误。
    response.text 是 bytes 数据类型
    """
    # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/70.0.3538.67 Chrome/70.0.3538.67 Safari/537.36'}
    words = words.replace("/", "／")
    url = URL.format(words)

    response = requests.get(url, headers)
    selector = etree.HTML(response.text)  # 生成 selector  对象, 利用 xpath 获得内容

    # 移到外层, 否则会有空白
    scontainer = selector.xpath("//div[@id='scontainer']")[0]
    container = selector.xpath("//div[@id='container']")[0]
    scontainer.getparent().append(container)
    scontainer.getparent().remove(scontainer)

    # 隐藏
    hiddens = [
        ('class', 'c-topbar-wrapper'),
        ('class', 'dict-votebar'),
        ('id', 'topImgAd'),
        ('id', 'c_footer'),
        ('id', 'ads'),
    ]
    for hidden in hiddens:
        selector.xpath("//div[@%s='%s']" % hidden)[0].attrib['style'] = 'display:none'

    content = etree.tostring(selector, encoding='utf-8', method='html').decode('utf8')
    content = re.sub(r'href="(?:http://dict\.youdao\.com)?/w/eng/(.*?)/', r'href="\1"', content)
    return content


if __name__ == "__main__":
    """
    argv[1] 获得控制器输入的第一个参数
    """
    result = translate(argv[1])
    print(result)
