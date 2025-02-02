# app/notifications.py
import requests

# Asegúrate de usar los valores correctos para tu aplicación OneSignal.
ONESIGNAL_APP_ID = "dc17cf54-a-b30a-bf30f60cc265" 
ONESIGNAL_API_KEY = "os_v2_app_3ql46vfo4jaizmykx4ypmf3xw5fvnna7aofq5abtttljjffhutfmuwjrk66ya"  # Se corrigió la comilla y se definió correctamente la cadena

def send_push_notification(task_id: int):    
    url = "https://onesignal.com/api/v1/notifications"
    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "included_segments": ["All"],
        "contents": {"en": f"Tarea {task_id} completada"}
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {ONESIGNAL_API_KEY}"  # Se agregó un espacio luego de "Basic" si es necesario: "Basic {ONESIGNAL_API_KEY}"
    }
    response = requests.post(url, json=payload, headers=headers)
    # Imprime información para depuración
    print("Status Code:", response.status_code)
    print("Response:", response.text)
    return response.json()