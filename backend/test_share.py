# test_share.py

import pytest
from flask import Flask
from share import bp as share_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['MYSQL_HOST'] = 'mock'
    app.config['MYSQL_USER'] = 'mock'
    app.config['MYSQL_PASSWORD'] = 'mock'
    app.config['MYSQL_DB'] = 'mock'

    # Mock MySQL cursor and connection
    class DummyCursor:
        def execute(self, query, params=None):
            self.last_query = query
            self.last_params = params
        def fetchall(self):
            return [(1, "Buddy", "Dog", "Lab", 5, "view")]
        def fetchone(self):
            return (1, "Buddy", "Dog", "Lab", 5, "view")
        def close(self):
            pass

    class DummyConnection:
        def cursor(self):
            return DummyCursor()
        def commit(self):
            pass

    class DummyMySQL:
        def __init__(self):
            self.connection = DummyConnection()

    # Inject mock MySQL
    app.extensions['mysql'] = DummyMySQL()

    # Register your blueprint
    app.register_blueprint(share_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_share_pet_success(client):
    payload = {
        "pet_id": 1,
        "shared_with_user_id": 2,
        "permission_level": "view"
    }
    response = client.post("/share", json=payload)
    assert response.status_code == 201
    assert b"Pet profile shared successfully" in response.data

def test_get_shared_pets(client):
    response = client.get("/share/2")
    assert response.status_code == 200
    assert b"Buddy" in response.data
