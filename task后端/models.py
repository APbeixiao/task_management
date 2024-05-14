from tortoise import fields
from tortoise.models import Model
from tortoise import fields
from tortoise.models import Model

class User(Model):
    # 用户模型，用于表示系统中的用户
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=False)  # 用户名
    nickname = fields.CharField(max_length=50, unique=False)
    password = fields.CharField(max_length=255)  # 密码
    role = fields.IntField()  # 角色：1 - 执行者，2 - 两者


# Task 模型定义保持不变
class Task(Model):
    # 任务模型，用于表示系统中的任务
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)  # 任务名称
    description = fields.TextField()  # 任务描述
    status = fields.CharField(max_length=20)  # 任务状态
    progress = fields.IntField()  # 进度百分比
    deadline = fields.DateField()  # 截止日期
    created_at = fields.DatetimeField(auto_now_add=True)  # 创建日期
    reason_for_progress_change = fields.TextField()  # 项目进度变更原因
    created_user = fields.ForeignKeyField('models.User', related_name='created_user')

class TaskAssignment(Model):
    # 任务分配信息模型，用于记录任务的分配信息
    id = fields.IntField(pk=True)
    task = fields.ForeignKeyField('models.Task', related_name='task')  # 关联任务
    assigned_to = fields.ForeignKeyField('models.User', related_name='assigned_to')  # 分配给
    assignment_date = fields.DatetimeField(auto_now_add=True)  # 分配日期

class TaskStatusChange(Model):
    # 任务状态变更记录模型，用于记录任务状态的变更信息
    id = fields.IntField(pk=True)
    task = fields.ForeignKeyField('models.Task', related_name='status_changes')  # 关联任务
    changed_by = fields.ForeignKeyField('models.User', related_name='changed_by')  # 变更人员
    change_date = fields.DatetimeField(auto_now_add=True)  # 变更日期
    new_status = fields.CharField(max_length=20)  # 新状态
    change_reason = fields.TextField()  # 变更原因
