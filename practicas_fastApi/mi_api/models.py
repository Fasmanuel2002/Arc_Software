from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base
item_tag_association = Table(
    "item_tag",
    Base.metadata,
    Column("item_id", ForeignKey("items.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True)
    
    # relationship: Permite acceder a los items desde la categoría (ej: mi_cat.items)
    items = relationship("Item", back_populates="categoria")

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Float)
    
    # ForeignKey: El "ancla" real en la DB que conecta con Categoría
    categoria_id = Column(Integer, ForeignKey("categorias.id"))

    # Relaciones de Python
    categoria = relationship("Categoria", back_populates="items")
    tags = relationship("Tag", secondary=item_tag_association, back_populates="items")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True)
    
    items = relationship("Item", secondary=item_tag_association, back_populates="tags")