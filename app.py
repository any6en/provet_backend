from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

import tr

from routers import ping
from routers.directories import owner, animal_type, breed, patient, primary_visit, repeat_visit, user
from routers import auth
from routers.med import journal
from routers import document_generator

from utils.utils import global_exception_handling


app = FastAPI(title="Provet Backend Server")

app.include_router(auth.worker, prefix=f'/auth', tags=["ping"])
app.include_router(ping.worker, prefix=f'/api/directories', tags=["ping"])
app.include_router(user.worker, prefix=f'/api/directories', tags=["users"])
app.include_router(owner.worker, prefix=f'/api/directories', tags=["owners"])
app.include_router(animal_type.worker, prefix=f'/api/directories', tags=["animal_types"])
app.include_router(breed.worker, prefix=f'/api/directories', tags=["breeds"])
app.include_router(patient.worker, prefix=f'/api/directories', tags=["patients"])

app.include_router(primary_visit.worker, prefix=f'/api/directories', tags=["primary_visits"])
app.include_router(repeat_visit.worker, prefix=f'/api/directories', tags=["repeat_visits"])


app.include_router(journal.worker, prefix=f'/api', tags=["journal"])
app.include_router(document_generator.worker, prefix=f'/api', tags=["document_generator"])


# Обработка HTTPException в контроллерах.
#app.exception_handler(RequestValidationError)(unicorn_exception_handler)
app.add_exception_handler(RequestValidationError, tr.validation_exception_handler)


# Любое не отслеживаемое исключение - 500: Internal Server Error.
app.middleware("http")(global_exception_handling)


# Включение CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
