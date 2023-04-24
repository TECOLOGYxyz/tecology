#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import logging
from drivers import epd1in54b_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from gpiozero import CPUTemperature

# def initiateScreen():
#     epd = epd1in54b_V2.EPD() 
#     epd.init()
#     epd.Clear() 

def welcomeScreen(hostName, hostAddress, netStatus):
    cpu = CPUTemperature()
    cpu = str(round(cpu.temperature, 1))

    t = time.localtime(time.time())
    t = f'{t.tm_hour}:{t.tm_min} {t.tm_year}/{t.tm_mon}/{t.tm_mday}'

    epd = epd1in54b_V2.EPD() 
    epd.init()
    epd.Clear() 

    # Clear
    blackimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    redimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    
    #fontPath = os.path.join(os.getcwd(), "drivers", 'Font.ttc')
    fontPath = '/home/tecologyTrap1/tecology/Trap/drivers/Font.ttc'
    fontLarge = ImageFont.truetype(fontPath, 40)
    font = ImageFont.truetype(fontPath, 24)
    font18 = ImageFont.truetype(fontPath, 18)
    
    # Header
    drawblack = ImageDraw.Draw(blackimage)
    drawred = ImageDraw.Draw(redimage)

    #drawblack.text((8, 12), 'WELCOME', font = font, fill = 0)
    drawblack.text((30, 0), 'TECOLOGY.ai', font = font, fill = 0) # Bottom y is about 180
    #drawblack.text((30, 20), u'Trap 1', font = font18, fill = 0)

    # # # Write ip
    drawblack.text((2, 50), 'Host info', font = font, fill = 0)
    drawblack.text((2, 80), hostName, font = font18, fill = 0)
    drawblack.text((2, 110), hostAddress, font = font18, fill = 0)
    drawblack.text((2, 140), 'Internet: ' + netStatus, font = font18, fill = 0)

    # # # Time
    #drawblack.text((0, 180), u'Time: ', font = font18, fill = 0)
    drawblack.text((0, 180), t, font = font18, fill = 0)
    
    # # # CPU
    #drawblack.text((0, 150), u'CPU: ', font = font18, fill = 0)
    drawred.text((150, 180), cpu + " C", font = font18, fill = 0)

    epd.display(epd.getbuffer(blackimage),epd.getbuffer(redimage))
    
    epd.sleep()



#welcomeScreen()



def updateScreen(currentTime, CPUtemp):
    epd = epd1in54b_V2.EPD() 
    epd.init()
    epd.Clear() 

    # Clear
    blackimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    redimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    
    font = ImageFont.truetype(os.path.join("Trap", "drivers", 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join("Trap", "drivers", 'Font.ttc'), 18)
    
    # Header
    drawblack = ImageDraw.Draw(blackimage)
    drawred = ImageDraw.Draw(redimage)
    drawblack.rectangle((0, 10, 200, 38), fill = 0)
    drawblack.text((8, 12), 'TECOLOGY', font = font, fill = 255)
    drawblack.text((8, 36), u'Trap 1', font = font18, fill = 0)

    # Time
    #drawblack.text((0, 180), u'Time: ', font = font18, fill = 0)
    drawblack.text((0, 180), currentTime, font = font18, fill = 0)
    
    # CPU
    drawblack.text((0, 140), u'CPU: ', font = font18, fill = 0)
    drawred.text((45, 140), CPUtemp + " C", font = font18, fill = 0)

    epd.display(epd.getbuffer(blackimage),epd.getbuffer(redimage))
    
    epd.sleep()





# try:
#     logging.info("epd1in54b V2 Demo")
    
#     epd = epd1in54b_V2.EPD() 

#     logging.info("init and Clear")
#     epd.init()
#     epd.Clear()
#     time.sleep(1)


#     # Drawing on the image
#     logging.info("1.Drawing on the image...")
#     blackimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
#     redimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    
#     font = ImageFont.truetype(os.path.join("drivers", 'Font.ttc'), 24)
#     font18 = ImageFont.truetype(os.path.join("drivers", 'Font.ttc'), 18)
    
#     drawblack = ImageDraw.Draw(blackimage)
#     drawred = ImageDraw.Draw(redimage)
#     drawblack.rectangle((0, 10, 200, 34), fill = 0)
#     drawblack.text((8, 12), 'TECOLOGY', font = font, fill = 255)
#     drawblack.text((8, 36), u'Trap 1', font = font18, fill = 0)
#     # drawblack.line((16, 60, 56, 60), fill = 0)
#     # drawblack.line((56, 60, 56, 110), fill = 0)
#     # drawblack.line((16, 110, 56, 110), fill = 0)
#     # drawred.line((16, 110, 16, 60), fill = 0)
#     # drawred.line((16, 60, 56, 110), fill = 0)
#     # drawred.line((56, 60, 16, 110), fill = 0)
#     # drawred.arc((90, 60, 150, 120), 0, 360, fill = 0)
#     # drawred.rectangle((16, 130, 56, 180), fill = 0)
#     # drawred.chord((90, 130, 150, 190), 0, 360, fill = 0)
#     epd.display(epd.getbuffer(blackimage),epd.getbuffer(redimage))
#     time.sleep(10)
    
#     # # read bmp file 
#     # logging.info("2.read bmp file...")
#     # blackimage = Image.open(os.path.join("drivers", '1in54b-b.bmp'))
#     # redimage = Image.open(os.path.join("drivers", '1in54b-r.bmp'))    
#     # epd.display(epd.getbuffer(blackimage),epd.getbuffer(redimage))
#     # time.sleep(1)
    
#     # # read bmp file on window
#     # logging.info("3.read bmp file on window...")
#     # blackimage1 = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
#     # redimage2 = Image.new('1', (epd.width, epd.height), 255)
    
#     # newimage = Image.open(os.path.join(picdir, '100x100.bmp'))
#     # blackimage1.paste(newimage, (50,50))    
#     # epd.display(epd.getbuffer(blackimage1), epd.getbuffer(redimage2))
    
#     logging.info("Clear...")
#     epd.Clear()
    
#     logging.info("Goto Sleep...")
#     epd.sleep()
        
# except IOError as e:
#     logging.info(e)
    
# except KeyboardInterrupt:    
#     logging.info("ctrl + c:")
#     epd1in54b_V2.epdconfig.module_exit()
#     exit()
