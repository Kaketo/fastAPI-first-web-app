from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)

def test_root():
	response = client.get("/")
	assert response.status_code == 200
	assert response.json() == {"message": "Hello World during the coronavirus pandemic!"}



def test_print_method_get():
	response = client.get("/method")
	assert response.status_code == 200
	assert response.json() == {"method": "GET"}

def test_print_method_post():
	response = client.post("/method")
	assert response.status_code == 200
	assert response.json() == {"method": "POST"}

def test_print_method_put():
	response = client.put("/method")
	assert response.status_code == 200
	assert response.json() == {"method": "PUT"}

def test_print_method_delete():
	response = client.delete("/method")
	assert response.status_code == 200
	assert response.json() == {"method": "DELETE"}


test_patients = {}

@pytest.mark.parametrize("id,json_data", [
	(1, {"name": "TOMEK", "surename": "DOMEK"}), 
	(2, {"name": "JAN", "surename": "PAN"}),
	(3, {"name": "KASIA", "surename": "DASIA"})])
def test_patient(id,json_data):
	response = client.post("/patient", json=json_data)
	assert response.status_code == 200
	assert response.json() == {"id": id, "patient": json_data}

	test_patients[id] = json_data


def test_get_patient():
	for i in range(1,4):
		response = client.get(f"/patient/{i}")
		assert response.json() == test_patients[i]
		assert response.status_code == 200

	for i in range(4,6):
		response = client.get(f"/patient/{i}")
		assert response.json() == {}
		assert response.status_code == 204