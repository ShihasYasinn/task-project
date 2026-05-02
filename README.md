# Task Management System

A robust and efficient task management application built with Django.

## Features

- **Custom User Management**: Role-based access control (Admin, Supervisor, Associate).
- **Department Management**: Organize tasks by departments with assigned heads.
- **Task Dashboard**: High-level overview of task statuses and performance metrics.
- **Responsive Design**: Modern UI/UX built with professional aesthetics.

## Tech Stack

- **Backend**: Django 6.0
- **Database**: PostgreSQL
- **Configuration**: Python-decouple for environment variables
- **Styling**: Vanilla CSS with modern design patterns

## Getting Started

1.  Clone the repository.
2.  Install dependencies: `pip install -r requirements.txt`.
3.  Set up your `.env` file with `DATABASE_URL` and `SECRET_KEY`.
4.  Run migrations: `python manage.py migrate`.
5.  Start the server: `python manage.py runserver`.