from sqlalchemy.orm import Session
from models import Ingrediente

class IngredienteCRUD:

    @staticmethod
    def crear_ingrediente(db: Session, nombre: str, tipo: str, cantidad: int, unidad_de_medida: str) -> Ingrediente:
        ingrediente_existente = db.query(Ingrediente).filter(Ingrediente.nombre == nombre, Ingrediente.tipo == tipo).first()
        if ingrediente_existente:
            return None
        nuevo_ingrediente = Ingrediente(nombre=nombre, tipo=tipo, cantidad=cantidad, unidad_de_medida=unidad_de_medida)
        db.add(nuevo_ingrediente)
        db.commit()
        db.refresh(nuevo_ingrediente)
        return nuevo_ingrediente

    @staticmethod
    def leer_ingredientes(db: Session):
        return db.query(Ingrediente).all()

    @staticmethod
    def actualizar_ingrediente(db: Session, id_ingrediente: int, nombre: str, tipo: str, cantidad: int, unidad_de_medida: str) -> Ingrediente:
        ingrediente = db.query(Ingrediente).filter(Ingrediente.id_ingrediente == id_ingrediente).first()
        if ingrediente:
            ingrediente.nombre = nombre
            ingrediente.tipo = tipo
            ingrediente.cantidad = cantidad
            ingrediente.unidad_de_medida = unidad_de_medida
            db.commit()
            db.refresh(ingrediente)
            return ingrediente
        return None

    @staticmethod
    def borrar_ingrediente(db: Session, id_ingrediente: int):
        ingrediente = db.query(Ingrediente).filter(Ingrediente.id_ingrediente == id_ingrediente).first()
        if ingrediente:
            db.delete(ingrediente)
            db.commit()
            return True
        return False
