'''
Created on Mar 10, 2019

@author: vkhoday
'''

import pandas as pd
import pymssql 

conn = pymssql.connect(user='sa',password='password', host='.\\SQLEXPRESS', database='StockQuote',port='1433')
cur = conn.cursor()
cur.execute("select top 10 Script_Name, [Close], Volume, Change, Trnx_date from NSE_EOD where Trnx_date = (select MAX(Trnx_date) from NSE_EOD)")
BaseRes=cur.fetchall()
# print (BaseRes)
df_base = pd.DataFrame(BaseRes,columns=['Script_Name', 'Close', 'Volume',  'Change', 'Trnx_date'],dtype=float)

cur.execute("select top 6 Script_Name, [Close], Volume, Change, Trnx_date from NSE_EOD where Trnx_date = (select MAX(Trnx_date) from NSE_EOD)")
NewCode = cur.fetchall()
df_NewCode = pd.DataFrame(NewCode,columns=['Script_Name', 'Close', 'Volume',  'Change', 'Trnx_date'],dtype=float)


diff = set(zip(df_base.Script_Name,df_base.Close,df_base.Volume,df_base.Change,df_base.Trnx_date))-set(zip(df_NewCode.Script_Name,df_NewCode.Close,df_NewCode.Volume,df_NewCode.Change,df_NewCode.Trnx_date))
print ("BaseLine\n\n",df_base,'\n\n NewCode\n\n',df_NewCode,"\n\nDifference:- ")

str_diff =list(diff)
for row in str_diff:    
    print('Data Diff between DF1 & DF2 {}'.format(row))



