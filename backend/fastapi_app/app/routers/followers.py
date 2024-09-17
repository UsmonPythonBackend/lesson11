from fastapi import APIRouter, Depends, HTTPException, status
from backend.fastapi_app.app.database import Session, ENGINE
from backend.fastapi_app.app.schemas import FollowersCreateSchema, FollowersUpdateSchema
from backend.fastapi_app.app.models import Likes, User, Followers
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import or_
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page, paginate, add_pagination



session = Session(bind=ENGINE)

followers_router = APIRouter(
    prefix="/followers",
    tags=['Followers']
)


@followers_router.get('/')
async def get_followers(authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()

        current_user = session.query(User).filter(
            or_(
                User.username == authorization.get_jwt_subject(),
                User.email == authorization.get_jwt_subject(),
            )
        ).first()
        if current_user is not None:
            followers = session.query(Likes).filter(Likes.user == current_user).all()
            data = {
                "success": True,
                "code": 200,
                "message": f"All posts by {current_user.username} followers",
                "posts": followers
            }
            return jsonable_encoder(data)


    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")





@followers_router.post('/')
async def create_followers(post: FollowersCreateSchema, authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()

        current_user = session.query(User).filter(
            or_(
                User.username == authorization.get_jwt_subject(),
                User.email == authorization.get_jwt_subject(),
            )
        ).first()
        if current_user is not None:
            new_follower = Followers(
                follower_id=post.follower.id,
                following_id=post.following.id

            )
            new_follower.user = current_user
            session.add(new_follower)
            session.commit()

            data = {
                "status": 201,
                "message": f"Follower created successfully by {authorization.get_jwt_subject()}",
            }
            return jsonable_encoder(data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")


@followers_router.put("/{id}")
async def update_followers(id: int, post: FollowersUpdateSchema, authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()
        current_user = session.query(User).filter(User.username == authorization.get_jwt_subject()).first()
        if current_user:
            update_followers = session.query(Followers).filter(Followers.id == id).first()
            if update_followers:
                for key, value in post.dict().items():
                    setattr(update_followers, key, value)

                    data = {
                        "code": 200,
                        "success": True,
                        "message": "Successfully updated like",
                        "object": {
                            "follower_id": update_followers.follower_id,
                            "following_id": update_followers.following_id
                        }
                    }
                    session.add(update_followers)
                    session.commit()
                    return jsonable_encoder(data)

            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Follower not found")
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')


@followers_router.delete("/{id}")
async def delete_followers(id: int, authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()
        current_user = session.query(User).filter(User.username == authorization.get_jwt_subject()).first()
        if current_user:
            followers = session.query(Followers).filter(Followers.id == id).first()
            if followers:
                session.delete(followers)
                session.commit()
                return jsonable_encoder({"code": 200, "message": "Successfully deleted followers"})
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="followers not found")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')