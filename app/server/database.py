import motor.motor_asyncio
import configparser
from config import BASE_DIR



def get_collection(collection):
    config = configparser.ConfigParser()
    config.read(BASE_DIR + "/settings.ini")

    # database connections
    MONGO_DETAILS = config.get("settings", "DATABASE_URL")
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
    database = client.huggingai
    conn = database.get_collection(collection)
    return conn