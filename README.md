![banniere](https://github.com/erwannbst/imtoundra/assets/16354899/58aae6c8-b9eb-4a58-ba8d-2208d1498d1e)
# IMToundra

This project is a collection of microservices that detect animals and send analytics to a database.
It is part of the IMToundra project, which aims to monitor the environment of the Toundra house.

Table of contents
=================

- [Flowchart](#flowchart)
    - [1. Animal detection](#1-animal-detection)
    - [2. Image recognition](#2-image-recognition)
    - [3. Sensor reading](#3-sensor-reading)
    - [4. Encoding](#4-encoding)
    - [5. Network](#5-network)
    - [6. Database](#6-database)
- [Hardware](#hardware)
    - [First unit](#first-unit)
    - [Second unit](#second-unit)
- [Software](#software)
  - [Image recognition](#image-recognition)
    - [Features](#features)
    - [Usage](#usage)
    - [Execution](#execution)
  - [Sensors](#sensors)
  - [Encoding](#encoding)
  - [Network (pySX127x)](#network)
  - [Database](#database)

## Flowchart

#### 1. Animal detection
***This step is not implemented in this project.***
The first unit detects an animal and takes a picture of it.

#### 2. Image recognition
The image is sent to the image recognition microservice, which detects the animals in the image.

#### 3. Sensor reading
Then the unit reads the sensors (humidity, temperature, and CO2 level) and sends the data to the encoding microservice.

#### 4. Encoding
The encoding microservice encodes the data to reduce the payload size and sends it to the network microservice.

#### 5. Network
The network microservice sends the data to the second unit using LoRa.

#### 6. Database
The second unit receives the data and sends it to the database microservice.


## Hardware

This is a list of the hardware used in the project:

#### First unit

This unit is located inside the Toundra house and is responsible for detecting animals and monitoring the environment.
It has no internet access and sends the data to the second unit using LoRa.

- Raspberry Pi 3B
- ENS160 humidity sensor + AHT21 temperature sensor
<img
  src="https://github.com/erwannbst/imtoundra/assets/16354899/07a51419-0ccc-47a3-a6e7-425202ede7c4"
  alt="ENS160"
  title="ENS160"
  style="display: inline-block; width: 250px"
  />

- LED for visual feedback
- Ra-02 LoRa module (SX1278)
<img
  src="https://github.com/erwannbst/imtoundra/assets/16354899/89a290d7-6e87-47ea-ad91-12d788398494"
  alt="SX1278"
  title="SX1278"
  style="display: inline-block; width: 250px"
  />


#### Second unit

This second unit is located outside the Toundra house and is responsible for sending the data to the cloud.
It has internet access and sends the data to the cloud using Wi-Fi.

- Raspberry Pi Zero W
- Ra-02 LoRa module (SX1278)

![schematic](https://github.com/erwannbst/imtoundra/assets/16354899/12b72760-f707-435e-a4b3-8423cff42c1e)

## Software

Several micro services to detect animals and send analytics to a database.

- Image recognition
- Encoding
- Network
- Database
- Analytics

### Image recognition

This microservice utilizes the YOLOv7-Tiny model to detect objects in an image and return the results in JSON format.

The `recognition_visual.py` file displays the image after detection and serves as a visual example for the microservice located in the `recognition_ms.py` file.

#### Features

- The microservice exposes an `detect_objects` endpoint that accepts POST requests with images.
- It loads the pre-trained YOLOv7-Tiny model as well as classes from files.
- Detections are performed on the provided input image.
- Only detections with confidence above 0.5 are retained.
- Redundant detections are removed using Non-Maximum Suppression (NMS).
- The results are returned in JSON format containing detected classes and their confidences.

##### Usage

1. Send a POST request with an image to the `/detect_objects` endpoint.
2. The microservice returns detected object detections in the image.

##### Execution

- Run the Python script to launch the microservice.
- The microservice runs on `http://localhost:5000` by default.

### Sensors

Microservice of the fist unit with the sensors. It is responsible for reading the sensors and sending the data to the encoding microservice.

### Encoding
Its job is to minimize the weight of the payload
it removes the keys from the json and encodes the values to bytes with `msgpack`.
```
curl -X POST -H "Content-Type: application/json"
-d '{"animal_identifie": "cat", "timestamp": 1641992400, "temperature": 25, "co2": 400}'
http://localhost:5000/encode
```

returns
`{
  "encoded_bytes": "94a3636174ce61ded0d019cd0190"
}`

### Network (pySX127x)
This microservice is responsible for sending the data to the second unit using LoRa.


### Database
Build the container
`docker build -t imtoundra-db .`

Run the database container
`docker run -d -p 5432:5432 imtoundra-db`
