'''
Created on Mar 7, 2019

@author: vkhoday
'''

import teradata as td
import pandas as pd
import teradatasql as tds
from PIL import Image,ImageDraw

with tds.connect('{"host":"localhost","user":"UID","password":"pwd"}') as con:
    with con.cursor() as cur:
        cur.execute('select * from tabs')
        row = cur.fetchall()
# driver=webdriver.phan