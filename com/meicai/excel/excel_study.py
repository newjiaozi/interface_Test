#coding=utf-8
'''
Created on 2016��2��27��

@author: Administrator
'''

###
# 
#      0       1        2            3            4         5      6      7      8       9      10     11
#    接口地址    接口名称    请求方法（POST/GET）      headers    params    data    json    预期结果    场景描述    是否执行    执行结果         结果解析
###
import os
import requests
import xlrd
from xlutils.copy import copy
from sys import argv
from outputResult import outpu

ls = os.linesep
testcase=''

if len(argv) == 1:
    testcase = 'passport_moni.xls'
elif len(argv) == 2:
    testcase = argv[1]
print testcase

argLists=[]

def doTest():
    data = xlrd.open_workbook(testcase)
    table = data.sheet_by_index(0)
    write_data = copy(data) 
    for row in range(1,table.nrows):
        callAPI(write_data,table,row,tuple(table.row_values(row)))

        
        
    write_data.save(testcase) 
#     print argLists,"###############"
    outpu(argLists)
                

def callAPI(write_data,table,row,params):
    pass_R ='No'
    print params
    if params[9] == 'yes':
        if params[6]:
            resp = requests.request(params[2],params[0]+params[1],headers=eval(params[3]),json=eval(params[6]))
#             print resp.json()
            if int(params[7]) == resp.json().get('ret',None):
                pass_R='Yes'     
            elif int(params[7]) == 0:
                error_code = resp.json().get('error_code',None)
                if error_code == 0:
                    pass_R='Yes'
            elif int(params[7]) ==1:
                error_code = resp.json().get('error_code',None)
                if error_code !=0 and error_code:
                    pass_R='Yes'                           
            argLists.append([params[1],params[8],pass_R,str(resp.elapsed.total_seconds())])  
            getResutJson(resp,write_data,row)             

        elif params[5]:
            resp = requests.request(params[2],params[0]+params[1],headers=eval(params[3]),data=eval(params[5]))

            if int(params[7]) == resp.json().get('ret',None):
                pass_R='Yes'     
            elif int(params[7]) == 0:
                error_code = resp.json().get('error_code',None)
                if error_code ==0:
                    pass_R='Yes'
            elif int(params[7]) ==1:
                error_code = resp.json().get('error_code',None)
                if error_code !=0 and error_code:
                    pass_R='Yes'        
            argLists.append([params[1],params[8],pass_R,str(resp.elapsed.total_seconds())]) 
            getResutJson(resp,write_data,row)
        elif params[4]:
            resp = requests.request(params[2],params[0]+params[1],headers=eval(params[3]),params=eval(params[4]))

            if int(params[7]) == resp.json().get('ret',None):
                pass_R='Yes'     
            elif int(params[7]) == 0:
                error_code = resp.json().get('error_code',None)
                if error_code ==0:
                    pass_R='Yes'
            elif int(params[7]) ==1:
                error_code = resp.json().get('error_code',None)
                if error_code !=0 and error_code:
                    pass_R='Yes'   
            argLists.append([params[1],params[8],pass_R,str(resp.elapsed.total_seconds())]) 
            getResutJson(resp,write_data,row)
    
def getResultText(resp,write_data,row):
    result = resp.text
    if result:
        write_data.get_sheet(0).write(row,10,result) 
def getResutJson(resp,write_data,row):   
    result = resp.json()
    output = handleResult(result)
    write_data.get_sheet(0).write(row,10,output)
         


def handleResult(result):
    output=''
    if result:
        ret = result.get('ret',None)
        if ret == 1:
            data = result.get('data')
            if isinstance(data, list) and data:
                for i in data:
                    for j in i:
                        output += u'%s : %s%s' % (j,i[j],ls)
            elif isinstance(data,dict) and data:
                for i in data:
                    output += u'%s : %s%s' % (i,data[i],ls)
            elif isinstance(data,int):
                output  = u'返回的ret=1返回的data=%d' % data              
            else:
                output = u'返回的ret=1返回的data=[]'
        elif ret == 0:
            error = result.get('error')
            for i in error:
                output += u'%s : %s%s' % (i,error[i],ls)
        error_code = result.get('error_code',None)
        if error_code ==0:
            data = result.get('data',None)
#             print "#Q@$#",data,type(data)
            if isinstance(data, list) and data:
                for i in data:
                    for j in i:
                        output += u'%s : %s%s' % (j,i[j],ls)
            elif isinstance(data,dict) and data:
                for i in data:
                    output += u'%s : %s%s' % (i,data[i],ls)
            elif isinstance(data,int):
                output  = u'返回的ret=1返回的data=%d' % data              
            else:
                output = u'返回的ret=1返回的data=[]'            
        elif error_code:
            output = result.get('error',u'错误号%d' % error_code) + ls + u'error_code：%d' % error_code            
            
    else:
        output = u'无结果返回'
    
    return output      
        
                        
                        
        
                         
                 
                     
                     
        

             


if __name__ == "__main__":
    doTest()
        
        
        
    
    



