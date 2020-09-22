# qiot-sensor-service
Sensor service: retrieving environemental data and exposing this via rest api.

For now it's a very basic application, just using flask.

We did consider to use a local MQTT broker to which the raw measurement data would be published, enabling further processing, like calculating averages over 1 or 10 minues (which is a common interval for environmental data). 

We also considere using FastAPI and documenting the API using Swagger, but installing additonal packages, ie. uvicorn failed (dependecy on gcc <todo: check details>) and it took more space than we liked anyway.  

Testrun sensor service
.. 
prequisites
- flask...
cd were app is installed

export FLASK_APP=sensor-rest-api.py
run flask

on some host

curl http://127.0.0.1:5000/pollution
2020-09-22 13:54:46.816 INFO     127.0.0.1 - - [22/Sep/2020 13:54:46] "GET /pollution HTTP/1.1" 200 -
{ "instant":2020-09-22T13:54:46.775000, "PM1_0":7, "PM2_5":11, "PM10":19, "PM1_0_atm":7, “PM2_5_atm":11, "PM10_atm":19, "gt0_3um":0, "gt0_5um":0, "gt1_0um":0, "gt2_5um":0, "gt5_0um":0, "gt10um":0}

curl http://127.0.0.1:5000/gas
2020-09-22 13:55:43.833 INFO     127.0.0.1 - - [22/Sep/2020 13:55:43] "GET /gas HTTP/1.1" 200 -
{ "instant":2020-09-22T13:55:43.715350, "adc":0.636, "nh3":121011.49425287354, "oxidised":50574.39446366783, "reduced":1128615.3846153868}


curl http://127.0.0.1:5000/weather
2020-09-22 13:57:33.690 INFO     127.0.0.1 - - [22/Sep/2020 13:57:33] "GET /weather HTTP/1.1" 200 -
{ "instant":2020-09-22T13:57:33.529210, "temperature":24.18012930811965, "pressure":652.033925549806, "humidity":89.0146080309965}
