# Project Setup Guide

This README provides instructions on setting up the hospital management system project. Follow these steps to get the project up and running quickly.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python (preferably version 3.x)
- pip (Python package installer)
- venv (optional but recommended for isolating project dependencies)

## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/KeneNwogu/hospital-management-system.git
    ```

2. **Create a Virtual Environment (optional but recommended):**

   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

   Deactivate the virtual environment:

   ```bash
   deactivate
   ```
   
3. **Install Project Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
   
4. **Database Setup:**
- Ensure you have a PostgreSQL database server installed.
- Create a new database in your PostgreSQL server.
- Update the database settings in `.env` according to your database configuration.
- Use `.env.example` as a template for creating your `.env` file.

   ```bash
   DB_NAME=hospital_management
   DB_USER=your_database_username
   DB_PASSWORD=your_database_password
   DB_HOST=localhost
   DB_PORT=5432
   SECRET_KEY=testsecretkey
   ``

5. **Run Migrations:**

   ```bash
   python manage.py migrate
   ```
6. **Create a Superuser:**

   ```bash
    python manage.py createsuperuser
    ```
7. **Run the Development Server:**

   ```bash
   python manage.py runserver
   ```
8. **Access the Application:**
9. Visit `http://127.0.0.1:8000` in your web browser to view the application.
10. Log in with the superuser credentials created in step 6.
11. You can now use the admin dashboard to create dummy hospital data.
12. ## Accessing the GraphQL API
13. Visit `http://127.0.0.1:8000/graphql` in your web browser to access the GraphQL API.
14. You can use the GraphiQL interface to interact with the API and perform queries and mutations.
15. ## Example Queries and Mutations
16. Here are some example queries and mutations you can perform using the GraphQL API:
17. **Query to Get All Hospitals:**
```graphql
        query {
            hospitals{
              id
              name
              email
              address
              capacity
              website
              phoneNumber
            }
        }
```
18. **Query to get Hospital by ID:**
```graphql
        query {
             getHospital(id: "cc606339-0f73-4fc7-aa3f-656bc70c2f60"){
              id
              name
              email
              address
              capacity
              website
              phoneNumber
            }
        }
```

## Authentication
Simple jwt authentication was added to the project. To access the graphql api, you need to obtain a token by using the login mutation. Here is an example of how to obtain a token:

```graphql
mutation {
    login(username: "your_username", password: "your_password") {
        token
    }
}
  ```
Replace `your_username` and `your_password` with your superuser credentials. The token will be returned in the response. 
You can then use this token to authenticate your requests by adding it to the Authorization header in the format `Bearer <token>`.
    
```graphql
    {
        "Authorization": "Bearer <token>"
    }
   ```

The token can be used to access the protected mutation endpoint `createHospital`. 
Here is an example of how to use the mutation to create a new hospital:

```graphql
createHospital(
    input: {name: "Newest Hospital", email: "kcee@dev.com", address: "Moluwe", phoneNumber: "08052218036", capacity: 1000, website: "kcee.com"}
  ) {
    hospital {
      id
      phoneNumber
      capacity
      name
    }
  }
```