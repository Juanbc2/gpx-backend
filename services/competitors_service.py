from schemas import competitors_schema
from sqlalchemy.orm import Session
from database import models
from services import stages_service
from utils.validations import Validations
import json

def get_competitors(db: Session):
    return db.query(models.Competitors).all()

def get_competitor_by_id(db: Session, competitor_id: str):
    return db.query(models.Competitors).filter(models.Competitors.id == competitor_id).first()

def create_competitor(db: Session, competitor: competitors_schema.Competitor):
    new_competitor = models.Competitors(name=competitor.name, lastName=competitor.lastName, number=competitor.number, identification=competitor.identification)   
    db.add(new_competitor)
    db.commit()
    return new_competitor

def delete_competitor(db: Session, competitor_id: str):
    competitor = db.query(models.Competitors).filter(models.Competitors.id == competitor_id).first()
    db.delete(competitor)
    db.commit()
    return competitor

def get_competitor_results(db: Session, vehicle_id: str, stage_id: int):
    results = db.query(models.StageCompetitorResults).filter(models.StageCompetitorResults.vehicleId == vehicle_id, models.StageCompetitorResults.stageId == stage_id).first()
    return results


def create_stage_competitor_result(db: Session, stageCompetitorResult: str, stageId: int, vehicleId: int):
    result = json.loads(stageCompetitorResult)
    save = {
            "penaltieTime": result["penaltieTime"],
            "routeTime": result["routeTime"],
            "penalties": result["penalties"],
            "route": result["route"]
        }
    existing_result = db.query(models.StageCompetitorResults).filter_by(stageId=stageId, vehicleId=vehicleId).first()
    if existing_result:
        # Actualiza el registro existente
        existing_result.routeTime = save["routeTime"]
        existing_result.penaltieTime = save["penaltieTime"]
        existing_result.penalties = json.dumps(save["penalties"])
        existing_result.route = json.dumps(save["route"])
    else:
        # Crea un nuevo registro
        new_stage_competitor_result = models.StageCompetitorResults(
            stageId = stageId,
            vehicleId = vehicleId,
            routeTime= save["routeTime"],
            penaltieTime= save["penaltieTime"],
            penalties= json.dumps(save["penalties"]),
            route= json.dumps(save["route"]),
        )
        db.add(new_stage_competitor_result)
    db.commit()



def load_competitor_gpx(db: Session, competitorGpx: competitors_schema.CompetitorGpx):
    waypoints = stages_service.get_stage_waypoints(db, competitorGpx.stageId)
    if waypoints is None:
        return "Waypoints not found"
    validations_i = Validations()
    route = competitorGpx.filePath.replace("\\", "/")
    validationResult = validations_i.validations(waypoints,route)
    if validationResult is not None:
        create_stage_competitor_result(db, validationResult,competitorGpx.stageId, competitorGpx.vehicleId)
        return validationResult
    else:
        return None




