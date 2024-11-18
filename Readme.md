FASTAPI USER MANAGEMENT SERVICE
=================================

Overview
--------
This project is a REST API built using FastAPI for user management. It supports the following functionality:
- User registration
- User login
- Password recovery
- CORS setup for secure frontend communication

Features
--------
1. User Registration: Allows users to register by providing a username, email, and password.
2. User Login: Validates user credentials and generates an access token.
4. Password Recovery: Allows users to update their password using their username/email and old password.
5. CORS: Configured to allow frontend interaction.

Backend Setup Instructions
------------------

**Prerequisites**
- Python 3.8+
- pip
- Virtual Environment Tool (optional but recommended)
- PostgreSQL or any database supported by SQLAlchemy

1. Clone the Repository
------------------------
Run the following command:
    git clone https://github.com/Amit42373/Assignment_-FastAPI-
    cd Assignment_-FastAPI-

2. Setup a Virtual Environment (Optional)
-----------------------------------------
Run the following command:
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows

3. Install Dependencies
------------------------
Run the following command:
    pip install -r requirements.txt

4. Environment Configuration
-----------------------------
Create a `.env` file in the root directory for database credentials and JWT secret key.

Example `.env` file:
    SECRET_KEY=your_jwt_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

6. Run the Application
-----------------------
Start the FastAPI application using Uvicorn:
    uvicorn app.auth:app --reload
- The API will be available at: http://127.0.0.1:8000


Frontend Setup Instructions
---------------------------

**Prerequisites**
- Python 3.8+
- Streamlit (`pip install streamlit`)
- Backend FastAPI running at `http://127.0.0.1:8000`

2. Run the Streamlit Application
--------------------------------
Start the Streamlit application:
    streamlit run app.py
- The frontend will be available at: http://localhost:8501


Usage
-----

1. Register a User
------------------
- Endpoint: /register
- Method: POST
- Body:
    {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "password": "securepassword"
    }

2. Login a User
---------------
- Endpoint: /login
- Method: POST
- Body:
    {
        "username": "johndoe",
        "password": "securepassword"
    }

4. Password Recovery
--------------------
- Endpoint: /recover-password
- Method: POST
- Body:
    {
        "username_or_email": "johndoe",
        "old_password": "securepassword",
        "new_password": "newsecurepassword"
    }

CORS Configuration
-------------------
CORS is enabled via `CORSMiddleware` to allow requests from specific frontends. The configuration is:
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8501"],  # Frontend domains
        allow_credentials=True,
        allow_methods=["*"],  # All HTTP methods
        allow_headers=["*"],  # All headers
    )

License
-------
This project is licensed under the MIT License.
