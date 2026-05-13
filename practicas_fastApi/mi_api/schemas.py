from pydantic import BaseModel

# Esquemas Base (Lo que se necesita para crear)
class TagBase(BaseModel):
    nombre: str
    class Config: orm_mode = True

class ItemBase(BaseModel):
    nombre: str
    precio: float
    class Config: orm_mode = True

# Esquemas de Respuesta (Lo que el usuario verá, incluyendo relaciones)
class ItemDetalle(ItemBase):
    id: int
    categoria: str | None = None # Solo mostraremos el nombre de la categoría
    tags: list[TagBase] = []     # Lista de objetos Tag