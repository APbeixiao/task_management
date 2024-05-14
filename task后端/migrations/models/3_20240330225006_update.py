from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `taskstatuschange` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `change_date` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `new_status` VARCHAR(20) NOT NULL,
    `change_reason` LONGTEXT NOT NULL,
    `changed_by_id` INT NOT NULL,
    `task_id` INT NOT NULL,
    CONSTRAINT `fk_taskstat_user_b01f2463` FOREIGN KEY (`changed_by_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_taskstat_task_018be096` FOREIGN KEY (`task_id`) REFERENCES `task` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `taskstatuschange`;"""
