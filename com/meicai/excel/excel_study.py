#coding=utf-8
'''

@author: ldl

'''

###
###  update 20160801
###     A0       B1         C2         D3       E4      F5        G6          H7       I8       J9
###  接口地址    endpoint    method    headers    json    code    scene_desc    exec    result     pass


import os
import requests
import xlrd
import json

from xlutils.copy import copy
from sys import argv


ls = os.linesep
sep_o = os.path.sep
testcase=''

if len(argv) == 1:
#     testcase_dir = 'testdata%s' % sep_o
#     testcase = testcase_dir + 'test.xls'
    testcase = 'test20160802.xls'
elif len(argv) == 2:
    testcase = argv[1]
print testcase

def doTest():
    data = xlrd.open_workbook(testcase)
    table = data.sheet_by_index(0)
    write_data = copy(data) 
    for row in range(1,table.nrows):
        callAPI(write_data,row,tuple(table.row_values(row)))   
    write_data.save(testcase) 

def callAPI(write_data,row,params):
    if params[7] == 'yes':
        resp_json=''
#         print params
        resp = requests.request(params[2],params[0]+params[1],headers=eval(params[3]),json=eval(params[4]))        
        print row,"RESP::",resp.text
        resp_json = resp.json()        
#         print "##############",resp_json,"##############",type(resp_json)
#         print "@@@@@@@@@@@@@@",json.dumps(resp_json),"@@@@@@@@@@@@@@",type(json.dumps(resp_json))
        write_data.get_sheet(0).write(row,8,json.dumps(resp_json,indent=4,ensure_ascii=False))  
        pass_res="No"
        resp_code = resp_json.get('code',None)
#         print resp_code,type(resp_code),params[5],type(params[5]),type(int(resp_code))
        if int(resp_code) == int(params[5]):
#             print "____"
            pass_res ="Yes"
        write_data.get_sheet(0).write(row,9,pass_res)           


if __name__ == "__main__":
    doTest()
        
        
        
    
    



