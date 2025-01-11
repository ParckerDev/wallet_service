from fastapi import FastAPI
from api.router import router as wallet_router

app = FastAPI()

app.include_router(wallet_router)

@app.get('/', tags=['INDEX'])
async def index():
    return {'message': 'RESTFULL API docs here -> http://127.0.0.1:8000/docs'}






