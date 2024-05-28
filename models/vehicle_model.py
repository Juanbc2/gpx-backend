from schemas import vehicle_schema
from sqlalchemy.orm import Session
from database import models
from models import competitors_model

def get_vehicles(db: Session):
    vehicles = db.query(models.Vehicle).all()
    for vehicle in vehicles:
        vehicle.competitor = competitors_model.get_competitor_by_id(db, vehicle.competitorId)
    return vehicles


def get_vehicle_by_id(db: Session, vehicle_id: str):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if vehicle is not None:
        vehicle.competitor = competitors_model.get_competitor_by_id(db, vehicle.competitorId)
    return vehicle
    

def create_vehicle(db: Session, vehicle: vehicle_schema.Vehicle):
    new_vehicle = models.Vehicle(
        brand = vehicle.brand,
        model= vehicle.model,
        plate= vehicle.plate,
        securePolicy= vehicle.securePolicy,
        competitorId= vehicle.competitorId,
    )
    db.add(new_vehicle)
    db.commit()
    return new_vehicle


def delete_vehicle(db: Session, vehicle_id: str):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    db.delete(vehicle)
    db.commit()
    return vehicle

def get_vehicle_by_competitor(db: Session, competitor_id: str):
    return db.query(models.Vehicle).filter(models.Vehicle.competitorId == competitor_id).first()

def update_vehicle_by_id(db: Session, vehicle_id: str, vehicle: vehicle_schema.Vehicle):
    vehicle_to_update = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if vehicle_to_update is not None:
        vehicle_to_update.brand = vehicle.brand
        vehicle_to_update.model = vehicle.model
        vehicle_to_update.plate = vehicle.plate
        vehicle_to_update.securePolicy = vehicle.securePolicy
        vehicle_to_update.competitorId = vehicle.competitorId
        db.commit()
        return True
    return False

