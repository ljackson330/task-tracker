import pytest
from unittest.mock import MagicMock
from main import flaskapp as app
from db import db as main_db
from flask_login import current_user


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            with app.test_request_context():
                main_db.create_all()
            yield client

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

@pytest.fixture
def mock_authenticated_user(monkeypatch):
    # Define a mock user with an 'is_authenticated' attribute
    class MockUser:
        @property
        def is_authenticated(self):
            return True

    # Mock current_user to return the mock user
    monkeypatch.setattr(current_user, 'is_authenticated', MockUser().is_authenticated)
    monkeypatch.setattr(current_user, 'id', 1)


def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200


def test_tasks_route(client):
    response = client.get('/tasks')
    assert response.status_code == 302