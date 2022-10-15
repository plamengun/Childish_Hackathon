from fastapi import FastAPI
from routers.users import users_router
from routers.jobs import jobs_router


app = FastAPI()


app.include_router(users_router)
app.include_router(jobs_router)