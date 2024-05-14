from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `task_user`;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE `task_user` (
    `task_id` INT NOT NULL REFERENCES `task` (`id`) ON DELETE CASCADE,
    `user_id` INT NOT NULL REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""
