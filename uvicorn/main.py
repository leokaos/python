import uvicorn
import uuid

from fastapi import FastAPI, HTTPException
from item import Item

items = {}

items['a43c01ea-8ff0-4d7c-8fce-09cbbdb13f11'] = Item(id="a43c01ea-8ff0-4d7c-8fce-09cbbdb13f11", title="churros1", timestamp="2024-02-17T20:03:08.981966")
items['9ee5b76b-c5a5-4885-96c5-196c748d7202'] = Item(id="9ee5b76b-c5a5-4885-96c5-196c748d7202", title="churros2", timestamp="2024-02-17T20:03:08.981966")
items['4ef2536b-7f47-4d42-b5fa-979209b6e540'] = Item(id="4ef2536b-7f47-4d42-b5fa-979209b6e540", title="churros3", timestamp="2024-02-17T20:03:08.981966")


app = FastAPI()


@app.get("/items")
async def read_items():
    return list(items.values())


@app.get("/items/{id}")
async def read_items(id: str):

    check_exist_or_raise(id)

    return items[id]


@app.post("/items", status_code=201)
async def create_item(item: Item):

    item.id = uuid.uuid4()

    items[item.id] = item

    return item


@app.put("/items/{id}")
async def update_item(id: str, item: Item):

    check_exist_or_raise(id)

    inner_item = items[id]

    inner_item.title = item.title
    inner_item.timestamp = item.timestamp
    inner_item.description = item.description

    return item


@app.delete("/items/{id}", status_code=204)
async def delete_item(id: str):

    check_exist_or_raise(id)

    items.pop(id)


def check_exist_or_raise(id: str):

    if id not in items:
        raise HTTPException(status_code=404, detail="Item not found")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=1)
