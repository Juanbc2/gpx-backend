from schemas import competitors_schema
from sqlalchemy.orm import Session
from database import models
from services import stages_service
from utils.validations import Validations

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


def create_stage_competitor_result(db: Session, stageCompetitorResult: competitors_schema.CompetitorGpxResult, stageId: int, vehicleId: int):
    new_stage_competitor_result = models.StageCompetitorResults(
        stageId,
        vehicleId,
        routeTime= stageCompetitorResult.routeTime,
        penaltieTime= stageCompetitorResult.penaltieTime,
        penalties= stageCompetitorResult.penalties,
        route= stageCompetitorResult.route,
    )
    db.add(new_stage_competitor_result)
    db.commit()


def load_competitor_gpx(db: Session, competitorGpx: competitors_schema.CompetitorGpx):
    stage = stages_service.get_stage_by_id(db, competitorGpx.stageId)
    if stage is None:
        return "Stage not found"
    validations_i = Validations()
    route = competitorGpx.filePath.replace("\\", "/")
    validationResult = validations_i.validations(stage, route)
    if validationResult is not None:
        result = {
            "penaltieTime": validationResult.tiempoCarrera,
            "routeTime": validationResult.total,
            "penalties": validationResult.penalizacion,
            "route": validationResult.ruta
        }
        create_stage_competitor_result(db, result, stage.id, competitorGpx.vehicleId)
        return result
    else:
        return None




