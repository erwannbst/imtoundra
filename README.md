# imtoundra

Several micro services to detect animals and send analytics to a database.

- Image recognitation
- Encoding
- Network
- Database
- Analytics

## Image recognition

## Encoding
Removes the keys from the json and encodes the values to bytes with `msgpack`.
```
curl -X POST -H "Content-Type: application/json"
-d '{"animal_identifie": "cat", "timestamp": 1641992400, "temperature": 25, "co2": 400}'
http://localhost:5000/encode
```

returns
`{
  "encoded_bytes": "94a3636174ce61ded0d019cd0190"
}`