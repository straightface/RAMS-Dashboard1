import os, json, datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from utils.security import hash_password, verify_password, create_token, decode_token

BASE = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE, "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
PROJECTS_FILE = os.path.join(DATA_DIR, "projects.json")
TEMPLATES_FILE = os.path.join(DATA_DIR, "templates.json")
RAMS_FILE = os.path.join(DATA_DIR, "rams_records.json")
FRONTEND_BUILD = os.path.abspath(os.path.join(BASE, "..", "frontend", "build"))
os.makedirs(DATA_DIR, exist_ok=True)

app = FastAPI(title="RAMS Automater Combined App (v13)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.isdir(FRONTEND_BUILD):
    app.mount("/", StaticFiles(directory=FRONTEND_BUILD, html=True), name="frontend")

def load(path):
    if not os.path.exists(path):
        return []
    with open(path,'r') as f:
        return json.load(f)
def save(path, data):
    with open(path,'w') as f:
        json.dump(data, f, indent=2)

def require_role(request: Request, allowed_roles: List[str]):
    auth = request.headers.get('authorization') or ''
    token = auth.split(' ',1)[1] if auth.startswith('Bearer ') else None
    if not token:
        raise HTTPException(status_code=401, detail='Missing token')
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail='Invalid token')
    user_roles = payload.get('roles') or []
    if not any(r in allowed_roles for r in user_roles):
        raise HTTPException(status_code=403, detail='Forbidden')
    return payload

@app.get('/api/health')
def health(): return {'status':'ok'}

from pydantic import BaseModel
class LoginIn(BaseModel):
    username: str
    password: str

@app.post('/login')
def login(data: LoginIn):
    users = load(USERS_FILE)
    user = next((u for u in users if u['username']==data.username), None)
    if not user or not verify_password(data.password, user['password']):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_token({'username': user['username'], 'roles': user.get('roles', ['creator'])})
    return {'access_token': token, 'roles': user.get('roles', ['creator'])}

@app.get('/api/admin/users')
def list_users(request: Request):
    require_role(request, ['admin'])
    return {'users': load(USERS_FILE)}

@app.get('/api/projects/active')
def projects_active(request: Request):
    require_role(request, ['creator','approver','admin'])
    return {'projects': load(PROJECTS_FILE)}

@app.get('/api/templates/active')
def templates_active(request: Request):
    require_role(request, ['creator','approver','admin'])
    return {'templates': load(TEMPLATES_FILE)}

@app.get('/api/rams/list')
def rams_list(request: Request):
    require_role(request, ['creator','approver','admin'])
    return {'records': load(RAMS_FILE)}

@app.post('/api/rams/create')
def rams_create(request: Request, data: dict):
    require_role(request, ['creator','admin'])
    records = load(RAMS_FILE)
    ramsref = f"R{len(records)+1:04d}"
    rec = {'ramsref': ramsref, 'projectref': data.get('projectref'), 'template_id': data.get('template_id'),
           'revision': 1, 'status':'pending', 'created_on': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
    records.append(rec); save(RAMS_FILE, records)
    return {'ok': True, 'rams': rec}

@app.post('/api/rams/approve')
def rams_approve(request: Request, data: dict):
    require_role(request, ['approver','admin'])
    records = load(RAMS_FILE)
    target = next((r for r in records if r.get('ramsref')==data.get('ramsref')), None)
    if not target:
        raise HTTPException(status_code=404, detail='not found')
    if data.get('approve', True):
        target['status'] = 'approved'
        target['revision'] = target.get('revision',1) + 1
        token = request.headers.get('authorization','').split(' ',1)[1] if request.headers.get('authorization') else None
        target['approved_by'] = decode_token(token).get('username') if token else None
    else:
        target['status'] = 'rejected'
    save(RAMS_FILE, records)
    return {'ok': True, 'rams': target}

@app.get('/')
def index_fallback():
    if os.path.isdir(FRONTEND_BUILD):
        index = os.path.join(FRONTEND_BUILD, 'index.html')
        if os.path.exists(index):
            return FileResponse(index, media_type='text/html')
    return HTMLResponse('<html><body><h2>RAMS Automater API running (frontend not built)</h2></body></html>')
