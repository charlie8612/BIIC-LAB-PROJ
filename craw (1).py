# -*- coding: utf-8 -*-
"""
Created on Tue May 02 17:33:40 2017

@author: Ryan
"""
import requests
import re
from opencc import OpenCC 
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
from bs4 import BeautifulSoup

def write_txt(inside, name):
    print(name)
    name  = 'E:\\BIIC\\jdth\\' + name + '.txt'
    f = open(name,'w', encoding = 'utf-8')
    f.write(inside)
    f.close()
    return 

def translate(inside_rejoin):
    openCC = OpenCC('s2t')
    inside_rejoin_converted = openCC.convert(inside_rejoin)
    return inside_rejoin_converted
    
def get_text(url):
    ip = url.split('/')
    ip = ip[3]
    html_code = requests.get(url)
    html_code.encoding = 'gbk'
    soup=BeautifulSoup(html_code.text, "html.parser")
    web=[]
    #for hit in soup.findAll('article'):  
        #web.append(hit.text)
    web = soup.findAll('article')
    inside = web[1].text
    inside_split = re.split('（.+?）', inside)
    inside_rejoin = ''.join(inside_split)
    inside_rejoin = inside_rejoin.split(' '); #split white space
    inside_rejoin = ''.join(inside_rejoin)                               
    ###############找下一頁########################
    for anchor in soup.findAll('a'):
        anchor_split = re.split('<.+?>', str(anchor))
        if(anchor_split[1] == '下一页'):
            anchor = str(anchor)
            anchor_url = anchor.split('\"')
            anchor_url = anchor_url[1]
            check_next = str(anchor_url)
            anchor_url = "http://wap.etgushi.com/" + ip + "/" + str(anchor_url)
            if(check_next != "#"):
                inside_rejoin = inside_rejoin + get_text(anchor_url)
            break
    ##############################################
    return inside_rejoin
    
def craw_url(url):#拿到該網頁裡面的所有網址
    func_base = requests.get(url, headers = header)
    soup_base = BeautifulSoup(func_base.text, "lxml")
    target=[]
    for hit in soup_base.findAll('a'):
        target.append(hit)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    tmp_arry=[]
    for point_x in target:
        tmp = point_x
        tmp = str(tmp)
        tmp = tmp.split('\"')
        try:
            if(tmp[2] == ">ÏÂÒ»Ò³</a>"):
                tmp = "/jdth/" + tmp[1]
                tmp_arry.append(tmp)
            elif((tmp[2] != ">Ê×Ò³</a>") & (tmp[2] != ">ÉÏÒ»Ò³</a>")):  #去掉首頁&上一頁
                tmp = tmp[1]
                tmp_arry.append(tmp)
        except:
            pass
    target=[]
    target = tmp_arry[2:-1]
    next_url=[]
    for point_x in target:
        next_url.append("http://wap.etgushi.com" + str(point_x))
    return next_url

story_num = 0

before_page = ''
current_page = 'http://wap.etgushi.com/jdth/'
while 1:
   urllist = craw_url(current_page)
   webtopaste=[]
   webtopaste = urllist[0:-1]    #獲得故事LINK
   next_page = urllist[-1]       #獲得下一頁LINK
   for point in webtopaste:
       story_num = story_num + 1
       text_inside = get_text(point)
       text_inside_translate = translate(text_inside)
       write_txt(text_inside_translate, str(story_num))
   current_page = next_page 