from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from fastapi.security import OAuth2PasswordBearer
import json
from datetime import datetime
import os
from typing import List
from schemas import Object, ObjectCreate
import auth

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = auth.TokenData(username=username)
    except auth.JWTError:
        raise credentials_exception
    users = json.load(open('users.json'))
    user = next((user for user in users if user['username'] == username), None)
    if user is None:
        raise credentials_exception
    return user

@router.post("/upload/", response_model=Object)
async def upload_object(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    objects = json.load(open('objects.json'))
    obj = {
        "id": len(objects) + 1,
        "owner": current_user['username'],
        "file_name": file.filename,
        "upload_date": datetime.now().isoformat(),
        "preview_link": f"http://localhost:8000/files/{file.filename}"  # Placeholder link
    }
    objects.append(obj)
    with open('objects.json', 'w') as f:
        json.dump(objects, f, indent=4)
    return obj

@router.get("/objects/", response_model=List[Object])
async def list_objects(current_user: dict = Depends(get_current_user)):
    objects = json.load(open('objects.json'))
    user_objects = [obj for obj in objects if obj['owner'] == current_user['username']]
    return user_objects
