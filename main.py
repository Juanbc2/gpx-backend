from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import events_router as events
from routers import users_router as users
from routers import stages_router as stages
from routers import competitors_router as competitors
from routers import categories_router as categories
from routers import vehicles_router as vehicles
from uvicorn import run

import multiprocessing

app = FastAPI( title='GPX API',description='Documentación de las API para DARIEN GPX ANALYZER')
app.include_router(users.router)
app.include_router(events.router)
app.include_router(stages.router)
app.include_router(competitors.router)
app.include_router(vehicles.router)
app.include_router(categories.router)


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

if __name__ == '__main__':
    multiprocessing.freeze_support()  # For Windows support
    run(app, host="0.0.0.0", port=8000, reload=False, workers=1)