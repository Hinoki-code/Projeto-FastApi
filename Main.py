import fastapi
from pydantic import BaseModel
from typing import Optional
import sqlite3

""" Comando para rodar abrindo um server: uvicorn Main:app --reload """  

"""Criação banco de dados"""
tasks_db=[]   

conexao =sqlite3.connect("Banco.db")
cursor = conexao.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS Tarefas ( 
               id  INTEGER PRIMARY KEY AUTOINCREMENT, 
               title varchar(255) NOT NULL,
               description TEXT,
               completed  BOOLEAN DEFAULT FALSE)""") 


"""Aqui começaFastAPI"""

app = fastapi.FastAPI()


class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] =None
    completed: bool=False
    
@app.get("/")
def root():
    return {"Message":"Meu FastApi esta funcionando"}


@app.post("/tasks")
async def Create_tasks(task:Task):
    cursor.execute("INSERT INTO Tarefas(title , description , completed) VALUES(? , ? ,?)", (task.title , task.description , task.completed))
    conexao.commit()

    return task
    
    
@app.get("/tasks/{task_id}")
async def Get_taskid(task_id:int):            #E obrigadotorio o uso da virgula para o python entender que e uma tupla e o FastApi precisa que seja uma tupla
    cursor.execute("SELECT * FROM Tarefas WHERE id = ?  ", (task_id,))

    Buscar = cursor.fetchone()
    if Buscar is None:
        raise fastapi.HTTPException(status_code=404 , detail="Tarefa não encontrada no banco de dados.")
    else:
        return Buscar
    
@app.put("/tasks/{task_id}/Update")
async def Update_task(task_id:int ,task:Task):
    cursor.execute("UPDATE Tarefas SET title= ?,description=?, completed=? WHERE id = ?" , (task.title , task.description , task.completed, task_id))
    
    if cursor.rowcount == 0:
        raise fastapi.HTTPException(status_code=404 , detail="Id inexistente no banco de dados.")
    else:
        conexao.commit()
        return task         


@app.delete("/tasks/{task_id}/Delete")
async def Delet_task(task_id:int):
    cursor.execute("DELETE FROM Tarefas WHERE id= ? ", (task_id,))
    if cursor.rowcount == 0:
        raise fastapi.HTTPException(status_code=404 , detail="Id Não encontrado para ser deletado")
    else:
        conexao.commit()
        return {"message":"Tarefa deletada do banco"}
