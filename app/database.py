from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path
from os import getenv
from dotenv import load_dotenv
 
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()
 
# Inicialização (criação do SCHEMA no banco de dados)
SERVER_URL = f"mysql+pymysql://{getenv('DB_USER')}:{getenv('DB_PSWD')}@{getenv('DB_HOST')}"
engine_server = create_engine(SERVER_URL)
 
with engine_server.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {getenv('DB_NAME')}"))
    conn.commit()
 
# Conexão com o banco já criado
DATABASE_URL = f"mysql+pymysql://{getenv('DB_USER')}:{getenv('DB_PSWD')}@{getenv('DB_HOST')}/{getenv('DB_NAME')}"
 
# Criar um "motor" que fará o gerenciamento da conexão
engine = create_engine(DATABASE_URL)
 
# Criando uma sessão para executar os comandos SQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
# Cria um objeto da base dados manipulável pelo Python
Base = declarative_base()
 
# Injeção de dependência: injeta a sessão do banco de dados
# em cada rota que for criada
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()