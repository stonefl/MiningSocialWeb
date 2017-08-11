# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 21:38:36 2017

@author: 5004756
"""

from urllib.request import ProxyHandler, urlopen, build_opener,install_opener
import re

proxy = ProxyHandler({'https': 'https://internet.proxy.fedex.com:3128'})
# construct a new opener using your proxy settings
opener = build_opener(proxy)
# install the openen on the module-level
install_opener(opener)

#html = urlopen("https://www.lightspacetime.art/seasons-2017-art-exhibition-special-merit-category/")
html = urlopen("https://www.lightspacetime.art/seasons-2017-art-exhibition-special-merit-category/")

text = html.read('http://python.org/')

for s in re.findall(r'(\w+@\w+\.com)', str(text)):
    print(s)

