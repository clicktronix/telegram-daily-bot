UPDATE chats
SET done_task_ids = null
WHERE chats.id = (%s);