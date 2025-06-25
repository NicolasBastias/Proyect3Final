from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a MySQL en phpMyAdmin
DATABASE_URL = "mysql+mysqlconnector://root:@localhost/orm_clientes"


# Crear el motor de conexión
engine = create_engine(DATABASE_URL, echo=True)

# Crear una base de datos declarativa
Base = declarative_base()

# Crear una clase Session que gestiona la interacción con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener la sesión de la base de datos
def get_session():
    return SessionLocal()

