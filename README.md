# qiot-sensor-service
Sensor service: retrieving environemental data and exposing this via rest api.

For now it's a very basic application, just using flask.

We did consider to use a local MQTT broker to which the raw measurement data would be published, enabling further processing, like calculating averages over 1 or 10 minues (which is a common interval for environmental data). 

We also considere using FastAPI and documenting the API using Swagger, but installing additonal packages, ie. uvicorn failed (dependecy on gcc <todo: check details>) and it took more space than we liked anyway.  
