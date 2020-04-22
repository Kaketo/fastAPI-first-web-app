from typing import Dict, List
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()
app.counter = 0
app.patients = list()


@app.get("/")
def root():
	return{"message": "Hello World during the coronavirus pandemic!"}

@app.get("/welcome")
def welcome():
	return{"message" : "Welcome"}

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


@app.post("/patient", response_model=PatientDictResp)
def post_patient(rq: PatientDictRq):
	app.patients.append(rq)
	N = app.counter + 1
	app.counter += 1
	return PatientDictResp(id=N, patient=rq.dict())

@app.get("/patient/{pk}", response_model=PatientDictRq)
def get_patient_info(pk: int):
	if pk <= app.counter:
		return app.patients[pk-1]
	else:
		return JSONResponse(status_code=204, content={})