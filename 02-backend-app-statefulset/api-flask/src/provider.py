from flask import Flask, jsonify, request
from http import HTTPStatus

app = Flask(__name__)

PROVIDERS = [
    {"id": 1, "name": "Sanite Belair", "specialty": "Pediatry"},
    {"id": 2, "name": "Catherine Flon", "specialty": "Surgery"},
    {"id": 3, "name": "Toussaint Louverture", "specialty": "Podology"},
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

    new_provider = request.get_json()
    app.logger.info(f"new provider: {new_provider}")

    for provider in PROVIDERS:
        if provider["id"] == new_provider["id"]:
            return jsonify(
                {"message": f"Provider {new_provider['id']} already exists"}), HTTPStatus.CONFLICT
    
    PROVIDERS.append(new_provider)

    return jsonify(new_provider), HTTPStatus.CREATED


if __name__ == "__main__":
    app.run(debug=True)