from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from schemas import stages_schema
from .database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,autoincrement=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String)
    location = Column(String)
    details = Column(String,default="")
    eventStartDate = Column(String)
    eventEndDate = Column(String)
    categoriesIds = Column(String)

    stage = relationship("Stages", backref="events")

class Stages(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String)
    eventId = Column(Integer, ForeignKey("events.id"))
    details = Column(String)
    stageDate = Column(String)
    waypoints = Column(String)
    categoriesIds = Column(String)

    stageCompetitorResults = relationship("StageCompetitorResults", backref="stages")


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String)
    description = Column(String)


class Competitors(Base):
    __tablename__ = "competitors"

    id = Column(Integer, primary_key=True,autoincrement=True)
    identification = Column(String, unique=True)
    name = Column(String)
    lastName = Column(String)
    number = Column(String)


class Vehicle(Base):
    __tablename__ = "vehicle"

    id = Column(Integer, primary_key=True,autoincrement=True)
    brand = Column(String)
    model = Column(String)
    competitorId = Column(Integer, ForeignKey("competitors.id"))
    plate = Column(String)
    securePolicy = Column(String)

    stageCompetitorResults = relationship("StageCompetitorResults", backref="vehicle")

class StageCompetitorResults(Base):
    __tablename__ = "stage_competitor_results"

    id = Column(Integer, primary_key=True,autoincrement=True)
    stageId = Column(Integer, ForeignKey("stages.id"))
    vehicleId = Column(Integer, ForeignKey("vehicle.id"))
    penaltieTime = Column(String)
    routeTime = Column(String)
    penalties = Column(String)
    route = Column(String)




