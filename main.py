from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:123456@localhost:5432/minha_empresa_db")

# Configuração do Banco de Dados
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelos SQLAlchemy
class Empresa(Base):
    __tablename__ = "empresas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cnpj = Column(String, unique=True, nullable=False)
    endereco = Column(String)
    email = Column(String, nullable=False)
    telefone = Column(String)
    obrigacoes = relationship("ObrigacaoAcessoria", back_populates="empresa")

class ObrigacaoAcessoria(Base):
    __tablename__ = "obrigacoes_acessorias"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    periodicidade = Column(String, nullable=False)
    empresa_id = Column(Integer, ForeignKey("empresas.id"))
    empresa = relationship("Empresa", back_populates="obrigacoes")

# Schemas Pydantic
class EmpresaSchema(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    email: EmailStr
    telefone: str
    
    class Config:
        from_attributes = True  # Usando from_attributes em vez de orm_mode

class EmpresaResponseSchema(EmpresaSchema):
    id: int

    class Config:
        from_attributes = True  # Usando from_attributes em vez de orm_mode

class ObrigacaoAcessoriaSchema(BaseModel):
    nome: str
    periodicidade: str
    empresa_id: int

    class Config:
        from_attributes = True  # Usando from_attributes em vez de orm_mode

class ObrigacaoAcessoriaResponseSchema(ObrigacaoAcessoriaSchema):
    id: int

    class Config:
        from_attributes = True  # Usando from_attributes em vez de orm_mode

# Dependência do Banco de Dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inicializar FastAPI
app = FastAPI()

# Criar Tabelas
Base.metadata.create_all(bind=engine)

# Rotas CRUD para Empresa
@app.post("/empresas/", response_model=EmpresaResponseSchema)
def criar_empresa(empresa: EmpresaSchema, db: Session = Depends(get_db)):
    db_empresa = Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.get("/empresas/{empresa_id}", response_model=EmpresaResponseSchema)
def obter_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return empresa

# Rotas CRUD para ObrigacaoAcessoria
@app.post("/obrigacoes/", response_model=ObrigacaoAcessoriaResponseSchema)
def criar_obrigacao(obrigacao: ObrigacaoAcessoriaSchema, db: Session = Depends(get_db)):
    db_obrigacao = ObrigacaoAcessoria(**obrigacao.dict())
    db.add(db_obrigacao)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

@app.get("/obrigacoes/{obrigacao_id}", response_model=ObrigacaoAcessoriaResponseSchema)
def obter_obrigacao(obrigacao_id: int, db: Session = Depends(get_db)):
    obrigacao = db.query(ObrigacaoAcessoria).filter(ObrigacaoAcessoria.id == obrigacao_id).first()
    if not obrigacao:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada")
    return obrigacao
