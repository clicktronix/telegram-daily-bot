"""Task manager"""
from db import Database
from config import Config


class TaskManager:
    """Task manager class"""

    def __init__(self):
        self.database = Database(Config)
        self.database.connect()

    def insert_chat_id(self, chat_id):
        """Insert chat id to db"""
        self.database.update_rows(
            self.database.commands["insert_chat_id"], [chat_id],
        )

    def get_tasks(self, chat_id):
        """Get a list of uncompleted tasks"""
        done_task_ids = self.database.select_rows(
            self.database.commands["select_done_task_ids"], [chat_id]
        )
        if not all(done_task_ids[0]):
            tasks = self.database.select_rows(self.database.commands["select_tasks"])
        else:
            tasks = self.database.select_rows(
                self.database.commands["filter_tasks"], [done_task_ids[0]],
            )
        if len(tasks) == 0:
            self.database.clear_done_ids(chat_id)
            tasks = self.database.select_rows(self.database.commands["select_tasks"])
        return tasks

    def insert_done_task_id(self, task_id):
        """Add the id of the completed task to the db"""
        self.database.update_rows(
            self.database.commands["insert_done_task_id"], [task_id],
        )
