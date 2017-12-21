#coding=utf-8
'''

@author: ldl

'''

###
###  update 20160801
###     A0       B1         C2         D3       E4      F5        G6          H7       I8       J9
###  接口地址    endpoint    method    headers    json    code    scene_desc    exec    result     pass

###  update 20160811
###   0        1         2          3         4       5       6          7             8            9         10         11
### 接口地址    endpoint    method    headers    json    data    params    checkpoint    scene_desc    exec    resp_body    pass

import os
import requests
import xlrd
import json

from xlutils.copy import copy
from sys import argv

# import time

ls = os.linesep
sep_o = os.path.sep
testcase=''

if len(argv) == 1:
    testcase = u'20171220_ZROBOT盘古分数 _stb.xls'
#     testcase = u'20171220_ZROBOT盘古分数 _prd.xls'
 
elif len(argv) == 2:
    testcase = argv[1]
print testcase


pass_count = 0
case_count = 0

def doTest():
    print u"####----    执行中..."
    data = xlrd.open_workbook(testcase)
    table = data.sheet_by_index(0)
    write_data = copy(data) 
    for row in range(1,table.nrows):
#         time.sleep(1)
        callAPI(write_data,row,tuple(table.row_values(row)))   
    write_data.save(testcase) 
    print u"####----    总共%s个CASE,通过%s个 CASE" % (case_count,pass_count)

def callAPI(write_data,row,params):
    if params[9] == 'yes':
        global case_count
        case_count += 1
        resp =''
        resp_json=''
        resp_text=''
#         print params
        if params[2] == "POST":
            if params[4]:
                resp = requests.request(params[2],params[0]+params[1],headers=eval(params[3]),json=eval(params[4]))        
               
            elif params[5]:
                resp = requests.request(params[2],params[0]+params[1],headers=eval(params[3]),data=eval(params[5]))        
        elif params[2] == "GET":
            resp = requests.request(params[2],params[0]+params[1],headers=eval(params[3]),params=eval(params[6]))        
        print row,"RESP::",resp.text
        try:
            resp_json = resp.json()
            json_string = json.dumps(resp_json,indent=4,ensure_ascii=False)
            if len(json_string)> 32737:                
                with open("%s%s.txt" % (testcase,row+1),"w") as f1:
                    f1.write(json_string.encode("gbk"))
                json_string=u'响应值过大，请参看日志记录'
#             print "##########",json_string 
            write_data.get_sheet(0).write(row,10,json_string)  
        except ValueError:
            resp_text = resp.text
#             print "##########",resp_text
            write_data.get_sheet(0).write(row,10,resp_text)  
 
        pass_res = "FAIL"  
              
        if isinstance(resp_json,dict) and params[7]:            
            pass_num = 0             
            check_point_dict = eval(params[7])
            for i in check_point_dict:
                if resp_json.get(i,None) == check_point_dict[i]:
#                     print "AAA=",resp_json.get(i,None),"--","BBB=",check_point_dict[i]
                    pass_num += 1
            check_point_dict_length = len(check_point_dict)
            if pass_num == check_point_dict_length:
                pass_res = 'PASS'
                global pass_count
                pass_count += 1
#                 print u"####通过的checkpoint数为%s，checkpoint总数为：%s！####" % (pass_num,check_point_dict_length)
        write_data.get_sheet(0).write(row,11,pass_res)
                  

if __name__ == "__main__":
    doTest()
 
