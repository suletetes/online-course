# Online Course — Django App

A lightweight Django-based online course platform that lets students browse courses, enroll, read course content, and
take timed exams. This repository contains the full backend and frontend templates for a simple learning platform with
authentication, course pages, enrollment, and exam/result flow.

## Key features

- Browse available courses with images and descriptions
- User registration and login (student accounts)
- Enroll in courses and access course content
- Start and submit exams; view results immediately after submission
- Responsive Bootstrap-based templates and static assets included
- Media support for course images

## Quick start (for development)

### Prerequisites

- Python 3.8+ (recommended)
- pip
- virtualenv (recommended)
- SQLite (default, included) or another supported Django database

### Setup

1. Clone the repository

   ```bash
   git clone <repo-url>
   cd online-course
   ```

2. Create and activate a virtual environment

   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS / Linux
   venv\Scripts\activate    # Windows
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations

   ```bash
   python manage.py migrate
   ```

5. (Optional) Create a superuser to access the Django admin

   ```bash
   python manage.py createsuperuser
   ```

6. Collect static files (for production)

   ```bash
   python manage.py collectstatic
   ```

7. Run the development server

   ```bash
   python manage.py runserver
   ```

   Open `http://127.0.0.1:8000/` in your browser.

### Configuration

- Database: default uses SQLite (`db.sqlite3`). To use PostgreSQL or MySQL, update `myproject/settings.py` DATABASES
  section.
- Media files: course images are stored in `media/course_images`. Ensure `MEDIA_ROOT` and `MEDIA_URL` are configured in
  settings.
- Static files: `static/` contains admin and app CSS/JS. `STATIC_ROOT` is used when running collectstatic.

## Usage

- Register or log in using the registration/login pages.
- Browse the course list page to view available courses.
- Click a course to view details and enroll.
- After enrolling, access the course contents and start available exams.
- Exams are launched from the course detail page; after submission, results are shown on the exam results page.

## Project layout (important files)

- `manage.py` — Django management script
- `myproject/` — Django project settings and URLs
- `onlinecourse/` — main app containing models, views, templates, and URLs
- `static/` — static assets (CSS, JS, images)
- `media/course_images/` — packaged course images
- `templates/onlinecourse/` — Bootstrap templates for pages

## Testing

- Run the test suite with:

  ```bash
  python manage.py test
  ```

## Deployment notes

- Use a production-ready web server (Gunicorn, uWSGI) behind a reverse proxy (Nginx).
- Configure environment variables for `SECRET_KEY` and `DEBUG`.
- Use a production database (PostgreSQL recommended) and serve static/media via CDN or separate storage.
- `Procfile` and `manifest.yml` are included for simple deploys (Heroku-style).

## Contributing

Contributions are welcome. Suggested workflow:

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Open a pull request with a clear description of the changes

