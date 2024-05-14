from fastapi import APIRouter,File,UploadFile
from typing import List
from pydantic import BaseModel
import hashlib
from models import *


user_router = APIRouter()


class RegisterModel(BaseModel):
    username: str
    password: str
    nickname: str
    role: int


@user_router.post("/register")
async def register(data: RegisterModel):
    checkdata = await User.filter(username=data.username).first()
    if checkdata != None:
        return {
            "code":"0",
            "error":"已存在用户",
            "msg": "已存在用户"

        }
    # 对密码进行 MD5 加密
    hashed_password = hashlib.md5(data.password.encode()).hexdigest()
    print(type(data.password.encode()),type(data.password),data.password)
    # 创建用户并存储加密后的密码
    user = await User.create(username=data.username, password=hashed_password, role=data.role,nickname=data.nickname)

    return {
        "code": "200",
        "msg": "注册成功",
        "data":user
    }

class LoginModel(BaseModel):
    username: str
    password: str

@user_router.post("/login")
async def login(data: LoginModel):
    checkdata = await User.filter(username=data.username).first()

    if checkdata is None:
        return {
            "code": "0",
            "error": "未找到用户",
            "msg": "登录失败"
        }

    hashed_password = hashlib.md5(data.password.encode()).hexdigest()

    if checkdata.password == hashed_password:
        return {
            "code": "200",
            "msg": "登录成功",
            "data": {
                "id":checkdata.id,
                "username": checkdata.username,
                "role": checkdata.role,
                "nickname": checkdata.nickname
            }
        }
    else:
        return {
            "code": "0",
            "msg": "登录失败",
            "error": "密码或者账号错误"
        }


@user_router.get("/getuser")
async def getuser():
    data = await User.all().values('id', 'username','role','nickname')
    return {
        "code":200
        ,"msg":"获取成功"
        ,"data":data
    }

