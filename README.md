# Introduction
This project is the back-end api built using Django of the [todolist frontend](https://github.com/medardm/nextjs-todolist-frontend).

## Documentation
- the [docs](https://github.com/medardm/django-todolist-api/tree/main/docs/diagrams) directory contains all the project-related documents, design discussions, and diagrams (created using PlantUML).


## Setup Instructions

### Prerequisites

- Python 3.9.6
- Pip package manager
- Virtualenv (Optional but recommended)

### Steps
1. **Clone the repository**
   Use Git to clone the repository.
   `git clone https://github.com/medardm/django-todolist-api`

2. **Create a virtual environment** (Optional)
   We highly recommend creating a virtual environment to isolate the application dependencies from your system's Python environment.
    - If you are using `virtualenv`, use: `virtualenv .venv`
    - You can also use `python3 -m venv venv` if you are in mac/linux
    - Activate the virtual environment. On macOS/Linux, use: `source .venv/bin/activate`. On Windows, use: `.venv\Scripts\activate.bat`

3. **Install dependencies**
   Your project should include a `requirements.txt` file that lists the project's dependencies. Install them with:
   `pip install -r requirements.txt`

4. **Apply migrations**
   Django projects typically need to apply migrations to the database before running. This can be done with:
   `python manage.py migrate`

5. **Run the Development Server**
   Start the Django development server with:
   `python manage.py runserver`

6. **Access the Application**
   You can access the application at `http://127.0.0.1:8000/` or `http://localhost:8000/`

[//]: # (7. **Running Tests**)

[//]: # (   If applicable, you can run tests for your application with:  )

[//]: # (   `python manage.py test`)

