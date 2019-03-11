'''
Created on Mar 5, 2019

@author: vkhoday
'''

from flask import Flask
from psycopg2.sql import SQL
import teradata as td
import pandas as pd

host,UID,password='Host','UID','PWD'

uadExec = td.UdaExec(appName="test",version="1.0",logConsole=False)

with uadExec.connect(method="odbc",system=host,username=UID,password=password,driver="DRIVERNAME") as connect:
    query ="select * from Junk;"
    


app = Flask(__name__)

@app.route('/flask')
def hello_flask():
   return 'Hello Flask Testing time !'

@app.route('/python/')
def hello_python():
   return 'Hello Python Testing time !'

if __name__ == '__main__':
   app.run(debug=True)