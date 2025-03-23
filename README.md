# E-commerce Management System

A Django-based system for managing e-commerce operations including products, purchase orders, and invoices.

## Features

- **Product Management**
  - Track products with SKU, name, and unit price
  - Search and filter products in admin interface

- **Purchase Order System**
  - Create and manage purchase orders with vendors
  - Track order status (Pending, Completed, Canceled)
  - Calculate order totals automatically

- **Invoice Management**
  - Generate and track customer invoices
  - Status tracking (Paid, Unpaid, Overdue)
  - Automatic overdue calculation
  - Export invoices to Excel
  - Professional print-ready invoice templates

## Installation

1. Clone the repository:
```bash
git clone https://github.com/milliondejene/ecommerce_mgmt.git
cd ecommerce_mgmt
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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

## Usage

1. Access the admin interface at `http://localhost:8000/admin`
2. Log in with your superuser credentials
3. Manage products, purchase orders, and invoices through the admin interface

### Invoice Features

- **Excel Export**: Select invoices and use the "Export to Excel" action
- **Print View**: Click the "Print" button for a print-ready invoice view
- **Overdue Tracking**: System automatically calculates and displays overdue days
- **Status Management**: Mark invoices as paid/unpaid and track overdue status

## Dependencies

- Django 5.0.3
- openpyxl 3.1.5 (for Excel export)
- python-dotenv 1.0.1

## Project Structure

```
ecommerce_mgmt/
├── store/                  # Main application
│   ├── models.py          # Data models
│   ├── admin.py           # Admin interface
│   ├── views.py           # Views
│   └── templates/         # HTML templates
├── exports/               # Excel exports directory
└── requirements.txt       # Project dependencies
```

## License

MIT License
