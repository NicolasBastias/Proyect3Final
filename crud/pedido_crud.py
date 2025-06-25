from sqlalchemy.orm import Session
from models import Pedido, Cliente, Menu

class PedidoCRUD:

    @staticmethod
    def crear_pedido(db: Session, cliente_email: str, descripcion: str, menu_ids: list[int]) -> Pedido:
        cliente = db.query(Cliente).filter(Cliente.email == cliente_email).first()
        if not cliente:
            return None

        nuevo_pedido = Pedido(descripcion=descripcion, cliente_email=cliente_email)
        db.add(nuevo_pedido)
        db.commit()
        db.refresh(nuevo_pedido)

        # Asociar menús al pedido
        for id_menu in menu_ids:
            menu = db.query(Menu).filter(Menu.id_menu == id_menu).first()
            if menu:
                nuevo_pedido.menu_ids.append(menu)

        db.commit()
        db.refresh(nuevo_pedido)
        return nuevo_pedido


    @staticmethod
    def leer_pedidos(db: Session):
        return db.query(Pedido).all()

    @staticmethod
    def actualizar_pedido(db: Session, id_pedido: int, descripcion: str) -> Pedido:
        pedido = db.query(Pedido).filter(Pedido.id == id_pedido).first()
        if pedido:
            pedido.descripcion = descripcion
            db.commit()
            db.refresh(pedido)
            return pedido
        return None

    @staticmethod
    def borrar_pedido(db: Session, id_pedido: int):
        pedido = db.query(Pedido).filter(Pedido.id == id_pedido).first()
        if pedido:
            db.delete(pedido)
            db.commit()
            return True
        return False
