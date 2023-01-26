from flask import Flask, request, jsonify
import json
from flask_cors import cross_origin
from werkzeug.middleware.proxy_fix import ProxyFix
from pathlib import Path


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


@app.route("/save_client", methods=['POST'])
@cross_origin()
def save_client():
    FOLDER = Path(__file__).parent.resolve()
    client_file_path = FOLDER / "client_data.json"

    client_data = request.json
    with open(client_file_path, "w") as client_file:
        json.dump(client_data, client_file, indent=2)
    print(client_data)
    return jsonify(response={"success": "Successfully updated client info"})


if __name__ == "__main__":
    app.run(debug=True, port=5002)

