# 🛒 Personal E-Commerce Website

[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A full-featured e-commerce platform built with Django, featuring user authentication, product management, shopping cart, order processing, and an admin dashboard.

## ✨ Features

### 🛍️ Customer Features
- **User Registration & Authentication**: Secure login and signup with role-based access (Admin/Customer)
- **Product Browsing**: Browse products by categories with detailed product pages
- **Shopping Cart**: Add, update, and remove items from cart
- **Wishlist**: Save favorite products for later
- **Order Management**: Place orders, track order history, and view order details
- **Reviews & Ratings**: Leave reviews and ratings for products
- **Contact Support**: Send messages to administrators
- **Coupon System**: Apply discount coupons during checkout

### 👨‍💼 Admin Features
- **Dashboard**: Overview of sales, orders, and users
- **Product Management**: Add, edit, and delete products and categories
- **Order Management**: View and update order statuses
- **User Management**: Manage customer accounts
- **Message Handling**: Respond to customer inquiries
- **Analytics**: Monitor site performance and sales

## 🛠️ Tech Stack

- **Backend**: Django 6.0
- **Database**: SQLite (development), PostgreSQL (production recommended)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Image Handling**: Pillow
- **Static Files**: WhiteNoise
- **Deployment**: Gunicorn
- **Other**: Django Admin, Authentication, Sessions

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/mdzihad42/personal-e-commarce-website.git
   cd personal-e-commarce-website
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📖 Usage

### For Customers
1. Register an account or login
2. Browse products and add to cart
3. Proceed to checkout and place orders
4. Track orders in your dashboard
5. Leave reviews for purchased products

### For Admins
1. Login to admin panel
2. Manage products, categories, and orders
3. Respond to customer messages
4. Monitor site analytics

## 📁 Project Structure

```
personal-e-commarce-website/
├── ecommarce/                 # Django project settings
├── myapp/                     # Main Django app
│   ├── models.py             # Database models
│   ├── views.py              # View functions
│   ├── templates/            # HTML templates
│   ├── static/               # Static files (CSS, JS, images)
│   └── migrations/           # Database migrations
├── media/                    # User-uploaded files
├── staticfiles/              # Collected static files
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🔧 Configuration

### Environment Variables
For production deployment, set the following environment variables:
- `DEBUG=False`
- `SECRET_KEY=your-secret-key`
- `DATABASE_URL=your-database-url`

### Database
The project uses SQLite by default. For production, consider switching to PostgreSQL.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

For questions or support, please contact the project maintainer.

---

⭐ If you find this project helpful, please give it a star!
