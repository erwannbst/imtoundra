## Encoding microservice

Its job is to minimize the weight of the payload. It removes the keys from the JSON and encodes the values to bytes with `msgpack`.

### Execution

- Run the Python script to launch the microservice.
- The microservice runs on `http://localhost:5000` by default.
- The microservice exposes two endpoints: `/encode` and `/decode`.
- The `/encode` endpoint accepts POST requests with JSON data and returns the encoded bytes.
- The `/decode` endpoint accepts POST requests with JSON data containing the encoded bytes and returns the decoded values.
- The microservice uses `msgpack` to encode and decode the values.


### Usage

```bash
python3 encoding.py
```

Then, to encode:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"animal_identifie": "cat", "timestamp": 1641992400, "temperature": 25, "co2": 400}' http://127.0.0.1:5000/encode
```

Output:

```json
{
  "encoded_bytes": "94a3636174ce61ded0d019cd0190"
}
```

To decode:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"encoded_bytes": "94a3636174ce61ded0d019cd0190"}' http://127.0.0.1:5000/decode
```

Output:

```json
{
  "animal_identifier": "cat",
  "timestamp": 1641992400,
  "temperature": 25,
  "co2": 400
}
```

As you can see it reduces the size of the payload by removing the keys and encoding the values to bytes.

#### Bandwidth comparison

The original JSON data:

```json
{
  "animal_identifier": "cat",
  "timestamp": 1641992400,
  "temperature": 25,
  "co2": 400
}
```

The encoded bytes:

```json
"94a3636174ce61ded0d019cd0190"
```

The encoded bytes are 28 characters long, while the original JSON data is 83 characters long. This is a reduction of 66.27% in size.