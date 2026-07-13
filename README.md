# Coderr Backend

A Django REST Framework backend for the Coderr platform, where business users
offer services and customer users order them and leave reviews. This repository
contains the backend only; the frontend is a separate project.

## Tech Stack

- Python 3.14
- Django 6.0
- Django REST Framework 3.17 (Token Authentication)
- django-cors-headers
- SQLite (default development database)

## Requirements

- Python 3.12 or newer installed and available on your PATH.

## Setup

1. Clone the repository and enter the project folder:

   ```
   git clone <repository-url>
   cd Backend
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv env
   ```

   - Windows (PowerShell): `env\Scripts\Activate.ps1`
   - Windows (cmd): `env\Scripts\activate.bat`
   - macOS / Linux: `source env/bin/activate`

3. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Apply the database migrations:

   ```
   python manage.py migrate
   ```

5. (Optional) Create an admin account for the Django admin panel:

   ```
   python manage.py createsuperuser
   ```

6. Start the development server:

   ```
   python manage.py runserver
   ```

The API is now available at `http://127.0.0.1:8000/api/` and the admin panel at
`http://127.0.0.1:8000/admin/`.

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

## Project Structure

```
Backend/
├── core/              Project configuration (settings, root URLs)
├── user_auth_app/     Registration, login and profiles
├── offers_app/        Offers and offer details
├── orders_app/        Orders and order statistics
├── reviews_app/       Reviews
├── base_info_app/     Aggregated platform statistics
├── manage.py
└── requirements.txt
```
