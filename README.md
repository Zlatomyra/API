# Laboratory Work №2

## Implementation of REST API

### Author

Student: **Zlatomyra Severylova**
University: **Ivan Franko National University of Lviv**
Specialty: **System Analysis**

---

# Project Description

This project implements a **REST API** for a simple **Real Estate Management System**.
The API allows users to manage real estate properties and reviews.

The system includes several entities with relationships and supports full **CRUD operations**.
Additionally, the API provides functionality for:

* pagination
* sorting
* filtering
* automatic API documentation using Swagger

The project is implemented using the **FastAPI framework** in Python.

---

# Technologies Used

* **Python 3**
* **FastAPI**
* **Pydantic**
* **Uvicorn**

These technologies were chosen because they provide a simple way to develop high-performance APIs and automatically generate API documentation.

---

# System Entities

The system contains **three main entities**:

## 1. User

Represents a user of the system who can add properties and leave reviews.

Fields:

* `id` – unique identifier
* `name` – user name
* `email` – email address

Relationship:

* One user can create multiple properties.
* One user can leave multiple reviews.

---

## 2. Property

Represents a real estate object that can be listed in the system.

Fields:

* `id` – unique identifier
* `title` – property title
* `price` – property price
* `owner_id` – identifier of the user who owns the property

Relationship:

* One property belongs to one user.
* One property can have multiple reviews.

---

## 3. Review

Represents a review left by a user for a property.

Fields:

* `id` – unique identifier
* `property_id` – identifier of the property
* `user_id` – identifier of the user who wrote the review
* `rating` – rating value
* `comment` – review text

Relationship:

* Each review belongs to one property.
* Each review is created by one user.

---

# API Features

The API provides the following functionality:

### CRUD Operations

For each entity the following operations are implemented:

* **Create**
* **Read**
* **Update**
* **Delete**

HTTP methods used:

* `GET` – retrieve data
* `POST` – create new records
* `PUT` – update existing records
* `DELETE` – remove records

---

# Pagination

Pagination allows retrieving data in smaller portions.

Example request:

```
GET /properties?page=1&limit=5
```

Parameters:

* `page` – page number
* `limit` – number of items per page

---

# Sorting

Sorting allows ordering the data by specific fields.

Example:

```
GET /properties?sort_by=price
```

This request returns properties sorted by price.

---

# Filtering

Filtering allows selecting only data that meets certain conditions.

Example:

```
GET /properties?min_price=50000
```

This request returns only properties with price greater than or equal to 50000.

---

# API Endpoints

## User Endpoints

Create user

```
POST /users
```

Get all users

```
GET /users
```

Get user by ID

```
GET /users/{user_id}
```

Update user

```
PUT /users/{user_id}
```

Delete user

```
DELETE /users/{user_id}
```

---

## Property Endpoints

Create property

```
POST /properties
```

Get properties (with pagination, sorting, filtering)

```
GET /properties
```

Get property by ID

```
GET /properties/{property_id}
```

Delete property

```
DELETE /properties/{property_id}
```

---

## Review Endpoints

Create review

```
POST /reviews
```

Get all reviews

```
GET /reviews
```

Get reviews for a specific property

```
GET /properties/{property_id}/reviews
```

---

# Running the Project

## 1. Clone the repository

```
git clone https://github.com/yourusername/lab2-api.git
cd lab2-api
```

## 2. Install dependencies

```
pip install fastapi uvicorn
```

## 3. Run the server

```
uvicorn main:app --reload
```

The server will start at:

```
http://127.0.0.1:8000
```

---

# API Documentation (Swagger)

FastAPI automatically generates interactive API documentation.

Swagger documentation is available at:

```
http://127.0.0.1:8000/docs
```

Alternative documentation:

```
http://127.0.0.1:8000/redoc
```

This documentation allows testing all API endpoints directly in the browser.

