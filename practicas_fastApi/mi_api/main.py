from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

# Modelo de datos
class Item(BaseModel):
    nombre: str
    descripcion: str | None = None
    precio: float
    en_stock: bool = True

# GET
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, "mensaje": "Mostrando información del item"}

# POST
@app.post("/items/")
def create_item(item: Item):
    return {"mensaje": "Item creado exitosamente", "item": item}

# PUT
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"mensaje": f"Item {item_id} actualizado", "item": item}

# DELETE
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"mensaje": f"Item {item_id} eliminado"}