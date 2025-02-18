# Backend Development & API Integration 

## Objective: Develop a REST API to manage user data.

This project defines two SQLAlchemy models:

- User: Represents users in the system with authentication-related properties.
- TokenBlocklist: Stores revoked authentication tokens to prevent reuse.

These models enforce data integrity with constraints and validations while maintaining a secure authentication system.

## How To Run on Docker

1. On a new terminal session, switch to task1 folder.
2. In the task1 folder, define your env variables following example on .env.example:
    ```bash
    FLASK_APP=app
    FLASK_DEBUG=True
    FLASK_RUN_PORT=8000
    FLASK_RUN_HOST=0.0.0.0
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=password
    POSTGRES_DB=db_name
    SQLALCHEMY_DATABASE_URI=postgresql://user:password@db:5432/db_name
    JWT_SECRET_KEY=secret_string
    ```
3. Run docker-compose with both building the image and starting the services.
    ```bash
    docker-compose --env-file .env up --build
    ```
4. The api runs on port 8000, adminer (db data viewer runs on port 8080)
    N/B;- User can view any other user details but can only update or delete own details

    ```bash
    Create new user: POST /api/v1/auth/register

    {
      "name": "Juliet Ross",
      "email": "juliet.ross@gmail.com",
      "role": "admin",
      "password": "Kpass2000$"
    }

    ```
    ```bash
    Login for access token: POST /api/v1/auth/login

    {
      "email": "juliet.ross@gmail.com",
      "password": "Kpass2000$"
    }

    ```

    ```bash
    Retrieve user details: GET /api/v1/users/<uuid:id>
    ```
    ```bash
    Update user details: PUT /api/v1/users/<uuid:id>
    ```
    ```bash
    Remove user: DELETE /api/v1/users/<uuid:id>
    ```

  - To retrieve, update and delete user details, user must be authenticated, so first login to get the access token

  <img width="1557" alt="Image" src="https://github.com/user-attachments/assets/a11f17b8-8afa-493b-9353-e74bb319c8a5" />

  - Copy access token then add to headers for authentication

  <img width="1557" alt="Image" src="https://github.com/user-attachments/assets/4af58ae1-ec87-45bf-943a-e060db50e5b6" />

5. To configure adminer and view the db data, on a browser navigate to localhost:8080
    - Login with your db details

    <img width="1628" alt="Image" src="https://github.com/user-attachments/assets/72c31216-7844-4173-940b-ee67530c46e4" />

    - Select table from dashboard view

    <img width="1628" alt="Image" src="https://github.com/user-attachments/assets/049797c4-9be9-4a5f-9ae8-4e7a1d0d422d" />

    - View table data

    <img width="1628" alt="Image" src="https://github.com/user-attachments/assets/bdc84ffd-8f70-4276-8698-24dbccd7d0da" />