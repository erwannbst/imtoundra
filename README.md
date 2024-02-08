# imtoundra

Several micro services to detect animals and send analytics to a database.

- Image recognition
- Encoding
- Network
- Database
- Analytics

## Image recognition

This microservice utilizes the YOLOv7-Tiny model to detect objects in an image and return the results in JSON format.

The `recognition_visual.py` file displays the image after detection and serves as a visual example for the microservice located in the `recognition_ms.py` file.

### Features

- The microservice exposes an `detect_objects` endpoint that accepts POST requests with images.
- It loads the pre-trained YOLOv7-Tiny model as well as classes from files.
- Detections are performed on the provided input image.
- Only detections with confidence above 0.5 are retained.
- Redundant detections are removed using Non-Maximum Suppression (NMS).
- The results are returned in JSON format containing detected classes and their confidences.

### Usage

1. Send a POST request with an image to the `/detect_objects` endpoint.
2. The microservice returns detected object detections in the image.

### Execution

- Run the Python script to launch the microservice.
- The microservice runs on `http://localhost:5000` by default.

## Encoding
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


## Database
Build the container
`docker build -t imtoundra-db .`

Run the database container
`docker run -d -p 5432:5432 imtoundra-db`

## Sensors
Two drivers that read values from two sensors (humidity and CO2 level)
