from app import app
def test_health_endpoint():
    with app.test_client() as client:
        response = client.get('/health')
        assert response.status_code == 200
        assert response.get_json() == {'status': 'healthy', 'service': 'demo-api'}

def test_get_servers():
    with app.test_client() as client:
        response = client.get('/servers')
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)

def test_create_server():
    with app.test_client() as client:
        new_server = {"name": "app-server-01", "role": "application"}
        response = client.post('/servers', json=new_server)
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == new_server['name']
        assert data['role'] == new_server['role']
        assert 'id' in data

def test_update_server():
    with app.test_client() as client:
        update_data = {"name": "web-server-01-updated", "role": "frontend"}
        response = client.put('/servers/1', json=update_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == update_data['name']
        assert data['role'] == update_data['role']
        
def test_delete_server():
    with app.test_client() as client:
        response = client.delete('/servers/2')
        assert response.status_code == 200
        assert response.get_json() == {'message': 'Server deleted'}
        # Verify deletion
        get_response = client.get('/servers/2')
        assert get_response.status_code == 404