# Coderr Backend

A Django REST Framework backend for the Coderr platform, where business users
offer services and customer users order them and leave reviews. This repository
contains the backend only; the frontend is a separate project.

## Tech Stack

- Python 3.14 (developed with), 3.12 or newer required
- Django 6.0
- Django REST Framework 3.17 (Token Authentication)
- django-cors-headers
- python-dotenv (environment variables)
- Pillow (profile image uploads)
- SQLite (default development database)

## Setup

1. Clone the repository and enter the project folder:

   ```
   git clone https://github.com/kkupschi/Coderr.git
   cd Coderr
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv .venv
   ```

   - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
   - Windows (cmd): `.venv\Scripts\activate.bat`
   - macOS / Linux: `source .venv/bin/activate`

3. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Create your environment file. Copy the template and fill in the values:

   - Windows (PowerShell): `Copy-Item .env.template .env`
   - macOS / Linux: `cp .env.template .env`

   Then generate a secret key and paste it into `.env` as `SECRET_KEY`:

   ```
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   See [Environment Variables](#environment-variables) for all available keys.

5. Apply the database migrations:

   ```
   python manage.py migrate
   ```

6. (Optional) Create an admin account for the Django admin panel:

   ```
   python manage.py createsuperuser
   ```

7. Start the development server:

   ```
   python manage.py runserver
   ```

The API is now available at `http://127.0.0.1:8000/api/` and the admin panel at
`http://127.0.0.1:8000/admin/`.

## Environment Variables

All secrets live in a `.env` file in the project root. This file is excluded
from version control; `.env.template` documents the expected keys and is the
file you copy from.

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `SECRET_KEY` | yes | none | Django secret key. The app refuses to start without it. |
| `DEBUG` | no | `False` | Set to `True` for local development only. |
| `ALLOWED_HOSTS` | no | empty | Comma-separated host list, for example `example.com,www.example.com`. |

## Frontend Connection (CORS)

The backend allows requests from the Live Server default origin
(`http://127.0.0.1:5500` and `http://localhost:5500`). If your frontend runs on
a different origin, add it to `CORS_ALLOWED_ORIGINS` in `core/settings.py`.

## Authentication

Most endpoints require a token. Register or log in to receive a token, then send
it with each request in the `Authorization` header:

```
Authorization: Token <your-token>
```

## API Overview

Base path: `/api/`

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `registration/` | Register a new customer or business user |
| POST | `login/` | Log in and receive a token |
| GET / PATCH | `profile/<pk>/` | Retrieve or update a user profile |
| GET | `profiles/business/` | List all business profiles |
| GET | `profiles/customer/` | List all customer profiles |
| GET / POST | `offers/` | List offers (filter/search/order) or create one |
| GET / PATCH / DELETE | `offers/<id>/` | Retrieve, update or delete an offer |
| GET | `offerdetails/<id>/` | Retrieve a single offer detail |
| GET / POST | `orders/` | List own orders or create one |
| PATCH / DELETE | `orders/<id>/` | Update the status or delete an order |
| GET | `order-count/<business_user_id>/` | Count of running orders |
| GET | `completed-order-count/<business_user_id>/` | Count of completed orders |
| GET / POST | `reviews/` | List reviews or create one |
| PATCH / DELETE | `reviews/<id>/` | Update or delete a review |
| GET | `base-info/` | Platform statistics |

### Query Parameters

`offers/` accepts `creator_id`, `min_price` and `max_delivery_time` as filters,
`search` for title and description, and `ordering` for `updated_at` or
`min_price`. `reviews/` accepts `business_user_id` and `reviewer_id` as filters
and `ordering` for `updated_at` or `rating`. Invalid values return `400`.

## Project Structure

```
Backend/
├── core/              Project configuration (settings, root URLs, validators)
├── user_auth_app/     Registration, login and profiles
├── offers_app/        Offers and offer details
├── orders_app/        Orders and order statistics
├── reviews_app/       Reviews
├── base_info_app/     Aggregated platform statistics
├── .env.template      Template for the required environment variables
├── manage.py
└── requirements.txt
```

Each app follows the same layout: an `api/` package holding `views.py`,
`serializers.py`, `permissions.py` and `utils.py`, with the models at app level.
