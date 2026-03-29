from fastapi import FastAPI as fp
app = fp()



@app.get("/")
@app.head("/")
def get():
    return {"condition":"ok"}

prods = [
    {"id":1, "name": "a", "price": 1000},
    {"id":2, "name": "b", "price": 300},
    {"id":3, "name": "c", "price": 170}
]

@app.get("/prods")
def getAll():
    return prods

@app.get("/prods/{id}")
def getOne(id: int):
    for p in prods:
        if p["id"] == id:
            return p
    return {"error": "product not found"}
