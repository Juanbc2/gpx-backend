from fastapi import  FastAPI
from fastapi.middleware.cors import CORSMiddleware
import events
import stages
import competitors
import login

app = FastAPI( title='GPX API',description='Documentación de las API para DARIEN GPX ANALYZER')
app.include_router(login.router)
app.include_router(events.router)
app.include_router(stages.router)
app.include_router(competitors.router)

origins = [
   "http://localhost:3000",
   "http://localhost:3001"
]
app.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)