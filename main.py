from fastapi import FastAPI
from routers import user, objects

app = FastAPI()

app.include_router(user.router)
app.include_router(objects.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

