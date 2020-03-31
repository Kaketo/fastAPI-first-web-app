from typing import Dict, List
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def root():
	return{"message": "Hello World during the coronavirus pandemic!"}

@app.get("/method")
def read_method():
	return{"method": 'GET'}

@app.post("/method")
def read_method():
	return{"method": 'POST'}

@app.put("/method")
def read_method():
	return{"method": 'PUT'}

@app.delete("/method")
def read_method():
	return{"method": 'DELETE'}


class PatientDictRq(BaseModel):
	name: str
	surename: str

class PatientDictResp(BaseModel):
	id: int
	patient: PatientDictRq

class PatientDatabase(BaseModel):
	patients_dict: Dict

patients = PatientDatabase(patients_dict={})

@app.post("/patient", response_model=PatientDictResp)
def post_patient(rq: PatientDictRq):
	N = len(patients.patients_dict) + 1
	patients.patients_dict[N] = rq
	return PatientDictResp(id=N, patient=rq.dict())

@app.get("/patient/{pk}", response_model=PatientDictRq)
def get_patient_info(pk: int):
	if pk in patients.patients_dict.keys():
		return patients.patients_dict.get(pk)
	else:
		return JSONResponse(status_code=204, content={})