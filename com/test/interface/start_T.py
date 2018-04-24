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
# from compiler.syntax import check
# from nntplib import resp

# import time

ls = os.linesep
sep_o = os.path.sep
testcase=''

if len(argv) == 1:
#     testcase = u'20180418_身份认证idauth_stb.xls'
    testcase = u'20180423_身份认证idauth_stb.xls'

#     testcase = u'20180416_身份认证_stb.xls'
 
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
        if params[2] == "POST":
            if params[4]:
                resp = requests.request(params[2],params[0]+params[1],headers=eval(params[3]),json=eval(params[4]))        
               
            elif params[5]:
                resp = requests.request(params[2],params[0]+params[1],headers=eval(params[3]),data=eval(params[5]))        
        elif params[2] == "GET":
            resp = requests.request(params[2],params[0]+params[1],headers=eval(params[3]),params=eval(params[6]))        
        print row+1,"RESP::",resp.text
        try:
            resp_json = resp.json()
            json_string = json.dumps(resp_json,indent=4,ensure_ascii=False)
            if len(json_string)> 32737:                
                with open("%s%s.txt" % (testcase,row+1),"w") as f1:
                    f1.write(json_string.encode("utf-8"))
                json_string=u'响应值过大，请参看日志记录'
            write_data.get_sheet(0).write(row,10,json_string)  
        except ValueError:
            resp_text = resp.text
            write_data.get_sheet(0).write(row,10,resp_text)  
 
        pass_res = "FAIL"  
              
        if isinstance(resp_json,dict) and params[7]:            
            pass_num = 0             
            check_point_dict = eval(params[7])
            for i in check_point_dict:
                check_data = check_point_dict[i]
                if isinstance(check_data, dict):
                    inner_pass_num = 0
                    for j in check_data:
                        try:
                            data_value = resp_json[i][j]
                            if isinstance(check_data[j],str) and check_data[j].startswith('LIKE'):
                                assert check_data[j][4:] in data_value
                                inner_pass_num +=1
                            else:
                                assert check_data[j] == resp_json[i][j]
                                inner_pass_num +=1
                        except Exception,e:
                            print e
                            break
                    if len(check_data) == inner_pass_num:
                        pass_num +=1
                    
                else:
                    if isinstance(check_data,str) and check_data.startswith('LIKE'):
                        if check_data[4:] in resp_json.get(i,None):
                            pass_num +=1
                    else:
                        if resp_json.get(i,None) == check_data:
                            pass_num += 1
                            
            check_point_dict_length = len(check_point_dict)
            if pass_num == check_point_dict_length:
                pass_res = 'PASS'
                global pass_count
                pass_count += 1
        write_data.get_sheet(0).write(row,11,pass_res)
                  

if __name__ == "__main__":
    doTest()
 
