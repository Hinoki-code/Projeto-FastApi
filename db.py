import sqlalchemy as db 
from sqlalchemy.orm import declarative_base , sessionmaker

Engine = db.create_engine("sqlite:///Dados.db")
Base = declarative_base()
TempSessao = sessionmaker(Engine)
Sessao = TempSessao()


class Tarefa(Base):
    __tablename__= "Tarefas"
    
    Id =  db.Column(db.Integer, primary_key=  True , autoincrement= True )
    Titulo = db.Column(db.String(60), nullable=  False)
    Descricao = db.Column (db.Text , nullable=False)
    Completo = db.Column(db.Boolean , default= False)
    
    @classmethod
    def Contrutor(Cs , Titulo , Descricao , Completo):
        Valores = Cs(Titulo=Titulo ,Descricao=Descricao ,Completo=Completo)
        Sessao.add(Valores)
        Sessao.commit()
        Sessao.close()
    

Base.metadata.create_all(Engine)


        
        

