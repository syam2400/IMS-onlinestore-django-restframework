Online Store Inventory Management System - Api

Welcome to the Online Store Inventory Management System, a robust solution for managing products, variants, and stock levels in an online store. Built using Django and Django REST Framework, this project provides a set of RESTful APIs to create, list, and manage products, offering a seamless experience for integrating with frontend applications.

Features
Product Management: Create products with multiple variants and sub-variants.
Stock Management: Efficiently add and remove stock for specific product variants.
Comprehensive Logging: Monitor API usage and capture errors.
Optimized Performance: Efficient database queries and pagination support for large datasets.

Follow these steps to set up the project locally:

Clone the repository:

bash
Copy code
git clone https://github.com/syam2400/IMS-onlinestore-django-restframework.git
cd IMS-onlinestore-django-restframework
Create a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies:

pip install -r requirements.txt
Run database migrations:

python manage.py migrate
Create a superuser:

python manage.py createsuperuser
Start the development server:

python manage.py runserver
Access the application at http://127.0.0.1:8000/admin to explore the Django admin panel.

Usage
The application allows you to manage an online store's inventory with ease. The provided APIs enable seamless integration with other systems, making it possible to build comprehensive e-commerce solutions.

API Endpoints
1. Create Product
Endpoint: /products/create/
Method: POST
Description: Create a new product with variants and sub-variants.
Request Payload:

2. List Products
Endpoint: /products/
Method: GET
Description: Retrieve a list of all available products.

4. Add Stock (Purchase)
Endpoint: /add-products/
Method: POST
Description: Add stock for a specific product variant.
Request Payload:

5. Remove Stock (Sale)
Endpoint: /products/remove-stock/
Method: POST
Description: Remove stock for a specific product variant.
Request Payload:

Validation and Error Handling
The system includes robust validation to ensure that all required fields are present in the request payloads. Error handling mechanisms are implemented to gracefully handle invalid requests and database errors.

Validation Errors: HTTP 400 Bad Request
Database Errors: HTTP 500 Internal Server Error
Logging
Logging is implemented to track API usage and errors, aiding in monitoring and debugging. Log entries include:

Info Logs: Successful API requests
Error Logs: Failed requests and exceptions

Contributing
We welcome contributions to this project. To contribute, please fork the repository and create a pull request with your changes. Ensure that your code follows the project's coding standards and includes necessary tests.
For any questions or issues, feel free to open an issue on GitHub or contact the repository maintainer. Happy coding!
