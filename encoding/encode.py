import msgpack
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


def encode_values_to_bytes(data):
    try:
        values = list(data.values())
        packed_data = msgpack.packb(values)
        return packed_data
    except Exception as e:
        print(f"Error encoding data values: {e}")
        return None


def decode_bytes_to_values(encoded_bytes):
    # The structure of the JSON data is:
    # {
    #     "animal_identifie": first_value,
    #     "timestamp": second_value,
    #     "temperature": third_value,
    #     "co2": fourth_value
    # }
    # The output only contains the values of the dictionary in the same order as the input JSON data
    try:
        decoded_values = msgpack.unpackb(bytes.fromhex(encoded_bytes))
        json_data = {
            "animal_identifier": decoded_values[0],
            "timestamp": decoded_values[1],
            "temperature": decoded_values[2],
            "co2": decoded_values[3],
        }
        return json_data

    except Exception as e:
        print(f"Error decoding data values: {e}")
        return None


@app.route("/encode", methods=["POST"])
def encode_endpoint():
    try:
        json_data = request.get_json()
        print(f"Encode service: received: {json_data}")
        encoded_values_bytes = encode_values_to_bytes(json_data)

        if encoded_values_bytes:
            hex = encoded_values_bytes.hex()
            # Call the network service on port 5003
            data = {"encoded_bytes": hex}
            print(f"Encode service: Sending data to network service: {data}")
            response = requests.post("http://localhost:5003/send", json=data)

        else:
            return jsonify({"error": "Failed to encode values"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/decode", methods=["POST"])
def decode_endpoint():
    try:
        json_data = request.get_json()
        encoded_bytes = json_data.get("encoded_bytes")
        if not encoded_bytes:
            return jsonify({"error": "No encoded bytes provided"}), 400

        decoded_values = decode_bytes_to_values(encoded_bytes)
        if decoded_values:
            return jsonify(decoded_values)
        else:
            return jsonify({"error": "Failed to decode values"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5002)
