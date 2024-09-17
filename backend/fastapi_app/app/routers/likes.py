from fastapi import APIRouter, Depends, HTTPException, status
from backend.fastapi_app.app.database import Session, ENGINE
from backend.fastapi_app.app.schemas import LikesCreateSchema, LikesUpdateSchema
from backend.fastapi_app.app.models import Likes, User
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import or_
from fastapi.encoders import jsonable_encoder


session = Session(bind=ENGINE)

likes_router = APIRouter(
    prefix="/likes",
    tags=['Likes']
)

@likes_router.get('/')
async def get_likes(authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()

        current_user = session.query(User).filter(
            or_(
                User.username == authorization.get_jwt_subject(),
                User.email == authorization.get_jwt_subject(),
            )
        ).first()
        if current_user is not None:
            likes = session.query(Likes).filter(Likes.user == current_user).all()
            data = {
                "success": True,
                "code": 200,
                "message": f"All posts by {current_user.username} likes",
                "posts": likes
            }
            return jsonable_encoder(data)


    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")



@likes_router.post('/')
async def create_likes(post: LikesCreateSchema, authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()

        current_user = session.query(User).filter(
            or_(
                User.username == authorization.get_jwt_subject(),
                User.email == authorization.get_jwt_subject(),
            )
        ).first()
        if current_user is not None:
            new_likes = Likes(
                user_id=post.user.id,
                post_id=post.post_id

            )
            new_likes.user = current_user
            session.add(new_likes)
            session.commit()

            data = {
                "status": 201,
                "message": f"Likes created successfully by {authorization.get_jwt_subject()}",
            }
            return jsonable_encoder(data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")




@likes_router.put("/{id}")
async def update_post(id: int, post: LikesUpdateSchema, authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()
        current_user = session.query(User).filter(User.username == authorization.get_jwt_subject()).first()
        if current_user:
            update_likes = session.query(Likes).filter(Likes.id == id).first()
            if update_likes:
                for key, value in post.dict().items():
                    setattr(update_likes, key, value)

                    data = {
                        "code": 200,
                        "success": True,
                        "message": "Successfully updated like",
                        "object": {
                            "user_id": update_likes.id,
                            "post_id": update_likes.post_id
                        }
                    }
                    session.add(update_post)
                    session.commit()
                    return jsonable_encoder(data)

            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="like not found")
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')


@likes_router.delete("/{id}")
async def delete_likes(id: int, authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()
        current_user = session.query(User).filter(User.username == authorization.get_jwt_subject()).first()
        if current_user:
            likes = session.query(Likes).filter(Likes.id == id).first()
            if likes:
                session.delete(likes)
                session.commit()
                return jsonable_encoder({"code": 200, "message": "Successfully deleted likes"})
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
