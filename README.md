# FastAPI PostgreSQL CRUD

A FastAPI application with PostgreSQL demonstrating CRUD operations, Pydantic validation, and database integration.

## Project Overview

This project is created to practice backend development using FastAPI and PostgreSQL.

The application provides APIs to create, retrieve, update, and delete customer records stored in a PostgreSQL database.

## Technologies Used

1.Python
2.FastAPI
3.Pydantic
4.PostgreSQL
5.psycopg2
6.Uvicorn
7.python-dotenv

## Features

* Get all customers

* Get a customer by ID

* Create a new customer

* Update a customer using PUT

* Partially update a customer using PATCH

* Delete a customer

* Request validation using Pydantic

* PostgreSQL database integration

* Environment variables for database configuration

* Transaction handling using commit and rollback

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /customers | Get all customers |
| GET | /get_customer/{customer_id} | Get a customer by ID |
| POST | /create_customer | Create a customer |
| PUT | /update_customer/{customer_id} | Update a customer |
| PATCH | /update_customer/{customer_id} | Partially update a customer |
| DELETE | /delete_customer/{customer_id} | Delete a customer |

## Project Structure

fastapi/
    
    crud_operations.py
    
    db.py
    
    .env
    
    .gitignore
    
    README.md
    
    requirements.txt

## Database

The application uses PostgreSQL as the database.

The customers table contains the following fields:

* customer_id

* customer_name

* email

* city

* registration_date

## Environment Configuration

Create a `.env` file in the project directory.

```env
DB_HOST=localhost
DB_NAME=company_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
