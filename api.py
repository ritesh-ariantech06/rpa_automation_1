from flask import Flask, request, jsonify
import os
import json
from datetime import datetime
from uuid import uuid4
from threading import Lock

app = Flask(__name__)


FOLDER_MAP = {
    "leadcreate": "templeadcreate",
    "leadupdate": "templeadupdate",
    "taskcreate": "temptaskcreate",
    "taskupdate": "temptaskupdate",
    "eventcreate": "tempeventcreate",
    "eventupdate": "tempeventupdate",
    "assign": "tempassign",
    "opp": "tempopp"
}


for folder in FOLDER_MAP.values():
    os.makedirs(folder, exist_ok=True)

file_write_lock = Lock()

@app.route('/runrpa', methods=['POST'])
def trigger_rpa():
    try:
        data = request.get_json()
        rpa_name = data.get("rpa_name", "")

        if rpa_name not in FOLDER_MAP:
            return jsonify({"error": f"Unknown rpa_name: {rpa_name}"}), 400

        target_folder = FOLDER_MAP[rpa_name]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        unique_id = str(uuid4())[:8]
        filename = f"{rpa_name}_{timestamp}_{unique_id}.json"
        filepath = os.path.join(target_folder, filename)

        with file_write_lock:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)

        print(f"📥 Saved to {filepath}")
        return jsonify({
            "message": "Data queued",
            "file": filename,
            "folder": target_folder,
            "status": "success"
        }), 200

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    pending_summary = {
        folder: len([
            f for f in os.listdir(folder)
            if f.endswith('.json')
        ])
        for folder in FOLDER_MAP.values()
    }
    return jsonify({
        "status": "running",
        "pending_by_folder": pending_summary
    }), 200

if __name__ == '__main__':
    print("🚀 Flask API running on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
