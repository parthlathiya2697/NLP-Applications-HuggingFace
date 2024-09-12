import time, os, jwt, hashlib
from fastapi.encoders import jsonable_encoder
import configparser
from typing import Dict
import motor.motor_asyncio
from config import BASE_DIR
# from ..utils.main import get_collection
from server.database import get_collection

config = configparser.ConfigParser()
config.read(BASE_DIR + "/settings.ini")

# JWT Verifications
SECRET_KEY = config.get("settings", "SECRET_KEY")
JWT_ALGO = config.get("settings", "JWT_ALGO")

# Database
MONGO_DETAILS = config.get("settings", "DATABASE_URL")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

class Hashing:
    ALGO = config.get("settings", "HASHING_ALGO")
    ITR = int(config.get("settings", "HASHING_ITR"))

    @classmethod
    def pass_hash(cls, data):
        password_salt = os.urandom(32)
        password_key = hashlib.pbkdf2_hmac(cls.ALGO,
                                        data.get("password").encode("utf-8"),
                                        password_salt, cls.ITR)
        del data['password']
        return {**data, "password_salt": password_salt, "password_key": password_key}


    @classmethod
    def pass_check(cls, user):
        new_pk = hashlib.pbkdf2_hmac(cls.ALGO,
                                        user.get("password").encode("utf-8"),
                                        user.get("password_salt"), cls.ITR)
        print(f'-----------')
        print(f'Entered pk: {new_pk}, Saved pk: {user.get("password_key")}')
        if new_pk == user.get("password_key"):
            return True
        return False

async def check_user(credentials):
    print(credentials.get("username"))
    user_id = None
    users = [user async for user in get_collection("users_collection").find()]
    # import pdb
    # pdb.set_trace()
    print(users)
    for user in users:
        user = {(k if k != "_id" else "id"): v if k != "_id" else str(v) for k, v in user.items()}
        print(user.get("email"))
        # Check entered username(->email or ->contact) 
        if credentials.get("username") == user.get("email") or credentials.get("username") == user.get("contact"):
            status = Hashing().pass_check({**user,**credentials} )
            if status:
                return str(user.get("id"))
    return user_id
    

def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 120*60
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGO)

    return token

def decodeJWT(token: str) -> dict: 
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGO])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}

def get_user(req):
    auth = req.headers["Authorization"]
    scheme, token = auth.split()
    token_datadict = decodeJWT(token)
    return token_datadict