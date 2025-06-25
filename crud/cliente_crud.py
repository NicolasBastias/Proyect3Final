from sqlalchemy.orm import Session
from models import Cliente

class ClienteCRUD:
    
    @staticmethod
    def obtener_todos_clientes(db: Session):
        """Obtiene todos los clientes de la base de datos."""
        return db.query(Cliente).all()

    @staticmethod
    def crear_cliente(db: Session, nombre: str, email: str) -> Cliente:
        cliente_existente = db.query(Cliente).filter(Cliente.email == email).first()
        if cliente_existente:
            return None
        nuevo_cliente = Cliente(nombre=nombre, email=email)
        db.add(nuevo_cliente)
        db.commit()
        db.refresh(nuevo_cliente)
        return nuevo_cliente

    @staticmethod
    def leer_clientes(db: Session):
        return db.query(Cliente).all()

    @staticmethod
    def actualizar_cliente(db: Session, email: str, nombre: str) -> Cliente:
        cliente = db.query(Cliente).filter(Cliente.email == email).first()
        if cliente:
            cliente.nombre = nombre

            db.commit()
            db.refresh(cliente)
            return cliente
        return None

    @staticmethod
    def borrar_cliente(db: Session, email: str):
        cliente = db.query(Cliente).filter(Cliente.email == email).first()
        if cliente:
            db.delete(cliente)
            db.commit()
            return True
        return False
    
    @staticmethod
    def obtener_cliente_por_email(db: Session, email: str) -> Cliente:
        return db.query(Cliente).filter(Cliente.email == email).first()

