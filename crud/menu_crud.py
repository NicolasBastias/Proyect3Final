from sqlalchemy.orm import Session, selectinload
from models import Menu, Ingrediente, menu_ingrediente

class MenuCRUD:

    @staticmethod
    def crear_menu(db: Session, nombre_menu: str, descripcion: str) -> Menu:
        menu_existente = db.query(Menu).filter(Menu.nombre_menu == nombre_menu).first()
        if menu_existente:
            return None
        nuevo_menu = Menu(nombre_menu=nombre_menu, descripcion=descripcion)
        db.add(nuevo_menu)
        db.commit()
        db.refresh(nuevo_menu)
        return nuevo_menu

    @staticmethod
    def leer_menus(db: Session):
        return db.query(Menu).all()

    @staticmethod
    def actualizar_menu(db: Session, id_menu: int, nombre_menu: str, descripcion: str) -> Menu:
        menu = db.query(Menu).filter(Menu.id_menu == id_menu).first()
        if menu:
            menu.nombre_menu = nombre_menu
            menu.descripcion = descripcion
            db.commit()
            db.refresh(menu)
            return menu
        return None

    def obtener_todos_menus(db: Session):
        """
        Devuelve una lista de objetos Menu, con la relación
        `ingrediente` ya cargada para evitar DetachedInstanceError.
        """
        return (
            db.query(Menu)
              .options(selectinload(Menu.ingrediente))  # carga los ingredientes de golpe
              .all()
        )

    @staticmethod
    def borrar_menu(db: Session, id_menu: int):
        menu = db.query(Menu).filter(Menu.id_menu == id_menu).first()
        if menu:
            db.delete(menu)
            db.commit()
            return True
        return False

    @staticmethod
    def agregar_ingrediente_a_menu(db: Session, id_menu: int, id_ingrediente: int):
        menu = db.query(Menu).filter(Menu.id_menu == id_menu).first()
        ingrediente = db.query(Ingrediente).filter(Ingrediente.id_ingrediente == id_ingrediente).first()
        
        if not menu or not ingrediente:
            return None
        
        # Verificar si el ingrediente ya está asociado al menú
        if db.query(menu_ingrediente).filter(menu_ingrediente.c.menu_id == id_menu, menu_ingrediente.c.ingrediente_id == id_ingrediente).first():
            return None

        # Asociar el ingrediente al menú
        menu.ingredientes.append(ingrediente)
        db.commit()
        db.refresh(menu)
        return menu
    
    def crear_menu_con_ingredientes(db: Session, nombre_menu: str, ingredientes: list):
            if db.query(Menu).filter_by(nombre_menu=nombre_menu).first():
                return None                       # evita duplicados

            nuevo = Menu(nombre_menu=nombre_menu)
            nuevo.ingrediente.extend(ingredientes)
            db.add(nuevo)
            db.commit()                           # ← guarda en BD
            db.refresh(nuevo)                     # ← trae id y relación completas
            return nuevo

    @staticmethod
    def obtener_todos_menus(db: Session):
        return (
            db.query(Menu)
            .options(selectinload(Menu.ingrediente))
            .order_by(Menu.nombre_menu.asc())
            .all()
        )
