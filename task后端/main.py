import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from settings import TORTOISE_ORM
from user.login_register import user_router
from task.task import task_router
from task.taskmanage import taskmanage_router
app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["user_router"])
app.include_router(task_router, prefix="/task", tags=["task_router"])
app.include_router(taskmanage_router, prefix="/taskmanage", tags=["taskmanage"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],  # 添加 OPTIONS 方法
    allow_headers=["*"],
)

# 该方法会在fastapi启动时触发，内部通过传递进去的app对象，监听服务启动和终止事件
# 当检测到启动事件时，会初始化Tortoise对象，如果generate_schemas为True则还会进行数据库迁移
# 当检测到终止事件时，会关闭连接
register_tortoise(
    app=app,
    config=TORTOISE_ORM,
    generate_schemas=True,  # 如果数据库为空，则自动生成对应表单，生产环境不要开
    # add_exception_handlers=True,  # 生产环境不要开，会泄露调试信息
)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8001, reload=True, workers=1)
