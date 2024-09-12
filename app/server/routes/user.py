import logging
from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ..utils.auth_bearer import JWTBearer
from ..utils.auth_handler import get_user as get_auth_user

from ..controllers.user import (add_user, get_users, get_user, 
                                update_user, check_availability)

from ..models.main import (ResponseModel, ErrorResponseModel)
from ..models.user import (AccountModel, ProfileModel, UpdateAccount, Chatname,
                            ConnectionModel, LoginModel, BindActivities, PrivacyModel)
from ..utils.auth_handler import check_user, signJWT

logger = logging.getLogger(__name__)

router = APIRouter()

##########################
##########################
# tested and ok with postman

# Add user
@router.post("/", response_description="user data added into the database")
async def add_user_(account: AccountModel):
    account = jsonable_encoder(account)
    check_list = [{"email": account.get("email")}, {"phone": account.get("phone")}]
    status = await check_availability(check_list)
    if status[0]:
        new_user = await add_user(account)
        return ResponseModel(new_user, "user added successfully.")
    logger.error("email or phone number already occupied")
    return JSONResponse(content=ErrorResponseModel("not available", 409, status[1]), status_code=409)

# Get all users (unauthenticated)
@router.get("/all", response_description="users retrieved")
async def get_users_():
    users = await get_users()
    if users:
        return ResponseModel(users, "users data retrieved successfully")
    logger.info("empty list returned")
    return ResponseModel(users, "empty list returned")

# Get user with id
@router.get("/{id}", dependencies=[Depends(JWTBearer())], response_description="user data retrieved")
async def get_user_(id: str):
    user = await get_user(id)
    if user:
        return ResponseModel(user, "user data retrieved successfully")
    logger.info("something went wrong in getting user's data")
    return JSONResponse(content=ErrorResponseModel("An error occurred.", 409, "user doesn't exist."), status_code=409)

# Get current user
@router.get("/", dependencies=[Depends(JWTBearer())], response_description="user data retrieved")
async def get_user_(req: Request):
    user_id = get_auth_user(req).get("user_id")
    user = await get_user(user_id)
    if user:
        return ResponseModel(user, "user data retrieved successfully")
    logger.info("something went wrong in getting user's data")
    return JSONResponse(content=ErrorResponseModel("An error occurred.", 409, "user doesn't exist."), status_code=409)

# Update account for user (unauthenticated)
@router.put("/{id}")
async def update_account_(id : str, acc: UpdateAccount):
    acc = jsonable_encoder(acc)
    # Return false if an empty profile body is sent.
    if len(acc) < 1:
        logger.error("empty data. may be need to add some data")
        return JSONResponse(content=ErrorResponseModel("empty data", 404, "please fill some data to update profile"), status_code=404) 
    updated_user = await update_user(id, acc)
    if updated_user:
        return ResponseModel("user with ID: {} updated successful".format(id), "user updated successfully")
    logger.error("something went wrong in updating the user")
    return JSONResponse(content=ErrorResponseModel("not available", 409, "something went wrong in updating the user"), status_code=409)

# Update user profile
@router.put("/", dependencies=[Depends(JWTBearer())])
async def update_user_(req: Request, pro: ProfileModel = Depends(ProfileModel.as_form)):
    id = get_auth_user(req).get("user_id")
    pro = jsonable_encoder(pro)
    pro = {k: v for k, v in pro.items() if v is not None}
    check_list = [{"email": pro.get("email")}, {"phone": pro.get("phone")}]
    if len(pro) < 1:
        logger.error("empty data. may be need to add some data")
        return JSONResponse(content=ErrorResponseModel("empty data", 404, "please fill some data to update profile"), status_code=404) 
    status = await check_availability(check_list, id) # checks email/phone is available 
    if status[0]:
        updated_user = await update_user(id, pro)
        if updated_user:
            return ResponseModel("User updated", f"user with ID: {id} updated successful")
        else:
            updated_user = await update_user(id, pro)
            if updated_user:
                return ResponseModel("user updated without image field", f"user with ID: {id} updated successful")
    logger.warning("email or phone might be unavailable")
    return JSONResponse(content=ErrorResponseModel("not available", 409, status[1]), status_code=409)

@router.delete("/", dependencies=[Depends(JWTBearer())], response_description="user data deleted from the database")
async def delete_user_(req: Request):
    id = get_auth_user(req).get("user_id")
    deleted_user = await update_user(id, {"active": False, "image_url": None}) #updates active state to false wan't delete user
    if deleted_user:
        return ResponseModel("user with ID: {} removed".format(id), "user inactivated successfully")
    logger.error("user does not exists")
    return JSONResponse(content=ErrorResponseModel("An error occurred", 404, "user with id {0} doesn't exist".format(id)), status_code=404)

@router.post("/login", response_description="user's login")
async def login_user(credentials: LoginModel):
    credentials = jsonable_encoder(credentials)
    user_id = await check_user(credentials)
    if user_id:
        status = await update_user(user_id, {"last_login": credentials.get("last_login")})
        user = await get_user(user_id)
        token = signJWT(user_id)
        res = {"token": token, **user}
        return ResponseModel(res, "you have successfully logged in")
    logger.error("not valid credentials")
    return JSONResponse(content=ErrorResponseModel("not valid credentials!", 401, "please check the entered email and password"), status_code=401)

@router.post("/privacy", dependencies=[Depends(JWTBearer())], response_description="activities added to the user")
async def add_users_activity(req: Request, pm: PrivacyModel):
    user = get_auth_user(req)
    pm = jsonable_encoder(pm)
    status = await update_user(user.get("user_id"), pm)
    if status:
        return ResponseModel(f"privacy updated with the user with ID: {user.get('user_id')}", "user updated with given privacy")
    logger.error("error in updating the privacy of user")
    return JSONResponse(content=ErrorResponseModel("an error occurred", 404, "there was an error updating the privacy of user"), status_code=404)
