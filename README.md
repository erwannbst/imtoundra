# imtoundra

Several micro services to detect animals and send analytics to a database.

- Image recognition
- Encoding
- Network
- Database
- Analytics

## Image recognition

Ce microservice utilise le modèle YOLOv7-Tiny pour détecter des objets dans une image et renvoyer les résultats sous forme de JSON.

Le fichier `recognition_visual.py` renvoie l'image après détection et sers d'exemple visuel pour le microservice situé dans le fichier `recognition_ms.py`

## Fonctionnalités

- Le microservice expose un endpoint `detect_objects` qui accepte les requêtes POST avec des images.
- Il charge le modèle YOLOv7-Tiny pré-entraîné ainsi que les classes à partir de fichiers.
- Les détections sont effectuées sur l'image fournie en entrée.
- Seules les détections avec une confiance supérieure à 0.5 sont conservées.
- Les détections redondantes sont supprimées en utilisant la suppression non maximale (NMS).
- Les résultats sont renvoyés sous forme de JSON contenant les classes détectées et leurs confiances.

## Utilisation

1. Envoyez une requête POST avec une image à l'endpoint `/detect_objects`.
2. Le microservice renvoie les détections d'objets détectées dans l'image.

## Exécution

- Exécutez le script Python pour lancer le microservice.
- Le microservice tourne sur `http://localhost:5000` par défaut.



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
