from datetime import datetime, date

from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from typing import List, Union
from pydantic import BaseModel
from models import *
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import in_transaction

taskmanage_router = APIRouter()

@taskmanage_router.get("/gettaskmanage",description="获取传入值的任务的所有修改信息")
async def get_taskmanage_by_assigned_to(assigned_to: int):
    task_assignments = await TaskAssignment.filter(assigned_to_id=assigned_to).values_list('task_id', flat=True)

    # 根据获取到的 task_id 值在 Task 表中查询所有数据
    tasks = await Task.filter(id__in=task_assignments)

    # 创建一个空列表用于存储任务及其状态
    task_list = []

    for task in tasks:
        # 查询任务的所有状态
        states = await TaskStatusChange.filter(task_id=task.id).order_by('-change_date').prefetch_related('changed_by')

        # 创建一个列表用于存储处理后的状态
        processed_states = []

        for state in states:
            # 直接访问changed_by字段获取关联的用户对象
            user = state.changed_by
            # 创建一个新的状态字典，替换changed_by为user的username
            processed_state = {
                'id': state.id,
                'change_date': state.change_date,
                'change_reason': state.change_reason,
                'new_status': state.new_status,
                'changed_by': user.nickname,  # 使用user对象的username属性
                # 其他需要的字段...
            }
            # 将处理后的状态添加到列表中
            processed_states.append(processed_state)

        # 创建一个字典，将任务和其所有处理后的状态存储为键值对
        task_with_states = {
            'task': task,
            'states': processed_states
        }

        # 将任务及其状态添加到列表中
        task_list.append(task_with_states)

    if task_list:
        return {
            "code": "200",
            "data": task_list
        }

    else:
        return {
            "code": "0",
            "msg": "未找到数据"
        }

class AddtaskmanageModel(BaseModel):
    task_id: int
    change_reason: str
    new_status: int
    changed_by: int

@taskmanage_router.post("/addtaskmanage",description="添加任务管理信息")
async def add_taskmanage(data:AddtaskmanageModel):
    try:
        task = await Task.get(id=data.task_id)
        user = await User.get(id=data.changed_by)
        await Task.filter(id=data.task_id).update(progress=data.new_status)
        task_status_change = await TaskStatusChange.create(
            task=task,
            change_reason=data.change_reason,
            new_status=data.new_status,
            changed_by=user
        )

        return {
            "code": "200",
            "msg": "添加成功",
            "data": task_status_change
        }
    except DoesNotExist:
       return {
           "code": "0",
           "msg": "未找到数据"
       }
