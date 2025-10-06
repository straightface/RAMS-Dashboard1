from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import os, json, datetime
from utils.security import verify_password, create_token, decode_token

BASE = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE, 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
PROJECTS_FILE = os.path.join(DATA_DIR, 'projects.json')
TEMPLATES_FILE = os.path.join(DATA_DIR, 'templates.json')
RAMS_FILE = os.path.join(DATA_DIR, 'rams_records.json')
os.makedirs(DATA_DIR, exist_ok=True)

app = FastAPI(title='RAMS Automater Backend (v12 secure)')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

def load(f): return json.load(open(f))
def save(f,d): json.dump(d, open(f,'w'), indent=2)

def require_role(req, roles):
    auth = req.headers.get('authorization') or ''
    token = auth.split(' ',1)[1] if auth.startswith('Bearer ') else None
    if not token: raise HTTPException(401,'Missing token')
    payload = decode_token(token)
    if not payload: raise HTTPException(401,'Invalid token')
    if not any(r in payload.get('roles',[]) for r in roles): raise HTTPException(403,'Forbidden')
    return payload

from pydantic import BaseModel
class LoginIn(BaseModel): username: str; password: str

@app.post('/login')
def login(data: LoginIn):
    users = load(USERS_FILE)
    u = next((x for x in users if x['username']==data.username), None)
    from utils.security import verify_password, create_token
    if not u or not verify_password(data.password, u['password']):
        raise HTTPException(401, 'Invalid credentials')
    return {'access_token': create_token({'username': u['username'],'roles': u['roles']}), 'roles': u['roles']}

@app.get('/')
def root(): return {'message':'RAMS API running'}
