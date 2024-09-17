from pydantic import BaseModel
from typing import Optional

class ConfigBase(BaseModel):
    authjwt_secret_key: str = "45b5f73b5b4d9bd32faedb2d2ec70a603ecedaa0e2cc0ea8c2bcdaa6eea5f1ca"

class LoginSchema(BaseModel):
    username_or_email: Optional[str]
    password: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username_or_phone_number": None,
                "password": None
            }
        }

class UserRegisterSchema(BaseModel):
    username: Optional[str]
    password: Optional[str]
    email: Optional[str]

class UserLoginSchema(BaseModel):
    username_or_email: Optional[str]
    password: Optional[str]


# class ConfigBase(BaseModel):
#     authjwt_secret_key: str = "secret_token"


class CommentCreateSchema(BaseModel):
    user_id: Optional[int]
    post_id: Optional[int]
    content: Optional[str]


class CommentUpdateSchema(BaseModel):
    user_id: Optional[int]
    post_id: Optional[int]
    content: Optional[str]


class FollowersCreateSchema(BaseModel):
    follower_id: Optional[str]
    following_id: Optional[str]



class FollowersUpdateSchema(BaseModel):
    follower_id: Optional[str]
    following_id: Optional[str]


class LikesCreateSchema(BaseModel):
    user_id: Optional[str]
    post_id: Optional[str]


class LikesUpdateSchema(BaseModel):
    user_id: Optional[str]
    post_id: Optional[str]


class CreatePostsSchema(BaseModel):
    caption: Optional[str]
    image_path: Optional[str]


class UpdatePostsSchema(BaseModel):
    caption: Optional[str]
    image_path: Optional[str]

