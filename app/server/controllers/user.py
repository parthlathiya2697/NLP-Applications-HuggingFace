import os
from bson.objectid import ObjectId
# from ..utils.main import get_collection
from server.database import get_collection
from ..utils.auth_handler import Hashing

user_collection = get_collection("users_collection")

check_list = ["password_key", "password_salt", "is_active", "is_admin", "is_staff"]

# helpers
def user_helper(user) -> dict:
    res_dict = {}
    for k, v in user.items():
        if k in check_list:
            pass
        else:
            if k != "_id":
                res_dict[k] = v
            else:
                res_dict['id'] = str(v)
    return res_dict

async def check_availability(fields, id=None):
    """
    fields will be list of dictionary with key as field name and value as new value to be enter to the db
    """
    print("runs well")
    status = (True, "field value is available")
    users = [user async for user in user_collection.find()]
    for f in fields:
        for user in users:
            user = {(k if k != "_id" else "id"): v if k != "_id" else str(v) for k, v in user.items()}
            if user.get("id") != id:
                k = list(f.keys())[0]
                v = list(f.values())[0]
                if v != None and v == user.get(k):
                    status = (False, f"{k} already exists")
                    return status
    return status

# crud operations
# Retrieve all users present in the database
async def get_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users

# Add a new user into to the database
async def add_user(data) -> dict:
    data = Hashing().pass_hash(data)
    user = await user_collection.insert_one(data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

# Retrieve a user with a matching ID
async def get_user(id: str) -> dict:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)

# Update a user with a matching ID
async def update_user(id: str, data: dict):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one({"_id": ObjectId(id)},
                                                        {"$set": data})
        if updated_user:
            return True
        return False

# Delete a user from the database
async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True

# get user's connections
async def get_connections(id):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        conn = [await get_user(id) for id in user.get("connections") if id != None or ""]
        return conn
    return False


    