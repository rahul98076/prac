import pytest
from app import app, inventory

@pytest.fixture
def client():
    # Reset inventory to a known state before each test
    inventory.clear()
    inventory.update({
        1: {"name": "web-server-01", "role": "frontend"},
        2: {"name": "db-server-01", "role": "database"}
    })
    
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {'status': 'healthy', 'service': 'demo-api'}

def test_get_servers(client):
    response = client.get('/servers')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2

def test_get_server_not_found(client):
    response = client.get('/servers/999')
    assert response.status_code == 404

def test_create_server(client):
    new_server = {"name": "app-server-01", "role": "application"}
    response = client.post('/servers', json=new_server)
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == new_server['name']
    assert data['role'] == new_server['role']
    assert 'id' in data

def test_create_server_missing_name(client):
    response = client.post('/servers', json={"role": "unknown"})
    assert response.status_code == 400

def test_update_server(client):
    update_data = {"name": "web-server-01-updated", "role": "frontend"}
    response = client.put('/servers/1', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == update_data['name']
    
def test_delete_server(client):
    response = client.delete('/servers/2')
    assert response.status_code == 200
    
    # Verify deletion
    get_response = client.get('/servers/2')
    assert get_response.status_code == 404