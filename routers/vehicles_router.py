from fastapi import APIRouter,Depends, HTTPException
from database import models
from schemas import vehicle_schema
from database.database import SessionLocal, engine
from sqlalchemy.orm import Session
from services import vehicle_service

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/vehicles",tags=["vehicles"], response_model=list[vehicle_schema.VehicleWithCompetitor])
def get_vehicles(db: Session= Depends(get_db)):
    vehicles = vehicle_service.get_vehicles(db=db)
    if vehicles is not None:
        return vehicles
    else:
        raise HTTPException(status_code=404, detail="Vehicles not found")
    
@router.get("/vehicles/{vehicle_id}",tags=["vehicles"], response_model=vehicle_schema.VehicleWithCompetitor)
def get_vehicle(vehicle_id: str,db: Session= Depends(get_db)):
    vehicle = vehicle_service.get_vehicle_by_id(db=db, vehicle_id=vehicle_id)
    if vehicle is not None:
        return vehicle
    else:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
@router.post("/vehicles",tags=["vehicles"])
def add_vehicle(vehicle: vehicle_schema.Vehicle,db: Session= Depends(get_db)):
    new_vehicle = vehicle_service.create_vehicle(db=db, vehicle=vehicle)
    if new_vehicle is not None:
        raise HTTPException(status_code=200, detail="Vehicle created successfully")
    else:
        raise HTTPException(status_code=500, detail="Error creating vehicle")
    
@router.get("/vehicles/by_competitor/{competitor_id}",tags=["vehicles"], response_model=vehicle_schema.Vehicle)
def get_vehicle_by_competitor(competitor_id: str,db: Session= Depends(get_db)):
    vehicle = vehicle_service.get_vehicle_by_competitor(db=db, competitor_id=competitor_id)
    if vehicle is not None:
        return vehicle
    else:
        raise HTTPException(status_code=404, detail="Vehicle not found")

@router.put("/vehicles/{vehicle_id}",tags=["vehicles"])
def update_vehicle(vehicle_id: str, vehicle: vehicle_schema.Vehicle,db: Session= Depends(get_db)):
    updated_vehicle = vehicle_service.update_vehicle_by_id(db=db, vehicle_id=vehicle_id, vehicle=vehicle)
    if updated_vehicle:
        raise HTTPException(status_code=200, detail="Vehicle updated successfully")
    else:
        raise HTTPException(status_code=500, detail="Error updating vehicle")
    
@router.delete("/vehicles/{vehicle_id}",tags=["vehicles"])
def delete_vehicle(vehicle_id: str,db: Session= Depends(get_db)):
    vehicle = vehicle_service.delete_vehicle(db=db, vehicle_id=vehicle_id)
    if vehicle is not None:
        raise HTTPException(status_code=200, detail="Vehicle deleted successfully")
    else:
        raise HTTPException(status_code=500, detail="Error deleting vehicle")




