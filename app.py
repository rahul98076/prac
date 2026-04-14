from flask import Flask, jsonify,request,abort

app = Flask(__name__)

inventory = {
    1: {"name": "web-server-01", "role": "frontend"},
    2: {"name": "db-server-01", "role": "database"}
}

#read
@app.route('/servers', methods=['GET'])
def get_servers():
    return jsonify(list(inventory.values())), 200

@app.route('/servers/<int:server_id>', methods=['GET'])
def get_server(server_id):
    server = inventory.get(server_id)
    if not server:
        abort(404,description="Server not found")
    return jsonify(server), 200

#create
@app.route('/servers', methods=['POST'])
def create_server():
    data = request.get_json()
    if not request.json or 'name' not in request.json:
        abort(400,description="Missing required field: name")

    new_id = max(inventory.keys()) + 1
    new_server = {
        "name": request.json['name'],
        "role": request.json.get('role', 'unknown')
    }
    inventory[new_id] = new_server
    return jsonify({"id": new_id, **new_server}), 201

#update
@app.route('/servers/<int:server_id>', methods=['PUT'])
def update_server(server_id):
    if server_id not in inventory:
        abort(404,description="Server not found")

    inventory[server_id]['name'] = request.json.get('name', inventory[server_id]['name'])
    inventory[server_id]['role'] = request.json.get('role', inventory[server_id]['role'])
    return jsonify(inventory[server_id]), 200

#delete
@app.route('/servers/<int:server_id>', methods=['DELETE'])
def delete_server(server_id):
    if server_id in inventory:
        del inventory[server_id]
        return jsonify({'message': 'Server deleted'}), 200
    else:
        abort(404,description="Server not found")


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy','service': 'demo-api'}), 200 

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to the Demo API!'}), 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)