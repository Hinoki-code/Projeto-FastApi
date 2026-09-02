import fastapi
from fastapi.security import OAuth2PasswordBearer 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from pwdlib import PasswordHash 
from pydantic import BaseModel
from typing import Optional
import db
from datetime import datetime , timedelta
import jwt 


""" Comando para rodar abrindo um server: uvicorn Main:app --reload """  

# Autentificação de dados recebidos com pydentic


class Task(BaseModel):
    title: str
    description: Optional[str] =None
    completed: bool=False
    
class User(BaseModel):
    Nome: str
    Email: str
    Senha: str

class UserLogin(BaseModel):
    Email:str
    Senha:str
    
         
ChaveSecreta = "ChaveQualquerAprendendoJWT"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SenhaHash = PasswordHash.recommended()

app = fastapi.FastAPI()


async def ObterUsuarioAtual(token:str = fastapi.Depends(oauth2_scheme)):
   infoDecript=jwt.decode(token,ChaveSecreta, algorithms=["HS256"])
   Id_Usuario= infoDecript.get("Usuario")
   return Id_Usuario

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


  
# Rotas para servir as páginas HTML automaticamente pelo Uvicorn
@app.get("/")
def serve_login():
    return FileResponse("login.html")

@app.get("/register")
def serve_register():
    return FileResponse("register.html")

@app.get("/dashboard")
def serve_dashboard():
    return FileResponse("dashboard.html")


# Login e registro de dados 
@app.post("/api/login")
def Login(Login:UserLogin , sessao = fastapi.Depends(db.ConexaoBanco)):
    
    info = sessao.query(db.Usuario).filter_by(Email = Login.Email).first()

    
    if info is None:
        raise fastapi.HTTPException(status_code=404 , detail="Email ou Senha invalida")
    
    elif not SenhaHash.verify(Login.Senha , info.Senha):
        raise fastapi.HTTPException(status_code=404 , detail="Email ou Senha invalida")
        
    else:
        token = jwt.encode(
        {"Usuario":info.Id_usuario , "exp": datetime.utcnow() + timedelta(minutes=30)},
        ChaveSecreta , algorithm="HS256" )
        
        return {"access_token": token}



@app.post("/UserRegister")
def Registrar(user:User):
    db.Usuario.Contrutor(user.Nome , user.Email , senha=user.Senha)  
    return "Registrado com sucesso"


#________________________________________________________________________________________________________________________________________

# Rotas


@app.post("/tasks")
async def Create_tasks(task:Task , Id_Usuario:int = fastapi.Depends(ObterUsuarioAtual)):
    db.Tarefa.Contrutor(Id_Usuario , task.title , task.description , task.completed)
    return task
    


@app.get("/tasks/All")
async def get_All(Id_Usuario:int = fastapi.Depends(ObterUsuarioAtual) , sessao = fastapi.Depends(db.ConexaoBanco)):
    info = sessao.query(db.Tarefa).filter_by(Id_Usuario=Id_Usuario).all()
    return info

    
@app.put("/tasks/{task_id}/Update")
async def Update_task(task_id:int ,task:Task , Id_Usuario:int = fastapi.Depends(ObterUsuarioAtual) , sessao = fastapi.Depends(db.ConexaoBanco)):
       info = sessao.query(db.Tarefa).filter_by(Id_Usuario=Id_Usuario,Id = task_id).first()
       info.Titulo = task.title
       info.Descricao = task.description
       info.Completo = task.completed
      
       sessao.add(info)
       sessao.commit()
       
       return task
   
   
@app.delete("/tasks/{task_id}/Delete")
async def Delet_task(task_id:int, Id_Usuario:int = fastapi.Depends(ObterUsuarioAtual), sessao = fastapi.Depends(db.ConexaoBanco)):
    info = sessao.query(db.Tarefa).filter_by( Id_Usuario=Id_Usuario , Id = task_id).first()
    sessao.delete(info)
    sessao.commit()
    
    return "Id deletado do banco de dados"



