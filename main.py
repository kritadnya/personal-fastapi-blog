from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

# from fastapi.responses import HTMLResponse : not required since we will be using Jinja2 templates 
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from schemas import PostCreate, PostResponse

app = FastAPI()     # "this app object is what we will use to define all of our routes" - understand what this sentence means 

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory= "templates") # this creates a templates object that will look into our templates directory for files

# FastAPI uses decorators for routes
# lets create our first route which responds to get requests at the root URL; we want this to be for the home route so we use '/' a forward slash

posts: list[dict] = [
    {
        "id": 1,
        "author": "Kritadnya Kaling",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "January 20, 2026",
    },
    {
        "id": 2,
        "author": "Pratiksha Nayak",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "January 21, 2026",
    },
]

# @app.get("/", response_class=HTMLResponse, include_in_schema=False)
# @app.get("/posts", response_class=HTMLResponse, 
# include_in_schema=False)

@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request): # function that we are decorating
    return templates.TemplateResponse(request, "home.html", {"posts": posts, "title":"Home"} ) # ! Understand what this means 

@app.get("/posts/{post_id}", include_in_schema=False)
def post_page(request: Request,post_id:int):
    for post in posts:
        if post.get("id") == post_id:
            title = post['title'][:50]
            return templates.TemplateResponse(
                request, 
                "post.html", 
                {"post": post, "title":"title"} 
                )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post was not found")

@app.get("/api/posts", response_model=list[PostResponse])
def get_posts():
    return posts

@app.post(
        "api/posts",
        response_model=PostResponse,
        status_code=status.HTTP_201_CREATED
)
def create_post(post: PostCreate):
    new_id = max(p["id"] for p in posts) + 1 if posts else 1
    new_post = {
        "id": new_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "date_posted": "January 20, 2025" ,  
          }
    posts.append(new_post)
    return new_post

# to display specific posts; post_id is called as a path parameter 
@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id:int):
    for post in posts:
        if post.get("id") == post_id:
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