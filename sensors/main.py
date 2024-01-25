#!/usr/bin/env python
import time

import AHT21
import board

import ENS160

# set up
# i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))
i2c = board.I2C()
print(f"I2C: {i2c}")
ens = ENS160.ENS160(1)
ens.reset()
time.sleep(0.5)
ens.operating_mode = 2
time.sleep(2.0)

print("Starting AHT21...")
aht = AHT21.AHT21(1)
# ens = ENS160.ENS160(i2c)
# ens.reset()
# time.sleep(0.5)
# ens.operating_mode = 2
# time.sleep(2.0)

while True:
    print("Measuring temperature and humidity...")
    while not aht.is_ready:
        time.sleep(0.01)

    print(f"Temperature: {aht.temperature} °C, Humidity: {aht.humidity} %")
    aht_is_ready = False

    if ens.AQI == 0:
        ens.reset()
    print("Air quality (1-5):", ens.AQI)
    print("TVOC (ppb):", ens.TVOC)
    print("eCO2 (ppm):", ens.CO2)

    time.sleep(1.0)
