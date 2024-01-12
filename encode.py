import msgpack
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


@app.route("/encode", methods=["POST"])
def encode_endpoint():
    try:
        json_data = request.get_json()
        encoded_values_bytes = encode_values_to_bytes(json_data)

        if encoded_values_bytes:
            return jsonify({"encoded_bytes": encoded_values_bytes.hex()})
        else:
            return jsonify({"error": "Failed to encode values"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
