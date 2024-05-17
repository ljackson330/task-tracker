import pytest

# Import the Flask app instance
from main import flaskapp


# Fixture for the Flask app
@pytest.fixture
def app():
    yield flaskapp


# Fixture for the test client
@pytest.fixture
def client(app):
    return app.test_client()


def test_config(app):
    """
    Test the Flask app configuration.
    """
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///taskdatabase.db"
    assert app.instance_path.is_dir()


def test_blueprint_registration(app):
    """
    Test if the blueprint is registered correctly.
    """
    registered_blueprints = app.blueprints
    assert "html_routes" in registered_blueprints


def test_home_page(client):
    """
    Test the home page route.
    """
    response = client.get('/')
    assert response.status_code == 200


# Run the tests
if __name__ == "__main__":
    pytest.main()
