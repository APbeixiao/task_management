from datetime import datetime, date

from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from typing import List, Union
from pydantic import BaseModel
from models import *
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import in_transaction

task_router = APIRouter()

class AddModel(BaseModel):
    name: str
    description: str  # 任务描述
    status: str  # 任务状态
    progress: int  # 进度百分比
    deadline: datetime  # 截止日期
    # reason_for_progress_change: str  # 项目进度变更原因
    created_user: int

@task_router.post("/addtask",description="添加一个任务到系统中。")
async def add(data: AddModel):
    user_id = data.created_user
    user = await User.get(id=user_id)  # 获取用户对象
    add_data = await Task.create(
        name=data.name,
        description=data.description,
        status=data.status,
        progress=data.progress,
        deadline=data.deadline,
        reason_for_progress_change="无",
        created_user=user  # 将用户对象关联到任务中
    )
    return {
        "code":"200",
        "msg":"新增成功"
    }
class DeleteTask(BaseModel):
    task_id:Union[int, List[int]]

@task_router.post("/delete", description="根据提供的任务ID删除一个或多个任务。")
async def delete_task(data: DeleteTask):

    if type(data.task_id) == int:
        deleted_count = await Task.filter(id=data.task_id).delete()  # 条件删除
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"{data.task_id} not found")
        return {
            "code": "200",
            "msg": "删除成功"
        }
    elif type(data.task_id) == list:
        for i in data.task_id:
            deleted_count = await Task.filter(id=i).delete()  # 条件删除
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f" {data.task_id} not found")
        return {
            "code": "200",
            "msg": "删除成功"
        }


class DeleteData(BaseModel):
    id: Union[int, List[int]]

@task_router.post("/delete_TaskAssignment", description="根据提供的ID删除一个或多个任务分配。")
async def delete_TaskAssignment(data: DeleteData):

    if isinstance(data.id, int):
        deleted_count = await TaskAssignment.filter(task_id=data.id).delete()  # 条件删除
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"{data.id} not found")
        return {
            "code": "200",
            "msg": "删除成功"
        }
    elif isinstance(data.id, list):
        deleted_count = 0
        for i in data.id:
            deleted_count += await TaskAssignment.filter(task_id=i).delete()  # 条件删除
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"IDs not found")
        return {
            "code": "200",
            "msg": "删除成功"
        }

class AssignmentModel(BaseModel):
    task: int
    assigned_to:Union[int, List[int]]
@task_router.post("/add_assignment",description="为任务添加分配，将任务分配给一个或多个用户。")
async def add(data:AssignmentModel):


    if type(data.assigned_to) == int:
        try:
            user = await User.get(id=data.assigned_to)  # 获取用户对象
            task = await Task.get(id=data.task)  # 获取用户对象
        except:
            return {
                "code": "0"
            }

        add_data = await TaskAssignment.create(
            task=task,
            assigned_to=user
        )
        return {
            "code": "200",
            "msg": "新增成功",
            "data": add_data
        }
    elif type(data.assigned_to) == list:
        for i in data.assigned_to:
            try:
                user = await User.get(id=i)  # 获取用户对象
                task = await Task.get(id=data.task)  # 获取用户对象
            except:
                return {
                    "code": "0"
                }
            add_data = await TaskAssignment.create(
                task=task,
                assigned_to=user
            )
        return {
            "code": "200",
            "msg": "新增成功",
            "data": add_data
        }

#编辑任务分配(删除再添加)
@task_router.post("/editassignment",description="编辑任务分配(删除再添加)")
async def editassignment(data:AssignmentModel):
    try:
        await TaskAssignment.filter(task_id=data.task).delete()
    except:
        return {
            "code": "0"
        }

    if type(data.assigned_to) == int:
        try:
            user = await User.get(id=data.assigned_to)  # 获取用户对象
            task = await Task.get(id=data.task)  # 获取用户对象
        except:
            return {
                "code": "0"
            }

        add_data = await TaskAssignment.create(
            task=task,
            assigned_to=user
        )
        return {
            "code": "200",
            "msg": "修改成功",
            "data": add_data
        }
    elif type(data.assigned_to) == list:
        for i in data.assigned_to:
            try:
                user = await User.get(id=i)  # 获取用户对象
                task = await Task.get(id=data.task)  # 获取用户对象
            except:
                return {
                    "code": "0"
                }
            add_data = await TaskAssignment.create(
                task=task,
                assigned_to=user
            )
        return {
            "code": "200",
            "msg": "修改成功",
            "data": add_data
        }
#获取被分配的任务
@task_router.get("/gettask", description="根据用户ID获取该用户被分配的任务列表。")
async def get_tasks_by_assigned_to(assigned_to: int,limit:Union[int, None] = None):
    # 查询 TaskAssignment 表，获取所有 assigned_to_id 等于 assigned_to 的 task_id 值

    task_assignments = await TaskAssignment.filter(assigned_to_id=assigned_to).values_list('task_id', flat=True)

    # 根据获取到的 task_id 值在 Task 表中查询所有数据
    if limit != None:
        tasks = await Task.filter(id__in=task_assignments).order_by('created_at').limit(limit)
    else:
        tasks = await Task.filter(id__in=task_assignments).order_by('created_at')
    if tasks != []:
        return {
            "code": "200",
            "data": tasks
        }
    else:
        return {
            "code": "0",
            "msg":"未找到数据"
        }
@task_router.get("/get_limit_task", description="根据用户ID获取该用户被分配的分页任务列表。")
async def get_limittasks_by_assigned_to(assigned_to: int, limit: Union[int, None] = None, skip: Union[int, None] = None):
    # 查询 TaskAssignment 表，获取所有 assigned_to_id 等于 assigned_to 的 task_id 值
    task_assignments = await TaskAssignment.filter(assigned_to_id=assigned_to).values_list('task_id', flat=True)

    # 根据获取到的 task_id 值在 Task 表中查询所有数据
    tasks = await Task.filter(id__in=task_assignments).order_by('created_at')

    total_tasks = len(tasks)  # 获取所有任务的总数

    if skip is not None:
        tasks = tasks[skip:]  # 根据 skip 跳过指定数量的任务

    if limit is not None:
        tasks = tasks[:limit]  # 限制返回的任务数量

    if tasks:
        return {
            "code": "200",
            "data": tasks,
            "count": total_tasks  # 返回所有任务的总数
        }
    else:
        return {
            "code": "0",
            "msg": "未找到数据"
        }
#获取创建的任务包括用户信息
@task_router.get("/get_create_task", description="根据创建者的ID获取其创建的所有任务列表，并包含用户信息。")
async def get_tasks_by_create(created_id: int, limit: Union[int, None] = None, skip: Union[int, None] = None):
    try:
        # 获取由特定用户创建的所有任务
        query = Task.filter(created_user=created_id)
        count = await query.count()
        # 应用分页参数
        if limit is not None:
            query = query.limit(limit)
        if skip is not None:
            query = query.offset(skip)

        tasks = await query.all()
          # 获取总数据条数
    except DoesNotExist:
        return [], 404  # 如果没有找到任务，返回空列表和404状态码

    # 初始化一个列表来存储任务及其用户信息
    tasks_with_users = []

    # 遍历所有任务
    for task in tasks:
        # 初始化一个列表来存储该任务的所有用户信息
        users_for_task = []

        # 获取与任务相关的所有用户分配
        task_assignments = await TaskAssignment.filter(task=task).all()

        # 遍历任务分配
        for task_assignment in task_assignments:
            try:
                # 获取分配的用户信息
                user = await User.get(id=task_assignment.assigned_to_id)
                users_for_task.append({
                    'username': user.nickname,
                    'userid': user.id,
                    # 可以添加其他User字段
                })
            except DoesNotExist:
                # 如果分配中的用户不存在，可以记录错误，但通常不会跳过，因为我们需要知道分配存在问题
                # 可以选择继续，或者记录错误，或者抛出异常
                continue

        # 将任务详情和该任务的所有用户信息添加到tasks_with_users列表中
        tasks_with_users.append({
            'taskid': task.id,
            'name': task.name,
            'description': task.description,
            'deadline': task.deadline,
            # 添加其他Task字段...
            'users': users_for_task  # 用户数组
        })

    # 返回带有用户数组的任务列表和总数据条数
    return {
        "code": "200",
        "data": tasks_with_users,
        "count": count
    }

#获取指定任务分配的用户
@task_router.get("/get_task_user",description="获取指定任务分配的用户")
async def get_task_user(task_id:int):
    try:
        # 获取由特定用户创建的所有任务，并预取相关的用户信息
        task_assignments = await TaskAssignment.filter(task=task_id).prefetch_related('assigned_to')

        # 从查询结果中构建用户信息列表
        user_info_list = []
        for assignment in task_assignments:
            user_info = {
                "user_id": assignment.assigned_to.id,
                "username": assignment.assigned_to.nickname,  # 假设用户模型中有 username 字段
                "id": assignment.assigned_to.id,
                "role":assignment.assigned_to.role
                # 可以根据需要添加其他用户信息字段
            }
            user_info_list.append(user_info)

        return user_info_list
    except DoesNotExist:
        return [], 404


#获取该用户创建的所有任务
@task_router.get("/get_task_list",description="获取该用户创建的所有任务")
async def get_taskslist_by_create(created_id: int):
    try:
        # 获取由特定用户创建的所有任务
        tasks = await Task.filter(created_user=created_id).all()

        # 获取所有TaskAssignment表中的任务
        assigned_tasks = await TaskAssignment.all().values_list('task_id', flat=True)

        # 找出未被分配的任务
        unassigned_tasks = [task for task in tasks if task.id not in assigned_tasks]

    except DoesNotExist:
        return [], 404  # 如果没有找到任务，返回空列表和404状态码

    return {
        "code": "200",
        "data": unassigned_tasks
    }

@task_router.get("/get_onetask_content",description="获取一个任务的所有内容")
async def get_onetask_content(task_id:int):
    try:
        task = await Task.get(id=task_id)
        return {
            "code": "200",
            "data": task
        }
    except DoesNotExist:
        return {
            "code": "0",
            "msg": "未找到数据"
        }

#修改任务
class ChangeTaskModel(BaseModel):
    task_id: int
    name: str
    description: str
    deadline: datetime
    status: str
@task_router.post("/change_task",description="修改任务")
async def change_task(data:ChangeTaskModel):
    try:
        task = await Task.get(id=data.task_id)
        task.name = data.name
        task.description = data.description
        task.deadline = data.deadline
        task.status = data.status
        await task.save()
        return {
            "code": "200",
            "msg": "修改成功"
        }
    except DoesNotExist:
        return {
            "code": "0",
            "msg": "未找到数据"
        }

#获取账号任务占比
@task_router.get("/get_task_percent",description="获取账号任务占比")
async def get_task_percent(user_id:int):
    try:
        # 获取由特定用户创建的所有任务
        owntasks = await TaskAssignment.filter(assigned_to=user_id)

        alltasks = await Task.all()

        return {
            "code": "200",
            "data": {
                "assigned_tasks": len(alltasks),
                "unassigned_tasks": len(owntasks)
            }
        }
    except DoesNotExist:
        return {
            "code": "0",
            "msg": "未找到数据"
        }
#获取用户任务时间占比
@task_router.get("/get_task_time_percent",description="获取用户任务时间占比")
async def get_task_time_percent(user_id:int):
    try:
        assigned_tasks = await TaskAssignment.filter(assigned_to=user_id).prefetch_related('task')
        Idle, moderate, critical = 0, 0, 0
        for assigned_task in assigned_tasks:
            time_difference = (assigned_task.task.deadline - datetime.now().date()).days
            if time_difference > 15:
                Idle += 1
            elif time_difference > 0:
                moderate += 1
            else:
                critical += 1

        return {
            "code": "200",
            "data": {
                "Idle": Idle,
                "moderate": moderate,
                "critical": critical
            }
        }
    except DoesNotExist:
        return {
            "code": "0",
            "msg": "未找到数据"
        }
