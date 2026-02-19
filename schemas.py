from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field , EmailStr


# create our base schema with the fields shared between creating and returning post 

class UserBase(BaseModel):
    username:str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)

# what we expect when we create a user
class UserCreate(UserBase):
    pass

# 
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id:int
    image_file: str| None
    image_path: str

# this class is going to be shared between both creating and returning 
# so when we are creating and returning a post we want title content and the author name 
# pydantic uses this type hints to validate the data during runtime 
class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100 )
    content: str = Field(min_length=1 )
    # author: str= Field(min_length=1, max_length=50)

# make a post create schema; this defines what we accept when creating a post
class PostCreate(PostBase):
    user_id: int # TEMPORARY

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id : int

    date_posted: datetime
    author: UserResponse


# these schemas defien what we accept and return through our APIs