'''
Created on Mar 8, 2019

@author: vkhoday
'''
from PIL import Image, ImageDraw
from io import BytesIO
from selenium import webdriver
import datetime
import os
import sys
import HtmlTestRunner
import unittest

class ScreenAnalysis(unittest.TestCase):

    STAGING_URL = 'https://www.google.com/search?q=NYSE%3A+DXC&oq=NYSE%3A+DXC&aqs=chrome..69i57j69i58.4562j0j7&sourceid=chrome&ie=UTF-8'
    PRODUCTION_URL = 'https://www.google.com/search?q=NYSE%3A+DXC&oq=NYSE%3A+DXC&aqs=chrome..69i57j69i58.4562j0j7&sourceid=chrome&ie=UTF-8'
#     driver = webdriver.Chrome()
    
    
    def __init__(self):
        self.set_up()
        self.Test_capture_screens()
        self.analyze()
        self.clean_up()

    def set_up(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("start-maximized")
        self.options.add_argument("disable-infobars")
        self.driver = webdriver.Chrome(chrome_options=self.options)
#         self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def clean_up(self):
        self.driver.close()

    def Test_capture_screens(self):        
        self.screenshot(self.STAGING_URL, 'screen_Base.png')
        self.screenshot(self.PRODUCTION_URL, 'screen_NewCode.png')

    def screenshot(self, url, file_name):        
        print ("Capturing", url, "screenshot as", file_name, "...")
        self.driver.get(url)
#         xpath_logo= '//*[@id="automatedSlider"]'
        if file_name=='screen_Base.png':            
            elem_scr =self.driver.find_element_by_class_name("VADlJf")
            self.Elem_ScreenShot(elem_scr,file_name)
            
            
        else:            
            elem_scr =self.driver.find_element_by_class_name("VADlJf")
            self.Elem_ScreenShot(elem_scr,file_name)
#         self.driver.get_screenshot_as_png()
        print ("Done.")
    
    def Elem_ScreenShot(self,element,file_name):
        location=element.location
        size =element.size
        png = self.driver.get_screenshot_as_png()
        with Image.open(BytesIO(png)) as im:
            left=(location['x']- location['x']//20 )- location['x']// 20
            top=location['y'] - location['y']//5
            right =(location['x']-location['x']//20)+(size['width'] + size['width']//20)
            bottom =(location['y']-location['y']//20)  +(size['height'] + size['height']//5)
            im=im.crop((left,top,right,bottom))
            im.save('screenshots/{}'.format(file_name))
        
    def analyze(self):
        print("Image Analysis started !!!")
        screenshot_staging = Image.open("screenshots/screen_Base.png")
        screenshot_production = Image.open("screenshots/screen_NewCode.png")
        columns = 120 #Zooming into block size of the image Higher value more deep scan
        rows = 120
        screen_width, screen_height = screenshot_staging.size
        block_width = ((screen_width - 1) // columns) + 1 
        block_height = ((screen_height - 1) // rows) + 1
        Res = "Pass"
        for y in range(0, screen_height, block_height+1):
            for x in range(0, screen_width, block_width+1):
                region_staging = self.process_region(screenshot_staging, x, y, block_width, block_height)
                region_production = self.process_region(screenshot_production, x, y, block_width, block_height)

                if region_staging is not None and region_production is not None and region_production != region_staging:
                    draw = ImageDraw.Draw(screenshot_staging)
#                     draw = ImageDraw.Draw(screenshot_production)
                    
#                     draw.rectangle((x, y, x+block_width, y+block_height), outline = "red")
#                     draw.line((x, x+block_width), fill=256,width=block_width)
#                     draw.line((x, x+block_width), fill=128,width=block_width)
                    draw.rectangle((x, y, x+block_width, y+block_height), outline = "red")
                    Res="Fail"
        TM =datetime.datetime.now()
        TM=str(TM).replace(":","_")
        screenshot_staging.save("screenshots/result_BaseVsNew{}_{}.png".format(Res,TM))
        print("Image analysis Completed & result {} !!!".format(Res))


    def process_region(self, image, x, y, width, height):
        region_total = 0

        # This can be used as the sensitivity factor, the larger it is the less sensitive the comparison
#         factor = 100
        factor = 500
        for coordinateY in range(y, y+height):
            for coordinateX in range(x, x+width):
                try:
                    pixel = image.getpixel((coordinateX, coordinateY))
                    region_total += sum(pixel)/4
                except:
                    return

        return region_total/factor

if __name__ == "__main__":
    ScreenAnalysis()
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='C:/Users/vkhoday/eclipse-workspace/Pyunit_Selenium/Reports'))
    

