import os, datetime
from passlib.context import CryptContext
import jwt

pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET = os.environ.get('JWT_SECRET', 'change_me_securely')
ALGO = 'HS256'
ACCESS_EXPIRES_SECONDS = 60*60*4

def hash_password(password: str) -> str:
    return pwd_ctx.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    if isinstance(hashed, str) and hashed.startswith('PLAINTEXT:'):
        return plain == hashed.split('PLAINTEXT:',1)[1]
    return pwd_ctx.verify(plain, hashed)

def create_token(data: dict) -> str:
    payload = data.copy()
    payload.update({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=ACCESS_EXPIRES_SECONDS)})
    return jwt.encode(payload, SECRET, algorithm=ALGO)

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGO])
    except Exception:
        return None
