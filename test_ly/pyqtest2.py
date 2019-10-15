# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 12:03:59 2018

@author: ly
"""

html2 = '''
<div id="container">
    <ul class="list">
        <li class="item-0">first item</li>
        <li class="item-1"><a href="link2.html" target="_blank">second item</a></li>
        <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
        <li class="item-1 active"><a href="link4.html">fourth item</a></li>
        <li class="item-0"><a href="link5.html">fifth item</a></li>
    </ul>
     <ul class="list">
        <li class="item-0">first2 item</li>
        <li class="item-1"><a href="link2.html">second2 item</a></li>
        <li class="item-0 active"><a href="link3.html"><span class="bold">third2 item</span></a></li>
        <li class="item-1 active"><a href="link4.html">fourth2 item</a></li>
        <li class="item-0"><a sdfds="link5.html">fifth2 item</a></li>
    </ul>   
</div>
'''

from pyquery import PyQuery as pq
#初始化为PyQuery对象
doc2 = pq(html2)
print(type(doc2))
print(doc2)