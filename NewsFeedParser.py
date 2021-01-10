import os, time, threading, random
import feedparser
import qrcode


import RPi.GPIO as GPIO
from time import sleep, strftime
from datetime import datetime

from PIL import Image, ImageFont, ImageDraw
from random import shuffle

from luma.core.interface.serial import i2c, spi, noop
#from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.oled.device import ssd1327
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT

BITLY_ACCESS_TOKEN="BITLY_ACCESS_TOKEN"
items=[]
displayItems=[]
feeds=[
    #enter all news feeds you want here
    #"http://www.fda.gov/AboutFDA/ContactFDA/StayInformed/RSSFeeds/PressReleases/rss.xml",
    #"http://www.fiercepharma.com/feed",
    #"http://www.fiercebiotech.com/feed",
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "http://www.aljazeera.com/xml/rss/all.xml",
    "https://www.mlbtraderumors.com/feed",
    "https://www.mlb.com/feeds/news/rss.xml"
     ]

serial = spi(port=0, device=0, gpio = noop())
serial2= i2c(port=1, address=0x3D)
device = max7219(serial, width=32, height=8, block_orientation=-90)
device2 = ssd1327(serial2)
device.contrast(5)
virtual = viewport(device, width=32, height=16)
show_message(device, 'Dan is really awesome', fill="white", font=proportional(LCD_FONT), scroll_delay=0.08)

with canvas(device2, dither=True) as draw:
    draw.rectangle((10,10,30,30), outline="white", fill="red")

#try:
 #   while True:
  #      with canvas(virtual) as draw:
   #         text(draw, (0, 1), "Dan is really awesome", fill="white", font=proportional(CP437_FONT))
           #text(draw, (0, 1), datetime.now().strftime('%I:%M'), fill="white", font=proportional(CP437_FONT))

#except KeyboardInterrupt:
 #   GPIO.cleanup()

def populateItems():
    #first clear out everything
    del items[:]
    del displayItems[:]

    #delete all the image files
    #os.system("find . -name \*.ppm -delete")
    for url in feeds:
        feed=feedparser.parse(url)
        posts=feed["items"]
        for post in posts:
            items.append(post)
    shuffle(items)

def createLinks():
    try:
        populateItems()
        for idx, item in enumerate(items):
            #print(str(item["title"]), idx)
            show_message(device, str(item["title"]), fill="white", font=proportional(LCD_FONT), scroll_delay=0.08)
            #img = qrcode.make(str(item["link"]))
           # img.show()
    except ValueError:
        print("Bummer :( I couldn't make you 'dem links :(")
    finally:
        print("\nWill get more news next half hour!\n\n")

def run():
   # print("News Fetched at {}\n".format(time.ctime()))
    createLinks()
    threading.Timer(len(items) * 60, run).start()

if __name__ == '__main__':
      run()
