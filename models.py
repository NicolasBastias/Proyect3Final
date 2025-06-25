from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Tabla intermedia para la relación muchos a muchos entre Menú e ingrediente
menu_ingrediente = Table('menu_ingrediente', Base.metadata,
    Column('menu_id', Integer, ForeignKey('menu.id_menu', ondelete='CASCADE'), primary_key=True),
    Column('ingrediente_id', Integer, ForeignKey('ingrediente.id_ingrediente', ondelete='CASCADE'), primary_key=True)
)

# Tabla intermedia para la relación muchos a muchos entre Pedido y Menú
pedido_menu = Table('pedido_menu', Base.metadata,
    Column('pedido_id', Integer, ForeignKey('pedidos.id', ondelete='CASCADE'), primary_key=True),
    Column('menu_id', Integer, ForeignKey('menu.id_menu', ondelete='CASCADE'), primary_key=True)
)

class Cliente(Base):
    __tablename__ = 'clientes'
    
    email = Column(String(100), primary_key=True)  # Especificamos el tamaño del String
    nombre = Column(String(100), nullable=False)   # Especificamos el tamaño del String

    # Relación de uno a muchos con Pedidos
    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")

class Pedido(Base):
    __tablename__ = 'pedidos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(255), nullable=False)  # Especificamos el tamaño de la columna
    
    # Relación muchos a muchos con Menu
    menu_ids = relationship("Menu", secondary=pedido_menu, back_populates="pedidos")

    # Clave foránea que hace referencia a la tabla Cliente
    cliente_email = Column(String(100), ForeignKey('clientes.email', onupdate="CASCADE"), nullable=False)
    
    # Relación inversa con Cliente
    cliente = relationship("Cliente", back_populates="pedidos")

class Ingrediente(Base):
    __tablename__ = 'ingrediente'

    id_ingrediente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)  # Especificamos el tamaño del String
    tipo = Column(String(100), nullable=False)    # Especificamos el tamaño del String
    cantidad = Column(Integer, nullable=False)
    unidad_de_medida = Column(String(50), nullable=False)  # Especificamos el tamaño del String

    # Relación muchos a muchos con Menu
    menus = relationship('Menu', secondary=menu_ingrediente, back_populates='ingrediente')

class Menu(Base):
    __tablename__ = 'menu'

    id_menu = Column(Integer, primary_key=True, autoincrement=True)
    nombre_menu = Column(String(100), nullable=False)  # Especificamos el tamaño del String
    descripcion = Column(String(255), nullable=True)    # Especificamos el tamaño del String

    # Relación muchos a muchos con ingrediente
    ingrediente = relationship('Ingrediente', secondary=menu_ingrediente, back_populates='menus')

    # Relación muchos a muchos con Pedidos
    pedidos = relationship('Pedido', secondary=pedido_menu, back_populates='menu_ids')
