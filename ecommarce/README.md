# E-Commerce Website

A Django-based e-commerce platform with user authentication, product management, shopping cart, and admin panel.

## Features

- User registration and login
- Product browsing and search by category
- Shopping cart and wishlist functionality
- Order placement and history
- Admin panel for product management (add/edit/delete)
- Role-based access control (admin/customer)
- Responsive design with Bootstrap

## Installation

1. Clone the repository:
   ```
   git clone <your-repo-url>
   cd ecommarce
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. Install dependencies:
   ```
   pip install django
   # Add other dependencies as needed (e.g., Pillow for image handling)
   ```

4. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser for admin access:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the website at http://127.0.0.1:8000/

## Admin Setup

- **Django Admin**: Access at `/admin/` with superuser credentials. Use this to manage users, categories, and initial data.
- **Custom Admin Panel**: Login as admin user, then access `/admin-panel/dashboard/` for product management.
- **Adding Products**: First add categories via Django admin, then use the custom admin panel to add/edit/delete products.

## Usage

### For Customers:
- Register or login at the site
- Browse products on the home page or shop page
- Filter products by category
- View product details, add to cart or wishlist
- Proceed to checkout and place orders
- View order history in dashboard

### For Admins:
- Access admin dashboard at `/admin-panel/dashboard/`
- Manage products: add new, edit existing, delete products
- View orders and update status
- Manage users

## Project Structure

- `ecommarce/`: Django project settings
- `myapp/`: Main application
  - `models.py`: Database models (UserProfile, Category, Product, etc.)
  - `views.py`: View functions for pages and logic
  - `forms.py`: Django forms for product management
  - `templates/`: HTML templates
  - `static/`: CSS and other static files
- `db.sqlite3`: SQLite database
- `manage.py`: Django management script

## TODO

See `TODO.md` for a list of planned features and improvements.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test
4. Submit a pull request

## License

This project is for educational purposes. Modify and use as needed.
