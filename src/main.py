from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import redis
from json import JSONDecodeError

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
    name: str = None
    description: str = None
    price: float = None
    tax: float = None


items_storage = []

def save_item(item_data):
    items_storage.append(item_data)

@app.post("/items/")
async def create_items(items: list[Item]):
    try:
        r.incr("hits")

        timestamp = datetime.now().isoformat()

        items_data = []
        for item in items:
            item_data = item.dict()
            item_data["timestamp"] = timestamp
            items_data.append(item_data)
        
            save_item(item_data)

        return items_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/items/")
async def get_items():
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

@app.get("/items/")
async def sorted():
    global items_storage
    for item in items_storage:
        item["price"]

# def clear_list():
#     items_storage = []