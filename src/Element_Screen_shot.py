'''
Created on Mar 8, 2019

@author: vkhoday
'''

from selenium import webdriver
 
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.binary_location = "/usr/bin/chromium"
driver = webdriver.Chrome(chrome_options=options)
 
driver.get('https://python.org')
driver.save_screenshot("screenshot.png")
 
driver.close()