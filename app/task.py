# app/task.py
import time
from app.notifications import send_push_notification

def process_task(task_id: int):
    #tarea intensiva
    time.sleep(5)
    print(f"Tarea {task_id} Completada Si o Si")
    send_push_notification(task_id)
