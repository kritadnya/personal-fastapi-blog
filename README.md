# FASTAPI_BLOG

```text
FASTAPI_BLOG/
│
├── alembic/
│   ├── versions/
│   │   ├── 537efd1330ad_initial_schema.py
│   │   └── e1db85a9a97f_add_likes_to_post.py
│   ├── env.py
│   ├── script.py.mako
│   └── README
│
├── media/
│   └── profile_pics/
│
├── routers/
│   ├── __init__.py
│   ├── posts.py
│   └── users.py
│
├── static/
│   ├── css/
│   │   └── main.css
│   ├── icons/
│   ├── images/
│   ├── js/
│   │   ├── auth.js
│   │   ├── navbar-particles.js
│   │   └── utils.js
│   └── site.webmanifest
│
├── templates/
│   ├── email/
│   │   └── password_reset.html
│   ├── account.html
│   ├── error.html
│   ├── forgot_password.html
│   ├── home.html
│   ├── layout.html
│   ├── login.html
│   ├── post.html
│   ├── register.html
│   ├── reset_password.html
│   └── user_posts.html
│
├── auth.py
├── config.py
├── database.py
├── email_utils.py
├── image_utils.py
├── main.py
├── models.py
├── schemas.py
├── alembic.ini
├── .gitignore
└── README.md
```

```text
🚀 FastAPI Blog Platform

A modern full-stack blogging platform built with **FastAPI** that allows users to register, create blog posts, upload profile pictures, like posts, and manage their accounts through a clean and responsive web interface.

✨ Features

1 🔐 User registration and login with JWT authentication
2 📝 Create, edit, and delete blog posts
3 ❤️ Like blog posts
4 👤 User profiles with profile picture uploads
5 🖼️ Image processing using Pillow
6 📧 Password reset via email
7 📄 Paginated home page
8 🕒 Post timestamps and author pages
9 🎨 Responsive UI built with Jinja2, HTML, CSS, and JavaScript
10 🗄️ Database migrations with Alembic

🛠️ Tech Stack

| Category            | Technologies                    |
| ------------------- | ------------------------------- |
| **Backend**         | FastAPI, Python                 |
| **Database**        | PostgreSQL, SQLAlchemy, Alembic |
| **Authentication**  | JWT, Password Hashing           |
| **Frontend**        | Jinja2, HTML, CSS, JavaScript   |
| **Image Handling**  | Pillow                          |
| **Email**           | SMTP                            |
| **Version Control** | Git, GitHub                     |


🚀 Getting Started

```bash
git clone https://github.com/your-username/fastapi-blog.git

cd fastapi-blog

python -m venv venv

# Activate the virtual environment

pip install -r requirements.txt

alembic upgrade head

uvicorn main:app --reload
```

Open your browser and visit:

```
http://127.0.0.1:8000
http://127.0.0.1:8000/docs
```

```