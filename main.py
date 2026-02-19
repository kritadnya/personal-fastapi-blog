from typing import Annotated

from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException

# from fastapi.responses import HTMLResponse : not required since we will be using Jinja2 templates 
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import models 
from database import Base , engine, get_db
from schemas import PostCreate, PostResponse, UserCreate, UserResponse

# we need to create our db table before we create our app
Base.metadata.create_all(bind=engine) # this looks at all of our models that inherit from Base and creates the tables if they dont already exist

app = FastAPI()     # "this app object is what we will use to define all of our routes" - understand what this sentence means 

app.mount("/static", StaticFiles(directory="static"), name="static")

# this creates a "/ media" url prefix and serves files from that media dir
app.mount("/media", StaticFiles(directory="media"), name="media")

templates = Jinja2Templates(directory= "templates") # this creates a templates object that will look into our templates directory for files

# FastAPI uses decorators for routes
# lets create our first route which responds to get requests at the root URL; we want this to be for the home route so we use '/' a forward slash

# posts: list[dict] = [
#     {
#         "id": 1,
#         "author": "Kritadnya Kaling",
#         "title": "FastAPI is Awesome",
#         "content": "This framework is really easy to use and super fast.",
#         "date_posted": "January 20, 2026",
#     },
#     {
#         "id": 2,
#         "author": "Pratiksha Nayak",
#         "title": "Python is Great for Web Development",
#         "content": "Python is a great language for web development, and FastAPI makes it even better.",
#         "date_posted": "January 21, 2026",
#     },
# ]

# @app.get("/", response_class=HTMLResponse, include_in_schema=False)
# @app.get("/posts", response_class=HTMLResponse, 
# include_in_schema=False)

# @app.get("/", include_in_schema=False, name="home")
# @app.get("/posts", include_in_schema=False, name="posts")
# def home(request: Request): # function that we are decorating
#     return templates.TemplateResponse(request, "home.html", {"posts": posts, "title":"Home"} ) # ! Understand what this means 

# updated home route:
@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request, db:Annotated[Session, Depends(get_db)]): # function that we are decorating
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return templates.TemplateResponse(request, "home.html", {"posts": posts, "title":"Home"} ) # ! Understand what this means 


# @app.get("/posts/{post_id}", include_in_schema=False)
# def post_page(request: Request,post_id:int):
#     for post in posts:
#         if post.get("id") == post_id:
#             title = post['title'][:50]
#             return templates.TemplateResponse(
#                 request, 
#                 "post.html", 
#                 {"post": post, "title":"title"} 
#                 )
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post was not found")

# updated 
@app.get("/posts/{post_id}", include_in_schema=False)
def post_page(request: Request,post_id:int, db:Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if post:
        title = post.title[:50]
        return templates.TemplateResponse(
                request, 
                "post.html", 
                {"post": post, "title":"title"} 
                )
            
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post was not found")


@app.get("/users/{user_id}/posts", include_in_schema=False, name="user_posts")
def user_posts_page( 
    request: Request, user_id: int,
db: Annotated [Session, Depends (get_db)],
):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="User not found"
        )
    result = db.execute(select(models.Post).where(models.Post.user_id == user_id))
    posts = result.scalars().all()
    return templates.TemplateResponse(
    request,
    "user_posts.html",
    {"posts": posts, "user": user, "title": f"{user.username}'s Posts"},
    )



@app.post(
        "api/users",
        response_model=UserResponse,
        status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, db:Annotated[Session, Depends(get_db)]): # this is called a "dependency injection" this tells fatsapi before writing this function call get_db and pass the result into the db parameter
    # check if a user already exists
    result = db.execute(select(models.User).where(models.User.username ==user.username),
     )
    existing_user = result.scalars().first() # Gets the first user object or None if there is no match 

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User name already exists",
        )
    # check if a email already exists
    result = db.execute(select(models.User).where(models.User.email ==user.email),
     )
    existing_email = result.scalars().first() # Gets the first user object or None if there is no match 

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )
    new_user = models.User(
        username = user.username,
        email = user.email,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # not strictly necessary but a good habit 

    return new_user



@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id:int, db:Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id ==user_id),
     )
    existing_email = result.scalars().first()

    if user:
        return user
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

# get user posts, to get all posts by a user
@app.get("/api/users/{user_id}/posts", response_model=list[PostResponse])
def get_user_posts(user_id: int, db: Annotated[Session, Depends(get_db)]):
    # check if the user exists, if the user exists then query their posts 
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    result = db.execute(select(models.Post).where(models.Post.user_id ==user_id),
     )
    posts = result.scalars().all()
    return posts



# @app.get("/api/posts", response_model=list[PostResponse])
# def get_posts():
#     return posts

@app.get("/api/posts", response_model=list[PostResponse])
def get_posts(db:Annotated[Session, Depends(get_db)]):
    # quering for all of the posts and returning them
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return posts

@app.post(
        "api/posts",
        response_model=PostResponse,
        status_code=status.HTTP_201_CREATED
)
def create_post(post: PostCreate, db: Annotated[Session, Depends (get_db)]) :
    # verify if user exists then create the post with teh user id and add it ot the db
    result = db.execute(select(models.User).where(models.User.id == post.user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException (
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="User not found",
        )
    new_post = models.Post(
        title=post.title, 
        content=post.content, 
        user_id=post.user_id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
# def create_post(post: PostCreate):
#     new_id = max(p["id"] for p in posts) + 1 if posts else 1
#     new_post = {
#         "id": new_id,
#         "author": post.author,
#         "title": post.title,
#         "content": post.content,
#         "date_posted": "January 20, 2025" ,  
#           }
#     posts.append(new_post)
#     return new_post

# to display specific posts; post_id is called as a path parameter 
@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id:int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    
    if post:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post was not found")

## StarletteHTTPException Handler
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )

### RequestValidationError Handler
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )