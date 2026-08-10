# Gorgan Abzar

A production-oriented e-commerce platform built with Django for managing products, customers, orders, payments, content, and customer interactions.

The project provides a complete shopping experience including product discovery, authentication via mobile number and OTP, cart management, checkout, discount codes, online payments, order tracking, customer dashboards, and content management.

---

## Features

### Authentication & Accounts

* Custom Django user model
* Phone number-based authentication
* OTP verification
* User profile management
* Multiple user addresses
* Default address management
* Secure session-based authentication

### Product Management

* Product catalog
* Product categories
* Brands
* Product galleries
* Product variants and features
* Product stock management
* Discounted products
* Featured products
* Product visit tracking
* Favorites
* Automatic product image optimization

### Shopping & Orders

* Session-based shopping cart
* Cart quantity management
* Checkout workflow
* Order creation and management
* Order status tracking
* Shipping cost management
* Order tracking codes
* Stock validation
* Automatic stock reduction after successful payment

### Discounts

* Discount code management
* Fixed-amount discounts
* Expiration dates
* Per-user discount usage tracking
* Prevention of repeated use of paid discount codes

### Payments

* ZarinPal payment gateway integration
* Payment request handling
* Payment verification
* Payment callback workflow
* Payment status tracking

### Content

* Blog
* Blog categories
* Blog filtering
* Global search
* Reviews
* Contact form
* Dynamic homepage content
* Custom 404 page

### Administration

* Django Admin
* Custom administration routes
* Product management
* Order management
* Customer management
* Discount management
* Content management
* Review management

---

## Tech Stack

| Technology       | Purpose                    |
| ---------------- | -------------------------- |
| Python           | Backend language           |
| Django 5.2       | Web framework              |
| MySQL            | Relational database        |
| Django Templates | Server-side rendering      |
| CKEditor         | Rich text editing          |
| Pillow           | Image processing           |
| Kavenegar        | SMS/OTP delivery           |
| ZarinPal         | Online payments            |
| Requests         | External API communication |
| python-decouple  | Environment configuration  |
| Jalali Date      | Persian date support       |
| django-ratelimit | Request rate limiting      |

---

## Architecture

The application follows a modular Django architecture where business domains are separated into dedicated applications.

```text
Client
   │
   ▼
Django URL Router
   │
   ├── Home
   ├── Authentication
   ├── Products
   ├── Orders
   ├── Dashboard
   ├── Blog
   ├── Search
   ├── Reviews
   └── Contact
   │
   ▼
Application Services & Business Logic
   │
   ├── Cart Management
   ├── Order Calculation
   ├── Stock Management
   ├── Discount Validation
   └── Payment Processing
   │
   ▼
MySQL Database
```

---

## Project Structure

```text
gorgan-abzar/
├── accounts/
├── blog/
├── config/
├── contact/
├── core/
├── dashboard/
├── home/
├── order/
├── product/
├── reviews/
├── search/
├── static/
├── templates/
├── manage.py
├── requirements.txt
├── .env.example
└── .gitignore
```

### Main Applications

#### `accounts`

Responsible for authentication and user management.

```text
accounts/
├── managers.py
├── models.py
├── forms.py
├── views.py
├── urls.py
└── admin.py
```

#### `product`

Handles the product catalog and related functionality.

```text
product/
├── models/
│   ├── product.py
│   ├── category.py
│   ├── brand.py
│   ├── gallery.py
│   ├── feature.py
│   ├── favorite.py
│   └── visit.py
├── views/
├── templates/
└── admin.py
```

#### `order`

Contains shopping cart, checkout, order, discount, and payment logic.

```text
order/
├── models/
├── utils/
│   ├── cart_manager.py
│   ├── order_calculator.py
│   └── payment_manager.py
├── views/
├── forms.py
└── admin.py
```

#### `dashboard`

Provides customer-facing account functionality.

* Profile management
* Address management
* Favorites
* Order history
* Account overview

#### `blog`

Provides blog and article functionality.

#### `search`

Provides global search functionality.

#### `core`

Contains shared infrastructure and reusable functionality.

* Base models
* Context processors
* OTP utilities
* Notification services
* HTTP utilities
* Media handling
* Template tags

---

## Requirements

Before running the project, make sure the following are installed:

* Python 3.12+
* MySQL
* pip
* Git

---

## Installation

Clone the repository:

```bash
git clone https://github.com/alidowlat/gorgan-abzar.git
cd gorgan-abzar
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root based on `.env.example`.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True

ALLOWED_HOSTS=127.0.0.1,localhost

DB_ENGINE=django.db.backends.mysql
DB_NAME=your_database
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=127.0.0.1
DB_PORT=3306

KAVENEGAR_API=your-kavenegar-api-key

ZP_API=your-zarinpal-merchant-id
ZP_API_REQUEST=your-zarinpal-request-url
ZP_API_VERIFY=your-zarinpal-verify-url
ZP_API_STARTPAY=your-zarinpal-start-payment-url
ZP_API_CALLBACKURL=your-callback-url
```

Never commit `.env` or any secret credentials to the repository.

---

## Database Setup

Create the MySQL database and configure the database credentials in `.env`.

Run migrations:

```bash
python manage.py migrate
```

Create an administrator account:

```bash
python manage.py createsuperuser
```

---

## Development

Run the development server:

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

---

## Static & Media Files

During development, Django serves media files directly when `DEBUG=True`.

Static files are located in:

```text
static/
```

Uploaded media files are stored in:

```text
media/
```

For production, the project uses dedicated static and media directories configured through `STATIC_ROOT` and `MEDIA_ROOT`.

Collect static files with:

```bash
python manage.py collectstatic
```

---

## Authentication Flow

The authentication system is based on phone numbers and OTP verification.

```text
User
 │
 ▼
Enter Phone Number
 │
 ▼
OTP Generation
 │
 ▼
SMS Provider
 │
 ▼
OTP Verification
 │
 ▼
Authenticated User
```

The custom user model uses `phone_number` as the authentication identifier.

---

## Shopping Flow

The primary shopping workflow is:

```text
Browse Products
      │
      ▼
Product Details
      │
      ▼
Add to Cart
      │
      ▼
Cart
      │
      ▼
Checkout
      │
      ▼
Discount Validation
      │
      ▼
Stock Validation
      │
      ▼
Payment
      │
      ▼
Payment Verification
      │
      ▼
Order Confirmation
      │
      ▼
Stock Reduction
```

---

## Payment Integration

The project integrates with ZarinPal for online payments.

The payment process consists of:

1. Calculating the final order amount
2. Validating the discount code
3. Validating product stock
4. Creating a payment request
5. Redirecting the customer to the payment gateway
6. Receiving the payment callback
7. Verifying the transaction
8. Updating the order payment status
9. Reducing product stock

Payment credentials and gateway URLs must be configured through environment variables.

---

## Order Management

Orders support the following statuses:

```text
cart
  │
  ▼
pending
  │
  ▼
shipped
  │
  ▼
delivered
```

The system also maintains:

* Payment status
* Payment timestamp
* Tracking code
* Shipping information
* Discount information
* Order items
* Product quantities
* Unit prices

---

## Security

The production configuration includes several Django security mechanisms:

* Environment-based secret configuration
* Secure session cookies
* Secure CSRF cookies
* HTTPS redirection
* HSTS
* HSTS preload
* HSTS subdomain protection
* Content-Type sniffing protection
* Browser XSS filtering
* SameSite cookies
* Proxy HTTPS detection
* Configurable allowed hosts

Sensitive configuration is intentionally kept outside the repository.

---

## Production Configuration

When running in production:

```env
DEBUG=False
```

The production configuration enables HTTPS-related security settings and uses dedicated filesystem paths for static and media files.

Before deployment, verify:

```bash
python manage.py check --deploy
```

Then collect static files:

```bash
python manage.py collectstatic
```

Database migrations should also be applied:

```bash
python manage.py migrate
```

---

## Admin Panel

The Django administration panel is available through a custom URL configured in the project settings.

The admin interface provides management capabilities for:

* Users
* Addresses
* Products
* Categories
* Brands
* Galleries
* Orders
* Order items
* Discount codes
* Reviews
* Blog content
* Site-related data

The production admin route should not be exposed unnecessarily and should be protected with strong credentials and appropriate access controls.

---

## Image Processing

Product images are processed automatically using Pillow.

The product image workflow includes:

* Image conversion
* WebP generation
* Automatic quality adjustment
* Maximum file-size control

This helps reduce image size while maintaining acceptable visual quality.

---

## Configuration

Project-level configuration is located in:

```text
config/
├── settings.py
├── urls.py
├── middleware.py
├── wsgi.py
└── asgi.py
```

Environment-specific values are loaded using `python-decouple`.

---

## Useful Commands

Run Django checks:

```bash
python manage.py check
```

Check deployment configuration:

```bash
python manage.py check --deploy
```

Apply migrations:

```bash
python manage.py migrate
```

Create migrations:

```bash
python manage.py makemigrations
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Collect static files:

```bash
python manage.py collectstatic
```

Run tests:

```bash
python manage.py test
```

Run the development server:

```bash
python manage.py runserver
```

---

## Development Guidelines

When contributing to the project:

1. Keep business logic inside the appropriate application.
2. Avoid hardcoding credentials or environment-specific configuration.
3. Keep database migrations under version control.
4. Do not commit `.env`, virtual environments, generated logs, or collected static files.
5. Validate stock and payment state before finalizing orders.
6. Use Django's built-in security mechanisms wherever possible.
7. Keep reusable functionality inside the `core` application.

---

## Project Status

The project is an actively developed Django-based e-commerce application with integrated authentication, product management, shopping cart, order processing, discount handling, online payment, customer dashboard, blog, reviews, and search functionality.

---

## License

This project is proprietary software.

Unauthorized copying, distribution, modification, or commercial use is not permitted without explicit permission from the project owner.
