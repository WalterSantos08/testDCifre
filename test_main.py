from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from fastapi.testclient import TestClient
import pytest

# --------------------------------------------
# Configuração do Banco de Dados & Modelos
# --------------------------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # Banco em memória para testes
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo SQLAlchemy
class EmpresaDB(Base):
    __tablename__ = "empresas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cnpj = Column(String, unique=True, nullable=False)
    endereco = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telefone = Column(String, nullable=False)

# --------------------------------------------
# FastAPI & Dependências
# --------------------------------------------
app = FastAPI()

# Dependência de banco de dados
def get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------------------------
# Schemas Pydantic
# --------------------------------------------
class EmpresaCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nome: str
    cnpj: str
    endereco: str
    email: str
    telefone: str

class EmpresaResponse(EmpresaCreate):
    id: int

# --------------------------------------------
# Rotas
# --------------------------------------------
@app.post("/empresas/", response_model=EmpresaResponse)
def criar_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = EmpresaDB(**empresa.model_dump())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.get("/empresas/{empresa_id}", response_model=EmpresaResponse)
def obter_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(EmpresaDB).filter(EmpresaDB.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return empresa

# --------------------------------------------
# Testes
# --------------------------------------------
@pytest.fixture(scope="session")  # Criar um único banco para todos os testes
def client():
    with TestClient(app) as client:
        def override_get_db():
            db = TestingSessionLocal()
            Base.metadata.create_all(bind=engine)  # Garante que as tabelas são criadas
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db
        yield client
        app.dependency_overrides.clear()

# Teste de criação de empresa
def test_criar_empresa(client):
    response = client.post(
        "/empresas/",
        json={
            "nome": "Empresa Teste",
            "cnpj": "00.000.000/0001-00",
            "endereco": "Rua Teste, 123",
            "email": "teste@empresa.com",
            "telefone": "123456789"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Empresa Teste"
    assert "id" in data

# Teste de obtenção de empresa
def test_obter_empresa(client):
    criar_response = client.post(
        "/empresas/",
        json={
            "nome": "Empresa para Consulta",
            "cnpj": "99.999.999/0001-99",
            "endereco": "Rua Consulta, 456",
            "email": "consulta@empresa.com",
            "telefone": "987654321"
        },
    )
    empresa_id = criar_response.json()["id"]
    response = client.get(f"/empresas/{empresa_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == empresa_id
    assert data["cnpj"] == "99.999.999/0001-99"

# Para rodar os testes: pytest -v
