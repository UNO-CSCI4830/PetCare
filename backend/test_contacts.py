# test_contacts.py

import pytest
from flask import Flask
from contacts import bp as contacts_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['MYSQL_HOST'] = 'mock'
    app.config['MYSQL_USER'] = 'mock'
    app.config['MYSQL_PASSWORD'] = 'mock'
    app.config['MYSQL_DB'] = 'mock'
    app.config['MYSQL_PORT'] = 3306

    class DummyCursor:
        def __init__(self):
            self.lastrowid = 123
            self.last_params = None

        def execute(self, query, params=None):
            self.last_params = params

        def fetchall(self):
            return [(1, 'Alice', 'alice@example.com'), (2, 'Bob', 'bob@example.com')]

        def fetchone(self):
            if self.last_params == (999,):
                return None
            return (1, 'Alice', 'alice@example.com')

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

    app.extensions['mysql'] = DummyMySQL()
    app.register_blueprint(contacts_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_contacts_success(client):
    response = client.get('/contacts')
    assert response.status_code == 200

def test_add_contact_success(client):
    payload = {'name': 'Charlie', 'email': 'charlie@example.com'}
    response = client.post('/contacts', json=payload)
    assert response.status_code == 201
    assert response.get_json()['id'] == 123

def test_add_contact_missing_fields(client):
    response = client.post('/contacts', json={'name': 'NoEmail'})
    assert response.status_code == 400

def test_get_specific_contact_success(client):
    response = client.get('/contacts/1')
    assert response.status_code == 200

def test_get_specific_contact_not_found(client):
    response = client.get('/contacts/999')
    assert response.status_code == 404

def test_delete_contact(client):
    response = client.delete('/contacts/1')
    assert response.status_code == 204

def test_update_contact_success(client):
    payload = {'name': 'Updated', 'email': 'updated@example.com'}
    response = client.put('/contacts/1', json=payload)
    assert response.status_code == 200

def test_update_contact_missing_fields(client):
    response = client.put('/contacts/1', json={'name': 'OnlyName'})
    assert response.status_code == 400
