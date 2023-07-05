import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from endpoints.metadata import tags_metadata
from endpoints.users import users_router
from endpoints.photos import photos_router
from endpoints.admins import admin_router
from endpoints.login import login_router


app = FastAPI(openapi_tags=tags_metadata)
app.include_router(users_router)
app.include_router(photos_router)
app.include_router(login_router)
app.include_router(admin_router)
app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8080,
        reload=True
    )

