from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

# Chemin vers le fichier yolov7-tiny.weights
weights_path = "./yolov7-tiny.weights"

# Charge le modèle YOLO
net = cv2.dnn.readNetFromDarknet("./yolov7-tiny.cfg", weights_path)

# Charge les classes
classes = []
with open("./classes.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

@app.route('/detect_objects', methods=['POST'])
def detect_objects():
    # Vérifie si une image est incluse dans la requête
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})

    # Charge l'image
    image = request.files['image'].read()
    image = np.frombuffer(image, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # Crée un blob à partir de l'image
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)

    # Passerle blob dans le réseau
    net.setInput(blob)

    # Obtiens les noms des couches de sortie
    output_layers = net.getUnconnectedOutLayersNames()

    # Effectue la détection d'objets
    outs = net.forward(output_layers)

    detections = []

    # Initialise des listes pour les boîtes englobantes, les confiances et les classes détectées
    boxes = []
    confidences = []
    class_ids = []

    # Parcours les détections
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            # Filtre les détections par confiance
            if confidence > 0.5:
                # Récupére les coordonnées de la boîte englobante
                center_x = int(detection[0] * image.shape[1])
                center_y = int(detection[1] * image.shape[0])
                w = int(detection[2] * image.shape[1])
                h = int(detection[3] * image.shape[0])

                # Coordonnées de la boîte englobante
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Ajoute les coordonnées, la confiance et l'ID de classe à leurs listes respectives
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Supprime les détections redondantes en utilisant la suppression non maximale (NMS)
    indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)

    # Ajoute les détections restantes à la liste des détections
    if len(indices) > 0:
        for i in indices.flatten():
            detections.append({
                'class': classes[class_ids[i]],
                'confidence': confidences[i]
            })

    return jsonify({'detections': detections})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
