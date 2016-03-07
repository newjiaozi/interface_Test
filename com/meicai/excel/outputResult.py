#coding=utf-8
'''
Created on 2016年3月2日

@author: Administrator
'''

import time
from bs4 import  BeautifulSoup



now = time.strftime('%Y%m%d-%H%M%S',time.localtime())
fail_num=0
time_sum=0

def outpu(argLists):
    with open('model.html','r') as res:
        soup = BeautifulSoup(res,"html.parser")
        summary = soup.find(id='summary')
        argLists_lenth = len(argLists)
        
        for i in argLists:
            global fail_num
            global time_sum
            if i[2]=='No':                
                fail_num += 1            
            time_sum += float(i[3])
        suc_rate_float = (argLists_lenth-fail_num)/float(argLists_lenth)*100
        print type(suc_rate_float)
        suc_rate = "%.2f%%"  % suc_rate_float
        avg_time = time_sum/argLists_lenth
        str_avg_time = '%.3f' % avg_time
        handelTrTd(summary, [str(argLists_lenth),str(fail_num),suc_rate,str_avg_time])
        detail = soup.find(id='detail')        
        for i in range(len(argLists)):
            print '#########',argLists[i]
            detail_result = BeautifulSoup('<tr valign="top" class=""><td></td><td align="left"></td><td align="center"></td><td align="right"></td></tr>', "html.parser")
            detail.append(handelTrTd(detail_result.tr, argLists[i]))

        writeHtml(soup.prettify(encoding='utf-8'))
    

def writeHtml(soup):
    with open('%s_result.html' % now,'w') as ht:
        ht.writelines(soup)
# 将数据添加到td中,tag就是trtd的html，argList为四位数据，最终返回添加数据的trtd
def handelTrTd(tag,argList):
#     print tag,argList,"@@@@@@@@@"
    tag_contents = tag.contents
#     print tag_contents
    for i in range(len(tag_contents)):
        tag_contents[i].string = argList[i] 
    return tag 
