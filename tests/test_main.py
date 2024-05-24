import pytest
from main import flaskapp as app
from db import db as main_db

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            main_db.create_all()
            yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_tasks_route(client):
    response = client.get('/tasks')
    assert response.status_code == 302
