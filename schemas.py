from pydantic import BaseModel, ConfigDict, Field 

# create our base schema with the fields shared between creating and returning post 

# this class is going to be shared between both creating and returning 
# so when we are creating and returning a post we want title content and the author name 
# pydantic uses this type hints to validate the data during runtime 
class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100 )
    content: str = Field(min_length=1 )
    author: str= Field(min_length=1, max_length=50)

# make a post create schema; this defines what we accept when creating a post
class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    date_posted: str
