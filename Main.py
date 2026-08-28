import fastapi
from pydantic import BaseModel
from typing import Optional
import db

""" Comando para rodar abrindo um server: uvicorn Main:app --reload """  

app = fastapi.FastAPI()

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] =None
    completed: bool=False
    
@app.get("/")
def root():
    return {"Message":"Meu FastApi esta funcionando"}


@app.get("/tasks/All")
async def get_All():
    info = db.Sessao.query(db.Tarefa).all()
    return info

    
@app.get("/tasks/{task_id}")
async def Get_taskid(task_id:int):  
    info = db.Sessao.query(db.Tarefa).filter_by(Id = task_id).first()
    
    if info is None:
        raise fastapi.HTTPException(status_code=404 , detail="Tarefa não encontrada no banco de dados.")
    else:
        return info



@app.post("/tasks")
async def Create_tasks(task:Task):
    db.Tarefa.Contrutor(task.title , task.description , task.completed)
    return task
    
    
@app.put("/tasks/{task_id}/Update")
async def Update_task(task_id:int ,task:Task):
       info = db.Sessao.query(db.Tarefa).filter_by(Id = task_id).first()
    
       info.Titulo = task.title
       info.Descricao = task.description
       info.Completo = task.completed
      
       db.Sessao.add(info)
       db.Sessao.commit()
       
       return task
   
   
@app.delete("/tasks/{task_id}/Delete")
async def Delet_task(task_id:int):
    info = db.Sessao.query(db.Tarefa).filter_by(Id = task_id).first()
    db.Sessao.delete(info)
    db.Sessao.commit()
    
    return "Id deletado do banco de dados"
