from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `task` ADD `created_user_id` INT NOT NULL;
        ALTER TABLE `task` ADD CONSTRAINT `fk_task_user_3c31643f` FOREIGN KEY (`created_user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `task` DROP FOREIGN KEY `fk_task_user_3c31643f`;
        ALTER TABLE `task` DROP COLUMN `created_user_id`;"""
