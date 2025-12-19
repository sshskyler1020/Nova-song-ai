from passlib.hash import bcrypt
from jose import jwt, JWTError

SECRET_KEY = "SUPERSECRETKEY"

USERS = {}

def create_user(email, password):
    if email in USERS: return {"error":"User exists"}
    hashed = bcrypt.hash(password)
    USERS[email] = {"password":hashed,"is_premium":False}
    token = jwt.encode({"email":email}, SECRET_KEY)
    return {"token":token}

def login_user(email, password):
    user = USERS.get(email)
    if user and bcrypt.verify(password, user["password"]):
        return jwt.encode({"email":email}, SECRET_KEY)
    return None

def get_user(token):
    try:
        data = jwt.decode(token, SECRET_KEY)
        email = data["email"]
        return USERS.get(email)
    except JWTError:
        return None
