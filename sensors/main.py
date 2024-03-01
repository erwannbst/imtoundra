#!/usr/bin/env python
import time

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

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


def measure():
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
    return aht.temperature, aht.humidity, ens.CO2


@app.route("/sensors", methods=["POST"])
def sensors_endpoint():
    try:
        print(f"Sensors service: a request was received, measuring...")
        temperature, humidity, co2 = measure()

        # Get animal identifier in the post request
        animal_identifie = request.json.get("animal_identifie")

        # Call the encoding service on port 5002
        data = {
            "animal_identifie": animal_identifie,
            "temperature": temperature,
            "humidity": humidity,
            "co2": co2,
        }

        print(f"Sensors service: Sending data to encoding service: {data}")

        response = requests.post("http://localhost:5002/encode", json=data)
        return response.json()

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5001)
