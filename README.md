# CW2-COMP2001-Information-Management-Retrieval-WenAlvin
This repository contains the implementation of the TrailService micro-service, part of a data-driven well-being trail application. It provides RESTful API endpoints for managing trails (CRUD operations), locations, and user authentication, integrated with an external authenticator API. The service uses Python with Flask, Connexion for OpenAPI-driven routing, SQLAlchemy for ORM, and Marshmallow for validation. Data is stored in a Microsoft SQL Server database.

The project adheres to the assignment requirements, including RESTful principles, JSON output, OWASP mitigations, and deployment on university servers (web.socem.plymouth.ac.uk for the API, dist-6-505.uopnet.plymouth.ac.uk for the DB).
Features

    Trail Management: Create, read, update, and delete trails with attributes like name, description, length, difficulty, estimated time, and features.
    Location Management: Add, retrieve, update, and delete GPS points associated with trails.
    Authentication: Integrates with the external API at https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users for verification, generating local JWT tokens for secure access.
    Role-Based Access: Owners/admins can modify data; limited views for others.
    Swagger UI: Auto-generated API documentation and testing interface.
    Database Views and Procedures: Includes stored procedures for CRUD and a view for combined trail details.

Prerequisites

    Python 3.8+
    Microsoft SQL Server (hosted on dist-6-505.uopnet.plymouth.ac.uk)
    Libraries: connexion[swagger-ui], flask, flask-sqlalchemy, flask-marshmallow, marshmallow-sqlalchemy, pyodbc, pyjwt, requests, pytz
    for more requirements refer to requirements.txt

Installation

    Clone the repository:

    git clone https://github.com/yourusername/trailservice-repo.git
    cd trailservice-repo

    Create a virtual environment and install dependencies:
    basic

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt

    Set up the database:
        Connect to dist-6-505.uopnet.plymouth.ac.uk using SSMS or similar.
        Create schema 'CW2' and run SQL scripts for tables, procedures, views, and sample data (e.g., from db_scripts.sql if available).
        Update config.py with your DB credentials (UID, PWD).

    Configure environment variables (e.g., SECRET_KEY for JWT in trails.py).

Running the Application

    Start the server:

    python app.py

        The API runs on http://localhost:8000 (or 0.0.0.0:8000 for network access).
        Swagger UI is available at http://localhost:8000/api/ui.

    For deployment on web.socem.plymouth.ac.uk:
        Use Gunicorn: gunicorn -w 4 -b 0.0.0.0:8000 app:app.
        Configure Nginx as a reverse proxy if needed.

Usage
Authentication

    POST /api/auth/login with JSON body { "email": "tim@plymouth.ac.uk", "password": "COMP2001!" } to get a JWT token.
    Include Authorization: Bearer <token> in headers for protected endpoints.

API Endpoints

Refer to swagger.yml for full details. Key examples:

    GET /api/trails: Retrieve all trails.
    POST /api/trails: Create a trail (body: e.g., { "Name": "New Trail", "Description": "Test" }).
    GET /api/trails/{name}: Get trail by name (URL-encode spaces, e.g., /trails/Test%20Trail).
    POST /api/locations: Add location (body: e.g., { "TrailID": 1, "Latitude": 50.41, "Longitude": -4.09, "SequenceOrder": 1 }).
    GET /api/locations/{location_id}: Get location by ID.

See models.py for schema details and trails.py/locations.py for handler logic.
Database ERD

An Entity-Relationship Diagram (ERD) for the schema:
mermaid

erDiagram
    USER ||--o{ TRAIL : owns
    TRAIL ||--o{ LOCATION : has

    USER {
        int UserID PK
        string Email UK
        string UserName
        string Role
    }

    TRAIL {
        int TrailID PK
        string Name
        text Description
        int ElevationGain
        float Length
        string RouteType
        int EstimatedTime
        string Features
        int OwnerID FK
        datetime CreatedDate
    }

    LOCATION {
        int LocationID PK
        int TrailID FK
        float Latitude
        float Longitude
        int SequenceOrder
    }

Testing

    Use Postman or Swagger UI for endpoint testing.
    Example: Authenticate, create a trail, add locations, and verify via GET.
    Database tests: Query tables post-operations to confirm integrity.

Contributing

Fork the repo and submit pull requests for improvements.
License

MIT License - see LICENSE for details.

For more details, refer to the report sections on design, implementation, and evaluation.