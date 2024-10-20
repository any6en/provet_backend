from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import ping
from routers.directories import owner, animal_type, breed, patient
from routers.med import journal

from utils.utils import global_exception_handling, unicorn_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException


app = FastAPI(title="Provet Backend Server")

app.include_router(ping.worker, prefix=f'/api/directories', tags=["ping"])
app.include_router(owner.worker, prefix=f'/api/directories', tags=["owners"])
app.include_router(animal_type.worker, prefix=f'/api/directories', tags=["animal_types"])
app.include_router(breed.worker, prefix=f'/api/directories', tags=["breeds"])
app.include_router(patient.worker, prefix=f'/api/directories', tags=["patients"])
app.include_router(journal.worker, prefix=f'/api', tags=["journal"])


# Обработка HTTPException в контроллерах.
app.exception_handler(StarletteHTTPException)(unicorn_exception_handler)

# Любое не отслеживаемое исключение - 500: Internal Server Error.
app.middleware("http")(global_exception_handling)

# Включение CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
