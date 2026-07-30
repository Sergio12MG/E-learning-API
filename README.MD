# E-Learning platform - FastAPI

## General description
This system was developed using FastAPI, structured by the hexagonal arquitecture and best code practices.

> Note: You will need to have Docker Compose in your machine. Otherwise, look at the instructions below.

## Project structure
### 🏠 Main
- 📁 **Domain:** Contains models and ports to implement in the repositories.
- 📁 **Application:** Services for each use case and data validators.
- 📁 **Infraestructure:**
    - Adapters:
        - Input: Routers, Pydantic schemas and dependencies.
        - Output: Repositories.
    - DB:
        - Alembic folder.
        - Models for the database.
        - File to configure the connection and session to the database.
- 📁 **Utils:** Auth, middlewares and custom response model for endpoints.

- **Main file:**
Include the following values to run the API
    - Host: 127.0.0.1
    - Port: 8000
    - Reload: True
---

### Execution using Docker:
- First step
```powershell
(env) ...\E-Learning\backend>docker-compose up --build
```
- Execution of migrations (in another console)
```powershell
(env) ...\E-Learning\backend>docker-compose exec api alembic upgrade head
```
---
### Execution without Docker
> Within the virtual environment, run **pip install -r requirements.txt**

### 1. Create a new migration
```powershell
(env) ...\E-Learning\backend>alembic revision --autogenerate -m "Migration description"
```
If need to revert the last migration:
```powershell
(env) ...\E-Learning\backend>alembic downgrade -1
```

### 2. Apply the migrations to the database
```powershell
(env) ...\E-Learning\backend>alembic upgrade head
```

### 3. Command to run the API
```powershell
(env) ...\E-Learning\backend>py -m src.main.main
```
---
