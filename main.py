from typing import Dict, List
from fastapi import FastAPI,Request, Response, Cookie, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from hashlib import sha256

import secrets


app = FastAPI()
security = HTTPBasic()
templates = Jinja2Templates(directory="templates")

app.counter = 0
app.patients = dict()

app.secret_key = "LPYGCwTTEXBzhjLp86TRAYQBvXa5fAEf249YxC9RAfS7YSj2rHUdf6W4S7jzN4yw"
app.users = {"trudnY":"PaC13Nt"}
app.sessions={}

def check_session(session_token: str = Cookie(None)):
    if session_token not in app.sessions:
        session_token = None
    return session_token

@app.get("/")
def root():
	return{"message": "Hello World during the coronavirus pandemic!"}

@app.get("/welcome")
def welcome(request: Request, response : Response, session_token: str = Depends(check_session)):
	if session_token is None:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "Log in to access."
	username = app.sessions[session_token]
	return templates.TemplateResponse("item.html", {"request": request, "user": username})


@app.post("/login")
def login(response: Response, credentials:  HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}" , encoding='utf8')).hexdigest()
    app.sessions[session_token]=credentials.username
    response.set_cookie(key="session_token", value=session_token)
    response.status_code = status.HTTP_302_FOUND
    response.headers["Location"] = "/welcome"



@app.post("/logout")
def logout(response: Response, session_token: str = Depends(check_session)):
	if session_token is None:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "Log in to access."
	response.status_code = status.HTTP_302_FOUND
	response.headers['Location'] = "/"
	app.sessions.pop(session_token)

class PatientDictRq(BaseModel):
	name: str
	surname: str

class PatientDictResp(BaseModel):
	id: int
	patient: PatientDictRq


@app.post("/patient")
def post_patient(response: Response, rq: PatientDictRq, session_token: str = Depends(check_session)):
	if session_token is None:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "Log in to access."
	app.patients[app.counter] = rq
	response.headers["Location"] = "/patient/" + str(app.counter)
	response.status_code = status.HTTP_302_FOUND
	app.counter += 1

@app.get("/patient")
def get_patients(response: Response, session_token: str = Depends(check_session)):
	if session_token is None:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "Log in to access."
	return app.patients

@app.get("/patient/{id}")
def get_patient(id: int, response: Response, session_token: str = Depends(check_session)):
	if session_token is None:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "Log in to access."
	if id in app.patients.keys():
		return app.patients[id]
	else:
		response.status_code = status.HTTP_204_NO_CONTENT

@app.delete("/patient/{id}")
def delete_patient(id: int, response: Response, session_token: str = Depends(check_session)):
	if session_token is None:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "Log in to access."
	app.patients.pop(id)
	response.status_code = status.HTTP_204_NO_CONTENT