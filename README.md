# doctor-django-app

App consist of Rest API using Django Rest Framework.

Following are the features available in this app:
- The doctor should be able to create an account using these informations :  email, phone password, bithdate, gender,location,spoken languages,Diplomas,picture.
- The doctor should be able to select many spoken languages
- The doctor should be able to log using a password (Two factor authentication is a plus)
- The doctor should be able to modify his infomations  
- The doctor should be able to add a patient with his first and last name ,birthdate, email .
- The doctor should be able to list all his patients  

This repository contains the django-rest-framework project which provides all the core logic and back-end for the doctor-django-app.

### How to run the project?

- Create a virtual environment

  - ```bash
    python3 -m venv doctor_app_venv
    ```

- Activate newly created environment
    - ```bash
      source doctor_app_venv\bin\activate
      ```

- Navigate to the directory

  - ```shell
    cd doctor-django-app
    ```

- Install the required packages

  - ```bash
    pip install -r requirements.txt
    ```

- Change the database settings in `appointment/settings.py`

- Setting up your privacy using environment variables
Create ```.env``` file and set below variables based on your configuration
     - ```shell
        PG_USERNAME=user_name_value
        PG_PASSWORD=user_password
        PG_HOST=server_host
        PG_PORT=server_port
        PG_DATABASE_NAME=database_name
        ```

- Run migrations

  - ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
  Note: You can skip ```python manage.py makemigrations``` command if you don't change anything in models.

- Start server

  - ```
    python manage.py runserver 0.0.0.0:8000
    ```

- Test the server with postman collection or install front-end and test.

  - Postman collection: [Import collection link](https://www.getpostman.com/collections/0352c931ecc8c7bad19d)