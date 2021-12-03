from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
import json
from .models import User
from . import models
from .database import SessionLocal, engine
# from . import models
# from .models import User
from werkzeug.security import generate_password_hash
# from .database import SessionLocal, engine
import time

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post('/users/', status_code=200)
async def create_user(request: Request, response: Response,db: Session = Depends(get_db)):
    _json = await request.json()
    responseMessage = {'message' : 'The account has been created'}
    responseStatusCode = 200

    time.sleep(5)
	
    email    = _json.get('email')
    name     = _json.get('name')
    password = _json.get('password')
    twitter_username = request.form.get('twitter_username')
    twitter_id = api.request(f'users/by/username/:{twitter_username}')
    twitter_id = twitter_id.json()['data']['id']

    user = db.query(models.User).filter(models.User.email == email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        responseMessage = {'message' : 'Email address already exists'}
        responseStatusCode = status.HTTP_400_BAD_REQUEST
    else:
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, 
                        name=name, 
                        password=generate_password_hash(password, method='sha256'),
                        twitter_id=twitter_id,
                        twitter_username=twitter_username)

        # add the new user to the database
         # add the new user to the database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    
    response.status_code = responseStatusCode

    return responseMessage