from fastapi import FastAPI
import uvicorn

from src.main.utils.middlewares import ErrorMiddlewareAPI
from src.main.infraestructure.adapters.input.routers.user_router import router as users_router
from src.main.infraestructure.adapters.input.routers.course_router import router as courses_router
from src.main.infraestructure.adapters.input.routers.auth_router import router as auth_router

app = FastAPI(title="API de E-Learning", version="1.0.0")

app.add_middleware(ErrorMiddlewareAPI)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(courses_router)

@app.get("/")
def inicio():
    return {"mensaje": "Hola mundo"}

# Execution
if __name__ == "__main__":
    uvicorn.run("src.main.main:app", host="127.0.0.1", port=8000, reload=True)
