from flask import Flask, request, jsonify
import subprocess
import os
import requests
from urllib.parse import urljoin
import logging
from rag import run_workflow
from flask_socketio import SocketIO, emit
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

SVELTE_SERVER_URL = "http://localhost:5173"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


def emit_rag_response(data):
    socketio.emit("rag_response", data)


@app.route("/api/rag", methods=["POST"])
def process_rag():
    try:
        data = request.json
        query = data.get("query")
        nodes = data.get("nodes")
    
        if not query:
            return jsonify({"error": "Query is required"}), 400

        if not nodes:
            nodes = json.load(open("client/src/lib/config/nodes.json"))
        
        print(nodes)

        result = run_workflow(query, nodes)
        emit_rag_response({"success": True, "result": result})

        return jsonify({"success": True, "message": "Processing started"})

    except Exception as e:
        logging.error(f"Error processing RAG query: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


def start_node_server():
    client_dir = os.path.join(os.path.dirname(__file__), "client")

    # Check if Svelte server is already running on port 5173
    try:
        response = requests.get(SVELTE_SERVER_URL)
        if response.status_code == 200:
            logger.info("Svelte server is already running, skipping initialization")
            return
    except requests.exceptions.ConnectionError:
        pass

    node_process = subprocess.Popen(
        "npm run dev",
        shell=True,
        cwd=client_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    while True:
        line = node_process.stdout.readline().decode()
        if "Local:" in line:
            local_address = line.split("Local:")[1].strip()
            logger.info(f"🚀 Svelte server running at: {local_address}")
            break
        elif "Network:" in line:
            network_address = line.split("Network:")[1].strip()
            logger.info(f"🌐 Network access available at: {network_address}")

    return node_process


# test
# def initialize():
#     global node_process
#     #

   

#     # Kill any existing node process before starting a new one
#     if hasattr(globals(), "node_process"):
#         try:
#             node_process.terminate()
#             node_process.wait()
#         except:
#             pass

#     node_process = start_node_server()


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def proxy(path):
    if path.startswith("api/"):
        return handle_api_request(path)

    url = urljoin(SVELTE_SERVER_URL, path)

    resp = requests.request(
        method=request.method,
        url=url,
        headers={key: value for key, value in request.headers if key != "Host"},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
    )

    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    ]
    headers = [
        (name, value)
        for name, value in resp.raw.headers.items()
        if name.lower() not in excluded_headers
    ]

    response = app.response_class(
        response=resp.content, status=resp.status_code, headers=headers
    )

    return response


def handle_api_request(path):
    if path == "api/rag":
        return process_rag()

    return {"error": "API endpoint not found"}, 404


if __name__ == "__main__":
    start_node_server()
    socketio.run(app, debug=True, port=5000)
