from fastapi import FastAPI
from routers.users import users_router
from routers.jobs import jobs_router
from routers.housings import housing_router
from routers.messages import messages_router
from routers.conversations import conversations_router
from routers.q_a import qa_router


app = FastAPI()


app.include_router(users_router)
app.include_router(jobs_router)
app.include_router(housing_router)
app.include_router(messages_router)
app.include_router(conversations_router)
app.include_router(qa_router)