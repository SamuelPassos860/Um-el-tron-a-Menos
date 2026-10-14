from flask import Flask, jsonify, request, abort
from pathlib import Path
import json
import os

app = Flask(__name__)
APP_DIR = Path(__file__).resolve().parent
DATA_FILE = APP_DIR / "dados_tabela.json"

API_TOKEN = os.getenv("BACKEND_TOKEN")


def check_auth():
    if API_TOKEN:
        token = request.headers.get("X-API-TOKEN") or request.headers.get("Authorization")
        if not token:
            return False
        if token.startswith("Bearer "):
            token = token[len("Bearer "):]
        return token == API_TOKEN
    return True


@app.route("/data", methods=["GET"])
def get_data():
    if not check_auth():
        abort(401)

    if not DATA_FILE.exists():
        return jsonify({"elementos_falados": [], "videos": {}})

    try:
        content = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        return jsonify(content)
    except Exception:
        return jsonify({"elementos_falados": [], "videos": {}})


@app.route("/data", methods=["POST"])
def post_data():
    if not check_auth():
        abort(401)

    if not request.is_json:
        abort(400)

    data = request.get_json()
    try:
        temp = DATA_FILE.with_suffix('.tmp')
        temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        temp.replace(DATA_FILE)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
