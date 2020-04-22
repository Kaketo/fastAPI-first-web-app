from typing import Dict, List
from fastapi import FastAPI, Response, Cookie, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from hashlib import sha256
import secrets


app = FastAPI()
security = HTTPBasic()

app.counter = 0
app.patients = list()

app.secret_key = "LPYGCwTTEXBzhjLp86TRAYQBvXa5fAEf249YxC9RAfS7YSj2rHUdf6W4S7jzN4yw"
app.users = {"trudnY":"PaC13Nt"}

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

@app.post("/login")
def create_session(response: Response, credentials:  HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}" , encoding='utf8')).hexdigest()
    response.set_cookie(key="session_token", value=session_token)
    response.status_code = status.HTTP_302_FOUND
    response.headers["Location"] = "/welcome"




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