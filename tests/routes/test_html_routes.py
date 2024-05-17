import pytest
from unittest.mock import MagicMock
from main import flaskapp as app
from db import db as main_db


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            main_db.create_all()
            yield client
            main_db.session.remove()
            main_db.drop_all()


@pytest.fixture
def mocked_db():
    # Mocking the database session
    db = MagicMock()
    db.create_all = MagicMock(return_value=None)
    db.session = MagicMock()
    db.session.add = MagicMock()
    db.session.commit = MagicMock()
    db.session.remove = MagicMock()
    db.drop_all = MagicMock()
    return db


def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"ACIT-2911 Agile Project" in response.data


def test_tasks_route(client):
    response = client.get('/tasks')
    assert response.status_code == 200


def test_create_tasks_route(client, mocked_db):
    response = client.post('/tasks/create', data={'title': 'New Task', 'description': 'Description'})
    assert response.status_code == 302  # Redirects after task creation, adjust as needed
