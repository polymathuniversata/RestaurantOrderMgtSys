# Restaurant Order Management System

A RESTful API for managing restaurant orders, built with Django and Django REST Framework.

## Features

- User authentication (JWT)
- Restaurant and customer profiles
- Menu management
- Order processing
- Admin dashboard

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/RestaurantOrderMgtSys.git
   cd RestaurantOrderMgtSys
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Documentation

Access the API documentation at:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Project Structure

```
restaurant_order_system/
├── accounts/           # User authentication and profiles
├── menu/               # Menu management
├── orders/             # Order processing
└── restaurant_order_system/  # Project configuration
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
