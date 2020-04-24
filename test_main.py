from fastapi.testclient import TestClient
import pytest
from main import app
from base64 import b64encode
from pydantic import BaseModel

client = TestClient(app)

def test_root():
	response = client.get("/")
	assert response.status_code == 200
	assert response.json() == {"message": "Hello World during the coronavirus pandemic!"}

def test_welcome():
	response = client.get("/welcome")
	assert response.status_code != 404
	# assert response.json() == {"message" : "Welcome"}

def test_logout():
    credentials = b64encode(b"trudnY:PaC13Nt").decode('utf-8')
    response = client.post("/logout")
    assert response.status_code == 401
    response = client.post("/login", headers={"Authorization": f"Basic {credentials}"})
    response = client.post("/logout")
    assert response.status_code == 302

def test_login():
    credentials = b64encode(b"trudnY:PaC13Nt").decode('utf-8')
    response = client.post("/login", headers={"Authorization": f"Basic {credentials}"})
    # assert response.json() == {"message" : "Welcome"}
    assert response.status_code in (301, 302, 303, 307)
    client.post("/logout")
	

def test_post_patient():
    response = client.post("/patient", json={'name':'Jan','surname':'Kowalski'})
    assert response.status_code == 401

    credentials = b64encode(b"trudnY:PaC13Nt").decode('utf-8')
    client.post("/login", headers={"Authorization": f"Basic {credentials}"})

    response = client.post("/patient", json = {'name':'Jan','surname':'Kowalski'})
    response.headers["Location"] = "/patient/0"
    assert response.status_code == 302

    response = client.post("/patient", json = {'name':'Jan','surname':'Kowalski'})
    response.headers["Location"] = "/patient/1"
    assert response.status_code == 302

    client.post("/logout")

def test_get_patietn():
    credentials = b64encode(b"trudnY:PaC13Nt").decode('utf-8')
    client.post("/login", headers={"Authorization": f"Basic {credentials}"})

    response = client.get("/patient")
    assert response.status_code == 200
    assert response.json() == {'0':{'name':'Jan','surname':'Kowalski'},'1':{'name':'Jan','surname':'Kowalski'}}

    client.post("/logout")
def test_patient_info():
    credentials = b64encode(b"trudnY:PaC13Nt").decode('utf-8')
    client.post("/login", headers={"Authorization": f"Basic {credentials}"})

    response = client.get("/patient/0")
    assert response.status_code == 200
    assert response.json() == {'name':'Jan','surname':'Kowalski'}

    response = client.get("/patient/100")
    assert response.status_code == 204

    client.post("/logout")

def test_delete_patients():
    credentials = b64encode(b"trudnY:PaC13Nt").decode('utf-8')
    client.post("/login", headers={"Authorization": f"Basic {credentials}"})

    response = client.delete("/patient/0")
    assert response.status_code == 204
    response = client.get("/patient/0")
    assert response.status_code == 204

    client.post("/logout")