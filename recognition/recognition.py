import cv2
import numpy as np
import requests
from flask import Flask, jsonify

app = Flask(__name__)


def recognition():
    # Chemin vers le fichier yolov7-tiny.weights
    weights_path = "./yolov7-tiny.weights"

    # Charger le modèle
    net = cv2.dnn.readNetFromDarknet("./yolov7-tiny.cfg", weights_path)

    # Charger l'image
    image = cv2.imread("../ours.png")

    # Charger les classes
    classes = []
    with open("./classes.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    # Créer un blob à partir de l'image
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)

    # Passer le blob dans le réseau
    net.setInput(blob)

    # Obtenir les noms des couches de sortie
    # layer_names = net.getLayerNames()
    # print("Layer names:", layer_names)

    # Obtenir les indices des couches de sortie non connectées
    output_layers = net.getUnconnectedOutLayersNames()

    # Convertir les indices en noms de couches
    # output_layers = ['yolo_90','yolo_94','yolo_98']

    # effectuer la détection d'objets
    outs = net.forward(output_layers)

    # Initialiser des listes pour les boîtes englobantes, les confiances et les classes détectées
    boxes = []
    confidences = []
    class_ids = []

    # Parcourir les détections
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            # Filtrer les détections par confiance
            if confidence > 0.5:
                # Récupérer les coordonnées de la boîte englobante
                center_x = int(detection[0] * image.shape[1])
                center_y = int(detection[1] * image.shape[0])
                w = int(detection[2] * image.shape[1])
                h = int(detection[3] * image.shape[0])

                # Coordonnées de la boîte englobante
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Ajouter les coordonnées, la confiance et l'ID de classe à leurs listes respectives
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Supprimer les détections redondantes en utilisant la suppression non maximale (NMS)
    indices = cv2.dnn.NMSBoxes(
        boxes, confidences, score_threshold=0.5, nms_threshold=0.4
    )

    # Vérifier s'il y a des détections après NMS
    if len(indices) > 0:
        for i in indices.flatten():
            # Récupérer les coordonnées de la boîte englobante, la confiance et l'ID de classe
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]

            # Dessiner la boîte englobante et afficher l'étiquette et la confiance
            color = (0, 0, 255)  # Couleur Rouge (BGR)
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = f"{label}: {confidence:.2f}"
            # mettre le texte dans la boîte englobante en bas à gauche
            cv2.putText(
                image, text, (x + 2, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
            )
    return image


@app.route("/recognition", methods=["POST"])
def recognition_endpoint():
    try:
        print(f"Recognition service: Recognition starts")
        # exécuter la fonction de reconnaissance
        image = recognition()

        # requête au service sensors sur le port 5001
        data = {"animal_identifie": image}
        print(f"Recognition service: calling sensors")
        response = requests.post("http://localhost:5001/sensors", json=data)
        return response.json()

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
