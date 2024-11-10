from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.user import user_controller
from app.routes.auth import auth_controller

origin = ['*']

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class Route:
    def __init__(self, *args) -> None:
        [app.include_router(keys.router) for keys in args]


app_route = Route(
    user_controller,
    auth_controller,
    )


@app.get('/')
async def home():
    return {"messsage": "Welcome to the home page"}

# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
