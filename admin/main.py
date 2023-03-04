from fastapi import FastAPI
import admin.infrastructure.adminapi_fastapi as adminapi
app = FastAPI()

app.include_router(adminapi.router)