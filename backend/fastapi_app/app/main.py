from fastapi import FastAPI
from uvicorn import run
from fastapi_jwt_auth import AuthJWT
from .routers.auth_router import auth_router
from .routers.comments import comment_router
from .routers.followers import followers_router
from .routers.likes import likes_router
from .routers.posts import post_router
from backend.fastapi_app.app.schemas import ConfigBase



@AuthJWT.load_config
def get_config():
    return ConfigBase()

app = FastAPI()


@app.get("/")
async def root():
    return {"Assalomu": "Aleykum"}



app.include_router(auth_router.router)
app.include_router(comment_router)
app.include_router(followers_router)
app.include_router(likes_router)
app.include_router(post_router)