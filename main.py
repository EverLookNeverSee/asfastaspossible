from dataclasses import dataclass
from fastapi import FastAPI, Response, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel


# Defining the api object
app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


@app.get("/")
def root():
    return Response(status_code=200, content="The server is running.")


@app.get("/about")
def about():
    return Response(status_code=200, content="This is about page.")


inventory = {}


@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The item's id", gt=0)):
    if item_id in inventory:
        return inventory[item_id]
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@app.get("/get-by-name/{item_id}")
def get_by_name(*, item_id: int, name: Optional[str] = None, version: int):
    if version:
        for item_id in inventory:
            if inventory[item_id].name == name:
                return inventory[item_id]
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item name not found")


@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item already exists")
    else:
        inventory[item_id] = item
        return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if item.name:
        inventory[item_id].name = item.name
    if item.price:
        inventory[item_id].price = item.price
    if item.brand:
        inventory[item_id].brand = item.brand
    return inventory[item_id]


@app.delete("/delete-item/{item_id}")
def delete_item(item_id: int = Query(..., description="The item's id", gt=0)):
    if item_id not in inventory:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    del inventory[item_id]
    return {"message": "Item deleted"}
