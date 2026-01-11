from flask import Flask, jsonify
from http import HTTPStatus

app = Flask(__name__)

PROVIDERS = [
    {"id": 1, "name": "Sanite Belair", "speciality": "Pediatry"},
    {"id": 2, "name": "Catherine Flon", "speciality": "Surgery"},
    {"id": 3, "name": "Toussaint Louverture", "speciality": "Podology"},
]

@app.route("/providers", methods=["GET"])
def get_providers():
    """Get the list of providers"""
    app.logger.info("Guetting the list of providers")
    return jsonify(PROVIDERS), HTTPStatus.OK

@app.route("/providers", methods=["POST"])
def create_provider():
    """Create a provider"""
    app.logger.info("Creating a provider")
    return jsonify(PROVIDERS), HTTPStatus.CREATED


if __name__ == "__main__":
    app.run(debug=True)