#!/usr/bin/env python3

import ST7735
from datetime import datetime
from enviroplus import gas
from flask import Flask
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import RobotoMedium as UserFont
import logging

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("sensor-service-api")

rest_api_app = Flask(__name__)

# Create LCD class instance.
disp = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)

# Initialize display.
disp.begin()

# Width and height to calculate text position.
WIDTH = disp.width
HEIGHT = disp.height

# New canvas to draw on.
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

# Text settings.
font_size = 25
font = ImageFont.truetype(UserFont, font_size)
text_colour = (255, 255, 255)
back_colour = (0, 170, 170)

# TODO use helper functions

# initial text
line1 = datetime.now().strftime("%H%M%S")
size_x, size_y = draw.textsize(line1, font)

# text position
x = 0
y = 0

# Draw background rectangle and write text.
draw.rectangle((0, 0, 160, 80), back_colour)
draw.text((x, y), line1, font=font, fill=text_colour)

line2 = "ready"
size_x, size_y = draw.textsize(line2, font)
y += size_y
draw.text((x, y), line2, font=font, fill=text_colour)

disp.display(img)


#--------
# Retrieving gas

# dont forget to enable adc

gas.enable_adc()
gas.set_adc_gain(4.096)



@rest_api_app.route('/gas')
def get_gas_measurements():

    line1 = datetime.now().strftime("%H%M%S")
    size_x, size_y = draw.textsize(line1, font)

    # text position
    x = 0 
    y = 0 

    # Draw background rectangle and write text.
    draw.rectangle((0, 0, 160, 80), back_colour)
    draw.text((x, y), line1, font=font, fill=text_colour)

    line2 = "gas"
    size_x, size_y = draw.textsize(line2, font)
    y += size_y
    draw.text((x, y), line2, font=font, fill=text_colour)

    disp.display(img)

    # retrieve gas readings
    gas_readings = gas.read_all()
    
    return '{ "oxidised":' + str(gas_readings.oxidising) + \
           ', "reduced":'  + str(gas_readings.reducing)  + \
           ', "nh3":' + str(gas_readings.nh3) + \
           ', "adc":' + str(gas_readings.adc) + ' }'
 

# ---- retrieving pollution

