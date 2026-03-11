# E-Learning platform - FastAPI

## General description
This system was developed using FastAPI, structured by the hexagonal arquitecture and best code practices.

> Within the virtual environment, run **pip install -r requirements.txt**

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

### Command to run
```powershell
(env) ...\E-Learning\backend>py -m src.main.main
```

---

