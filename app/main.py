# app/main.py
from fastapi import FastAPI, BackgroundTasks
from app.task import process_task

app = FastAPI()

#endpints
@app.post("/tasks/{task_id}")
def create_task(task_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_task, task_id)
    return {"message": "Tarea en progreso", "task_id": task_id}

@app.get("/")
def test_api():
    return {
        "Activo": "Funcionando correctamente!"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
