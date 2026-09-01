import sqlalchemy as db 
from sqlalchemy.orm import declarative_base , sessionmaker
from pwdlib import PasswordHash




# Configurar banco de dados
Engine = db.create_engine("sqlite:///Dados.db")
Base = declarative_base()
TempSessao = sessionmaker(Engine)
Sessao = TempSessao()
SenhaHash = PasswordHash.recommended()
  
# Criar Tabelas
class Usuario(Base):
    __tablename__="Usuarios"
    
    Id_usuario = db.Column(db.Integer , primary_key=True , autoincrement=True)
    Nome = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    Senha = db.Column(db.String(255), nullable=False)

    
    @classmethod
    def Contrutor(Cs ,Nome ,Email ,senha ):
        
        Hash = SenhaHash.hash(senha)
    
        Valores = Cs(Nome=Nome ,Email=Email , Senha=Hash)
        Sessao.add(Valores)
        Sessao.commit()
        Sessao.close()

class Tarefa(Base):
    __tablename__= "Tarefas"
    
    Id =  db.Column(db.Integer, primary_key= True , autoincrement= True )
    Id_Usuario = db.Column(db.Integer , db.ForeignKey(Usuario.Id_usuario), nullable=False)
    Titulo = db.Column(db.String(100), nullable=  False)
    Descricao = db.Column (db.Text , nullable=False)
    Completo = db.Column(db.Boolean , default= False)
    
    @classmethod
    def Contrutor(Cs ,Id_Usuario, Titulo , Descricao , Completo):
        Valores = Cs( Id_Usuario=Id_Usuario,Titulo=Titulo ,Descricao=Descricao ,Completo=Completo)
        Sessao.add(Valores)
        Sessao.commit()
        Sessao.close()
    

#Gerar o banco 
Base.metadata.create_all(Engine)


        
        

