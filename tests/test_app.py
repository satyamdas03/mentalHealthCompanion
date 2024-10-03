# tests/test_app.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_user(client):
    response = client.post('/api/user', json={'username': 'testuser'})
    assert response.status_code == 200
    assert 'user_id' in response.get_json()

def test_get_user(client):
    response = client.post('/api/user', json={'username': 'testuser'})
    user_id = response.get_json()['user_id']
    response = client.get(f'/api/user/{user_id}')
    assert response.status_code == 200
    assert response.get_json()['username'] == 'testuser'

def test_mood_analysis(client):
    response = client.post('/api/user', json={'username': 'testuser'})
    user_id = response.get_json()['user_id']
    response = client.post(f'/api/mood/{user_id}', json={'message': 'I am feeling great!'})
    assert response.status_code == 200
    assert 'sentiment' in response.get_json()

def test_exercises(client):
    response = client.post('/api/user', json={'username': 'testuser'})
    user_id = response.get_json()['user_id']
    response = client.get(f'/api/exercises/{user_id}')
    assert response.status_code == 200
    assert 'exercises' in response.get_json()
