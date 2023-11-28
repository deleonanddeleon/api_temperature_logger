import pytest
from api_isp_outage_logger import app, mongo

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_db'  # Use a different test database
    with app.test_client() as client:
        with app.app_context():
            mongo.init_app(app)
        yield client

def test_index_route(client):
    response = client.get('/outages')
    assert response.status_code == 200
    assert b'ISP Outage Logger' in response.data

def test_manage_records_get(client):
    response = client.get('/outages/records')
    assert response.status_code == 200
    assert response.is_json

def test_manage_records_post(client):
    data = {'id': 4}
    response = client.post('/outages/records', json=data)
    assert response.status_code == 200
    assert response.is_json
    assert 'message' in response.get_json()

def test_manage_record_get(client):
    response = client.get('/outages/records/1')
    assert response.status_code == 404
    assert response.is_json
    assert 'error' in response.get_json()

def test_manage_record_put(client):
    data = {'id': 5, 'stamp': 'test'}
    response = client.put('/outages/records/1', json=data)
    assert response.status_code == 404
    assert response.is_json
    assert 'error' in response.get_json()

def test_manage_record_delete(client):
    response = client.delete('/outages/records/1')
    assert response.status_code == 404
    assert response.is_json
    assert 'error' in response.get_json()

