from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import databases
import sqlalchemy

DATABASE_URL = "sqlite:///./tasks.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

tasks = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String, index=True),
    sqlalchemy.Column("description", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("completed", sqlalchemy.Boolean, default=False),
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

app = FastAPI()

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/tasks", response_model=List[Task])
async def read_tasks():
    query = tasks.select()
    return await database.fetch_all(query)

@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    query = tasks.insert().values(
        title=task.title, description=task.description, completed=task.completed
    )
    last_record_id = await database.execute(query)
    return {**task.dict(), "id": last_record_id}

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    query = tasks.update().where(tasks.c.id == task_id).values(
        title=task.title, description=task.description, completed=task.completed
    )
    await database.execute(query)
    return {**task.dict(), "id": task_id}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    query = tasks.delete().where(tasks.c.id == task_id)
    await database.execute(query)
    return {"message": "Task deleted"}
