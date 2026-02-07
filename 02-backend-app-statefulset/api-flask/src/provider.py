import logging
from http import HTTPStatus

from flask import Flask, jsonify, request

app = Flask(__name__)

app.logger.setLevel(logging.INFO)

PROVIDERS = [
    {"id": 1, "name": "Sanite Belair", "specialty": "Pediatry"},
    {"id": 2, "name": "Catherine Flon", "specialty": "Surgery"},
    {"id": 3, "name": "Toussaint Louverture", "specialty": "Podology"},
]


@app.route("/healthz", methods=["GET"])
def healthz():
    """Liveness probe: Check if the process is responding."""
    return jsonify({"status": "healthy"}), 200

@app.route("/readyz")
def readyz():
    """Readiness probe: Check if dependencies (DB, Cache) are available."""
    # Logic here: e.g., try a simple DB query
    # if database_is_down:
    #     return jsonify({"status": "unavailable"}), 503
    return jsonify({"status": "ready"}), 200

@app.route("/", methods=["GET"])
def home():
    """Home page"""
    app.logger.info("Getting the homepage")
    return "Welcome to the appointment service"


@app.route("/providers", methods=["GET"])
def get_providers():
    """Get the list of providers"""
    app.logger.info("Guetting the list of providers")
    return jsonify(PROVIDERS), HTTPStatus.OK


@app.route("/providers", methods=["POST"])
def create_provider():
    """Create a provider"""
    new_provider = request.get_json()

    app.logger.info("Received request to create new provider")

    if not new_provider or "id" not in new_provider:
        app.logger.warning("Failed creation: Missing provider ID in payload")
        return jsonify(
            {"error": "Bad Request: 'id' is required"}
        ), HTTPStatus.BAD_REQUEST

    for provider in PROVIDERS:
        if provider["id"] == new_provider["id"]:
            app.logger.warning(
                f"Creation blocked: Provider ID {new_provider['id']} already exists"
            )
            return jsonify({"message": "Already exists"}), HTTPStatus.CONFLICT

    PROVIDERS.append(new_provider)

    app.logger.info(
        f"Provider {new_provider['id']} ('{new_provider['name']}') created successfully"
    )

    return jsonify(new_provider), HTTPStatus.CREATED


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
