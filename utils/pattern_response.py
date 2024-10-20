from pydantic import BaseModel, ConfigDict

""" Формат ответов справочников
GET: Возврат всех записей
{
    response: {
        records: int,
        rows: []
    }
}
GET: Возврат выбранной по Id
{
    response: {
        object.dict()
    }
}
POST: Создание новой записи
{
    response: {
        object.dict()
    }
}
PATCH: Создание новой записи
{
    response: {
        object.dict()
    }
}
DELETE: Создание новой записи
{
    response: {
        object.dict()
    }
}

GET /owners
200 OK: Return a list of owners
404 Not Found: If no owners are found

GET /owners/{id}
200 OK: Return the owner with the specified ID
404 Not Found: If the owner with the specified ID is not found

POST /owners
201 Created: Return the newly created owner
400 Bad Request: If the request body is invalid or missing required fields
409 Conflict: If an owner with the same ID already exists

DELETE /owners/{id}
204 No Content: If the owner is successfully deleted
404 Not Found: If the owner with the specified ID is not found

PATCH /owners/{id}
200 OK: Return the updated owner
404 Not Found: If the owner with the specified ID is not found
400 Bad Request: If the request body is invalid or missing required fields

"""
class APIResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    response: object

