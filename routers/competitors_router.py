from fastapi import APIRouter,Depends, HTTPException
from database import models
from schemas import competitors_schema
from database.database import SessionLocal, engine
from sqlalchemy.orm import Session
from models import competitors_model

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/competitors",tags=["competitors"], response_model=list[competitors_schema.Competitor])
def get_competitors(db: Session= Depends(get_db)):
    competitors = competitors_model.get_competitors(db=db)
    if competitors is not None:
        return competitors
    else:
        raise HTTPException(status_code=404, detail="Competitors not found")
    
    
@router.get("/competitors/{competitor_id}",tags=["competitors"], response_model=competitors_schema.Competitor)
def get_competitor(competitor_id: str,db: Session= Depends(get_db)):
    competitor = competitors_model.get_competitor_by_id(db=db, competitor_id=competitor_id)
    if competitor is not None:
        return competitor
    else:
        raise HTTPException(status_code=404, detail="Competitor not found")

@router.post("/competitors",tags=["competitors"])
def add_competitor(competitor: competitors_schema.Competitor,db: Session= Depends(get_db)):
    new_competitor = competitors_model.create_competitor(db=db, competitor=competitor)
    if new_competitor is not None:
        raise HTTPException(status_code=200, detail="Competitor created successfully")
    else:
        raise HTTPException(status_code=500, detail="Error creating competitor")
    
@router.post("/competitors/bulk",tags=["competitors"])
def add_competitors(competitors: list[competitors_schema.Competitor],db: Session= Depends(get_db)):
    new_competitors = competitors_model.bulk_create_competitors(db=db, competitors=competitors)
    if new_competitors is not None:
        raise HTTPException(status_code=200, detail="Competitors created successfully")
    else:
        raise HTTPException(status_code=500, detail="Error creating competitors")

@router.delete("/competitors/{competitor_id}",tags=["competitors"])
def delete_competitor(competitor_id: str,db: Session= Depends(get_db)):
    competitor = competitors_model.delete_competitor(db=db, competitor_id=competitor_id)
    if competitor is not None:
        raise HTTPException(status_code=200, detail="Competitor deleted successfully")
    else:
        raise HTTPException(status_code=500, detail="Error deleting competitor")

# Post competition .gpx file path

@router.post("/competitors/gpx",tags=["competitors"])
def post_gpx_file(competitorGpx: competitors_schema.CompetitorGpx,db: Session= Depends(get_db)):
    result = competitors_model.load_competitor_gpx(db=db, competitorGpx=competitorGpx)
    if result is not None:
        return result
    else:
        raise HTTPException(status_code=500, detail="Error loading competitor gpx")
    
@router.get("/competitors/results/{vehicle_id}/{stage_id}/",tags=["competitors"])
def get_competitor_results( vehicle_id: str, stage_id: int,db: Session= Depends(get_db)):
    results = competitors_model.get_competitor_results(db=db, vehicle_id=vehicle_id, stage_id=stage_id)
    if results is not None:
        return results
    else:
        raise HTTPException(status_code=404, detail="Results not found")
    
@router.put("/competitors/{competitor_id}",tags=["competitors"])
def update_competitor(competitor_id: str, competitor: competitors_schema.Competitor,db: Session= Depends(get_db)):
    updated_competitor = competitors_model.update_competitor(db=db, competitor_id=competitor_id, competitor=competitor)
    if updated_competitor is not None:
        raise HTTPException(status_code=200, detail="Competitor updated successfully")
    else:
        raise HTTPException(status_code=500, detail="Error updating competitor")
