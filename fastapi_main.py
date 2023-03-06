from fastapi import FastAPI
import admin.infrastructure.adminapi_fastapi as adminapi
import product.infrastructure.productapi_fastapi as productapi
import product.infrastructure.anonymous_user_api as anonymousapi
import login.infrastructure.login_user_api_fastapi as loginapi

app = FastAPI()

app.include_router(adminapi.router)
app.include_router(productapi.router)
app.include_router(anonymousapi.router)
app.include_router(loginapi.router)


