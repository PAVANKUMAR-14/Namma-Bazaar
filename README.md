# About this project

Namma Bazaar is an e-commerce application built with Python Django Framework. Some of the features of this project includes custom user model, categories and products, Carts, Incrementing, Decrementing and removing car items, Unlimited Product image gallery, Orders, Payments, after-order functionalities such as reduce the quantify of sold products, send the order received email, clearing the cart, Order completion page as well as generating an invoice for the order. Also we have a Review and Rating system with the interactive rating stars that even allows you to rate a half-star rating. My account functionalities for the customer who can easily edit his profile, profile pictures, change his account password, and also manage his orders and much more.

## Features

### Authentication and Security
- **Token-Based User Authentication**: Ensures secure user access to the platform by generating and validating tokens.
- **Account Verification**: Upon registration, new users receive an email with a verification link. Clicking this link confirms their account.
- **Forget Password and Reset Password**: Users can securely reset their passwords via email using token-based authentication.

### Shopping Cart and Payment
- **Shopping Cart Management**: Users can add items to their cart, remove items, and adjust quantities as needed before checkout.
- **Payment Confirmation**: After successful payment, users receive an automated email containing their order number for reference.

### User Experience
- **User-Friendly Profile Dashboards**: Provides users with a comprehensive dashboard to manage their profiles, view order history, and also to change passwords.

## Installation instructions 

1. Clone the repository [Click here to clone](
https://github.com/PAVANKUMAR-14/Namma-Bazaar.git)
2. Navigrate to the working directory `cd Namma_bazaar`
3. Open the project from the code editor `code .` 
4. Create virtual environment `python -m venv django`
5. Activate the virtual environment `source django/Scripts/activate`
6. Install required packages to run the project `pip install -r requirements.txt`
7. Rename _.env-sample_ to _.env_
8. Fill up the environment variables:
    _Generate your own Secret key using this tool [https://djecrety.ir/](https://djecrety.ir/), copy and paste the secret key in the SECRET_KEY field._

    _Your configuration should look something like this:_
    ```sh
    SECRET_KEY=47d)n05#ei0rg4#)*@fuhc%$5+0n(t%jgxg$)!1pkegsi*l4c%
    DEBUG=True
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_HOST_USER=youremailaddress@gmail.com
    EMAIL_HOST_PASSWORD=yourStrongPassword
    EMAIL_USE_TLS=True
    ```
    _Note: If you are using gmail account, make sure to [use app password](https://support.google.com/accounts/answer/185833)_
9. Create database tables
    ```sh
    python manage.py migrate
    ```
10. Create a super user
    ```sh
    python manage.py createsuperuser
    ```
    _GitBash users may have to run this to create a super user - `winpty python manage.py createsuperuser`_
11. Run server
    ```sh
    python manage.py runserver
    ```
12. Login to admin panel - (`http://127.0.0.1:8000/securelogin/`)
13. Add categories, products, add variations, register user, login, place orders and EXPLORE SO MANY FEATURES

## Technologies Used

- Python
- Django
- HTML/CS
- Bootstrap 
- JavaScript
- SQLite (by default, but can be configured for other databases like PostgreSQL)

## Credits

This project was developed by Pavan Kumar.
