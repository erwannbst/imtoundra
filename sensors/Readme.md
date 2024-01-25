Microservice of the unit with the sensors. It is responsible for reading the sensors and sending the data to another microservice.

AHT21 and ENS160 are the drivers for the sensors. The first one is a temperature and humidity sensor and the second one is a gas sensor.

The data is sent to the microservice `imtoundra-network` through a socket.