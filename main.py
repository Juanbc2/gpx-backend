from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import events
import stages

app = FastAPI()

app.include_router(events.router)
app.include_router(stages.router)


origins = [
   "http://localhost:3000",
]
app.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)