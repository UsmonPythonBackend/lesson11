import datetime

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

from backend.fastapi_app.app.database import Session, ENGINE
from backend.fastapi_app.app.models import User
from backend.fastapi_app.app.schemas import UserRegisterSchema, UserLoginSchema
from fastapi.encoders import jsonable_encoder


session = Session(bind=ENGINE)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.get("/")
async def auth_router():
    all_posts = session.query(User).all()
    return jsonable_encoder(all_posts)

@router.post("/register")
async def auth_register_user(request: UserRegisterSchema):
    check_user = session.query(User).filter(
        or_(
            User.username == request.username,
            User.email == request.email
        )
    ).first()
    if check_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_user = User(
        username=request.username,
        email=request.email,
        password=generate_password_hash(request.password)
    )
    session.add(new_user)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="User registered")

@router.post("/login")
async def auth_login_user(request: UserLoginSchema, authorization: AuthJWT = Depends()):
    check_user = session.query(User).filter(
        or_(
            User.username == request.username_or_email,
            User.email == request.username_or_email
        )
    ).first()
    if check_user and check_password_hash(check_user.password, request.password):
        access_token = authorization.create_access_token(subject=request.username_or_email, expires_time=datetime.timedelta(minutes=15))
        refresh_token = authorization.create_refresh_token(subject=request.username_or_email, expires_time=datetime.timedelta(days=2))
        response = {
            "status_code": 200,
            "detail": "User logged in",
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        return jsonable_encoder(response)

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")


@router.get('/users')
async def get_users(authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()
        users = session.query(User).all()
        data = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at
            }
            for user in users
        ]
        return jsonable_encoder(data)
    except Exception as e:
        return HTTPException(status_code=401, detail="Token invalid")

