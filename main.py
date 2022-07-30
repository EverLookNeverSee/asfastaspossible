from fastapi import FastAPI, Response

# Defining the api object
app = FastAPI()


@app.get("/")
def root():
    return Response(status_code=200, content="The server is running.")


@app.get("/about")
def about():
    return {"message": "About page"}


inventory = {
    1: {"name": "banana", "price": "$1.00"},
    2: {"name": "apple", "price": "$2.00"},
    3: {"name": "orange", "price": "$3.00"},
    4: {"name": "pear", "price": "$4.00"},
    5: {"name": "grape", "price": "$5.00"},
}


@app.get("/get-item/{item_id}")
def get_item(item_id: int):
    if item_id in inventory:
        return inventory[item_id]
    else:
        return {"message": "Item not found"}
