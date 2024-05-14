from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `task` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `description` LONGTEXT NOT NULL,
    `status` VARCHAR(20) NOT NULL,
    `progress` INT NOT NULL,
    `deadline` DATE NOT NULL,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `reason_for_progress_change` LONGTEXT NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(50) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `role` INT NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `taskassignment` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `assignment_date` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `assigned_to_id` INT NOT NULL,
    `task_id` INT NOT NULL,
    CONSTRAINT `fk_taskassi_user_11060ee6` FOREIGN KEY (`assigned_to_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_taskassi_task_7e02dc18` FOREIGN KEY (`task_id`) REFERENCES `task` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `task_user` (
    `task_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    FOREIGN KEY (`task_id`) REFERENCES `task` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
