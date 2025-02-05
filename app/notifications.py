# app/notifications.py
import requests

# Api Key y App ID de OneSignal
ONESIGNAL_APP_ID = "dc17cf54-a-b30a-bf30f60cc265" 
ONESIGNAL_API_KEY = "os_v2_app_3ql46vfo4jaizmykx4ypmf3xw5fvnna7aofq5abtttljjffhutfmuwjrk66ya"  

def send_push_notification(task_id: int):    
    url = "https://onesignal.com/api/v1/notifications"
    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "included_segments": ["All"],
        "contents": {"en": f"Tarea {task_id} completada"}
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {ONESIGNAL_API_KEY}"
    }
    response = requests.post(url, json=payload, headers=headers)
    # Imprime información para depuración
    print("Status Code:", response.status_code)
    print("Response:", response.text)
    return response.json()