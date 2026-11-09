import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from src.routers import root, areas, auth, cameras, edge, events, media, users

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root.router)

api = APIRouter(prefix="/api/v1")
for module in (auth, users, areas, cameras, events, media, edge):
    api.include_router(module.router)
app.include_router(api)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)