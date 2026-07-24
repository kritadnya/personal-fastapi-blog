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
# FastAPI Blog Platform

A full-stack blogging platform built with **FastAPI** that enables users to create, manage, and share blog posts through a secure and responsive web interface. The application implements authentication, user profiles, image uploads, email-based password recovery, and a clean, modern UI while following FastAPI best practices.

## Features

* 🔐 Secure user authentication with JWT and password hashing
* 📝 Create, edit, delete, and view blog posts (CRUD)
* ❤️ Like posts
* 👤 User profiles with profile picture uploads
* 🖼️ Image processing and storage using Pillow
* 📧 Password reset via email
* 📄 Paginated blog feed
* 🕒 Post timestamps and author-specific post pages
* 🎨 Responsive frontend built with Jinja2 templates, HTML, CSS, and JavaScript
* 🗄️ Database migrations with Alembic
* ⚙️ Environment-based configuration using Pydantic Settings

## Tech Stack

**Backend**

* FastAPI
* Python
* SQLAlchemy (Async ORM)
* Alembic
* PostgreSQL
* JWT Authentication

**Frontend**

* Jinja2
* HTML5
* CSS3
* JavaScript

**Other**

* Pillow
* SMTP Email
* Git & GitHub

## Project Highlights

* Designed RESTful APIs for user authentication and blog management.
* Implemented asynchronous database operations using SQLAlchemy Async.
* Added secure password reset functionality through email.
* Built reusable Jinja2 templates for server-side rendering.
* Managed schema evolution with Alembic migrations.
* Structured the project into modular routers and reusable utility modules for maintainability.
```