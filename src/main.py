from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import redis
from pydantic import constr, conint, Field
from json import JSONDecodeError
from typing import Annotated
from typing import Optional

app = FastAPI()

r = redis.Redis(host="redis", port=6379)

@app.get("/")
def read_root():
    return {"Hello": "Worldasspiss88888"}

@app.get("/hits")
def read_root():
    r.incr("hits")
    return {"number of hits": r.get("hits")}




class Item(BaseModel):
    name: str = Field(max_length=10, pattern=r'^[a-zA-Z]+$')
    description: str = Field(max_length=50, pattern=r'^[a-zA-Z]+$')
    price: float = Field(conint(gt=0))
    tax: Optional[float] = None



items_storage = []


def save_item(item_data):
    items_storage.append(item_data)

@app.post("/items/")
async def create_items(items: list[Item]):
    print(items_storage)
    try:
        r.incr("hits")

        timestamp = datetime.now().isoformat()

        items_data = []
        for item in items:
            item_data = item.model_dump()
            item_data["timestamp"] = timestamp
            items_data.append(item_data)
        
            save_item(item_data)

        return items_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/items/")
async def get_items():
    print(items_storage)
    return {"items": items_storage}


@app.post("/items/clear")
async def clear_items():
    global items_storage
    items_storage = []

@app.post("/items/clear_prices")
async def clear_prices():
    global items_storage
    for item in items_storage:
        item["price"] = None

@app.get("/items/sorted")
async def sorted():
    global items_storage
    for item in items_storage:
        item["price"]
