from fastapi import FastAPI
import admin.infrastructure.adminapi_fastapi as adminapi
import product.infrastructure.productapi_fastapi as productapi
app = FastAPI()

app.include_router(adminapi.router)
app.include_router(productapi.router)