from datetime import datetime


from pydantic import BaseModel, ConfigDict, Field, EmailStr


# pydantic schemas help us determine what we accept and return from api

class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True) # True so that pydantic can read from sqlalchemy model
    id: int
    image_file : str | None
    image_path: str 

class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=120)
    image_file: str | None = Field(default=None, min_length=1, max_length=200)




# fields shared between creating and returning posts
class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)
    

# what we accept when we create a new post
class PostCreate(PostBase):
    user_id: int

class PostUpdate(BaseModel):
    title: str | None = Field(default = None, min_length=1, max_length=100)
    content: str | None = Field(default = None, min_length=1)
  

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True) # can read data from attributes, objects, database tables not just limited to dictionaries 

    id: int
    user_id: int
    date_posted: datetime
    author: UserResponse