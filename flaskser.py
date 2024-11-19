from flask import Flask, jsonify
from flask_cors import CORS 
import json
import os

app = Flask(__name__)
CORS(app)

# Path to the extracted data file
EXTRACTED_FILE = "extracted.json"

@app.route('/api/transcribe', methods=['GET'])
def get_transcription_data():
    # Check if the extracted file exists
    if not os.path.exists(EXTRACTED_FILE):
        return jsonify({"error": "No extracted data available"}), 404

    # Read the extracted data
    with open(EXTRACTED_FILE, "r") as f:
        extracted_data = json.load(f)

    return jsonify(extracted_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
