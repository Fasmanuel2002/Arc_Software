from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Item
from database import engine
from database import Base
from dependencies import get_db
from pydantic import BaseModel

from practicas_fastApi.mi_api import schemas
from practicas_fastApi.mi_api import models
from sqlalchemy.orm import selectinload

app = FastAPI()

class ItemCreate(BaseModel):
    nombre: str
    descripcion: str | None = None
    precio: float
    en_stock: bool = True

class ItemResponse(ItemCreate):
    id: int

    class Config:
        from_attributes = True

@app.post("/categorias/{cat_id}/items/", response_model=schemas.ItemDetalle)
async def crear_item(cat_id: int, item: schemas.ItemBase, db: AsyncSession = Depends(get_db)):
    nuevo_item = models.Item(**item.dict(), categoria_id=cat_id)
    db.add(nuevo_item)
    await db.commit()
    await db.refresh(nuevo_item)
    return nuevo_item

@app.post("/items/{item_id}/tags/{tag_id}")
async def asignar_tag(item_id: int, tag_id: int, db: AsyncSession = Depends(get_db)):
    # Cargamos el item incluyendo sus tags actuales
    res = await db.execute(
        select(models.Item).where(models.Item.id == item_id).options(selectinload(models.Item.tags))
    )
    item = res.scalar_one_or_none()
    
    res_tag = await db.execute(select(models.Tag).where(models.Tag.id == tag_id))
    tag = res_tag.scalar_one_or_none()

    if not item or not tag:
        raise HTTPException(status_code=404, detail="No encontrado")

    item.tags.append(tag) # SQLAlchemy gestiona la tabla 'item_tag'
    await db.commit()
    return {"mensaje": "Tag vinculado con éxito"}
@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item

@app.get("/items/", response_model=list[ItemResponse])
async def list_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item))
    return result.scalars().all()

@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: ItemCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    db_item = result.scalar_one_or_none()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    await db.commit()
    await db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    await db.delete(item)
    await db.commit()
    return {"mensaje": "Item eliminado"}