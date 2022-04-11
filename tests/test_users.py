from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'message':"Hello world!!!"}

def test_create_user():
    #request = email and password
    res = client.post("/users/", json={"email": "stuff2@gmail.com", "password": "stuff"})
    assert res.status_code == 201
    print(res.json())
    #response = email and created at