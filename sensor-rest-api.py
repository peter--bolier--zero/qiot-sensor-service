#!/usr/bin/env python3

"""
Simple application creating a REST-API to read Pimoroni enviro + Air quality
board and particular sensor.

Its a first rough approach, only for demo.

In this version we use Flask with it built in server to implement the
REST-API.


Note: the usage of the display on the enviro is only for easy checking while
testing.

"""

from enviroplus import gas
from bme280 import BME280
from pms5003 import PMS5003, ReadTimeoutError
import ST7735

from datetime import datetime
from flask import Flask
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import RobotoMedium as UserFont
import logging
from smbus import SMBus

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


# initilise bus for conenction to sensor
bus = SMBus(1)
# BME280 Weather data interface or temperature/pressure/humidity sensor
bme280 = BME280(i2c_dev=bus)
# PMS5003 particulate sensor
pms5003 = PMS5003()


gas.enable_adc()
gas.set_adc_gain(4.096)

# --------
# Retrieving gas
@rest_api_app.route('/gas')
def get_gas_measurements():

    now = datetime.utcnow()
    line1 = now.strftime("%H%M%S")
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

    return '{ "instant":"' + now.isoformat() + '"' + \
           ', "adc":' + str(gas_readings.adc) + \
           ', "nh3":' + str(gas_readings.nh3) + \
           ', "oxidised":' + str(gas_readings.oxidising) + \
           ', "reduced":' + str(gas_readings.reducing) + \
           '}'


# ---- retrieving pollution
@rest_api_app.route('/pollution')
def get_pollution_measurements():

    now = datetime.utcnow()
    line1 = now.strftime("%H%M%S")
    size_x, size_y = draw.textsize(line1, font)

    # text position
    x = 0
    y = 0

    # Draw background rectangle and write text.
    draw.rectangle((0, 0, 160, 80), back_colour)
    draw.text((x, y), line1, font=font, fill=text_colour)

    line2 = "pollution"
    size_x, size_y = draw.textsize(line2, font)
    y += size_y
    draw.text((x, y), line2, font=font, fill=text_colour)

    disp.display(img)

    # retrieve pollution readings
    values = {}
    pm_values = pms5003.read()
    try:
        pm_values = pms5003.read()
        # per m3
        values["PM1_0"] = str(pm_values.pm_ug_per_m3(1.0))
        values["PM2_5"] = str(pm_values.pm_ug_per_m3(2.5))
        values["PM10"] = str(pm_values.pm_ug_per_m3(10))
        values["PM1_0_atm"] = str(pm_values.pm_ug_per_m3(1.0, True))
        values["PM2_5_atm"] = str(pm_values.pm_ug_per_m3(2.5, True))
        values["PM10_atm"] = str(pm_values.pm_ug_per_m3(None, True))
        # per liter
        values["gt0_3um"] = str(pm_values.pm_per_1l_air(0.3))
        values["gt0_5um"] = str(pm_values.pm_per_1l_air(0.5))
        values["gt1_0um"] = str(pm_values.pm_per_1l_air(1.0))
        values["gt2_5um"] = str(pm_values.pm_per_1l_air(2.5))
        values["gt5_0um"] = str(pm_values.pm_per_1l_air(5))
        values["gt10um"] = str(pm_values.pm_per_1l_air(10))
    except ReadTimeoutError:
        pms5003.reset()
        pm_values = pms5003.read()
        # per m3
        values["PM1_0"] = str(pm_values.pm_ug_per_m3(1.0))
        values["PM2_5"] = str(pm_values.pm_ug_per_m3(2.5))
        values["PM10"] = str(pm_values.pm_ug_per_m3(10))
        values["PM1_0_atm"] = str(pm_values.pm_ug_per_m3(1.0, True))
        values["PM2_5_atm"] = str(pm_values.pm_ug_per_m3(2.5, True))
        values["PM10_atm"] = str(pm_values.pm_ug_per_m3(None, True))
        # per liter
        values["gt0_3um"] = str(pm_values.pm_per_1l_air(0.3))
        values["gt0_5um"] = str(pm_values.pm_per_1l_air(0.5))
        values["gt1_0um"] = str(pm_values.pm_per_1l_air(1.0))
        values["gt2_5um"] = str(pm_values.pm_per_1l_air(2.5))
        values["gt5_0um"] = str(pm_values.pm_per_1l_air(5))
        values["gt10um"] = str(pm_values.pm_per_1l_air(10))

    return '{ "instant":"' + now.isoformat() + '"' + \
           ', "PM1_0":' + values["PM1_0"] + \
           ', "PM2_5":' + values["PM2_5"] + \
           ', "PM10":' + values["PM10"] + \
           ', "PM1_0_atm":' + values["PM1_0_atm"] + \
           ', "PM2_5_atm":' + values["PM2_5_atm"] + \
           ', "PM10_atm":' + values["PM10_atm"] + \
           ', "gt0_3um":' + values["gt0_3um"] + \
           ', "gt0_5um":' + values["gt0_5um"] + \
           ', "gt1_0um":' + values["gt1_0um"] + \
           ', "gt2_5um":' + values["gt2_5um"] + \
           ', "gt5_0um":' + values["gt5_0um"] + \
           ', "gt10um":' + values["gt10um"] + \
           '}'


# ---- retrieving weatherdata
@rest_api_app.route('/weather')
def get_weather_measurements():
    now = datetime.utcnow()
    line1 = now.strftime("%H%M%S")
    size_x, size_y = draw.textsize(line1, font)

    # text position
    x = 0
    y = 0

    # Draw background rectangle and write text.
    draw.rectangle((0, 0, 160, 80), back_colour)
    draw.text((x, y), line1, font=font, fill=text_colour)

    line2 = "weather"
    size_x, size_y = draw.textsize(line2, font)
    y += size_y
    draw.text((x, y), line2, font=font, fill=text_colour)

    disp.display(img)

    # retrieve weather readings
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()

    return '{ "instant":"' + now.isoformat() + '"' + \
           ', "temperature":' + str(temperature) + \
           ', "pressure":' + str(pressure) + \
           ', "humidity":' + str(humidity) + \
           '}'

if __name__ == '__main__':
    rest_api_app.run(debug=False, host='0.0.0.0')
