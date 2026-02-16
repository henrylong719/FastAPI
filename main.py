from fastapi import FastAPI
from app.routes.issues import router as issues_router
from app.middleware.timer import add_process_time_header
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app = FastAPI()

app.middleware("http")(add_process_time_header)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(issues_router)




