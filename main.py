from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Database
DATABASE_URL = "sqlite:///./internships.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# Database table
class InternshipDB(Base):
    __tablename__ = "internships"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    location = Column(String, nullable=False)
    status = Column(String, nullable=False)


# Create database table
Base.metadata.create_all(bind=engine)


# Data format
class Internship(BaseModel):
    company: str
    role: str
    location: str
    status: str


app = FastAPI()


# Home
@app.get("/")
def home():
    return {"message": "Internship Tracker API is running!"}


# CREATE
@app.post("/internships")
def add_internship(internship: Internship):

    db = SessionLocal()

    new_internship = InternshipDB(
        company=internship.company,
        role=internship.role,
        location=internship.location,
        status=internship.status
    )

    db.add(new_internship)
    db.commit()
    db.refresh(new_internship)

    result = {
        "id": new_internship.id,
        "company": new_internship.company,
        "role": new_internship.role,
        "location": new_internship.location,
        "status": new_internship.status
    }

    db.close()

    return {
        "message": "Internship added successfully",
        "internship": result
    }


# READ ALL
@app.get("/internships")
def get_internships():

    db = SessionLocal()

    internships = db.query(InternshipDB).all()

    result = []

    for internship in internships:
        result.append({
            "id": internship.id,
            "company": internship.company,
            "role": internship.role,
            "location": internship.location,
            "status": internship.status
        })

    db.close()

    return result


# READ ONE
@app.get("/internships/{internship_id}")
def get_internship(internship_id: int):

    db = SessionLocal()

    internship = db.query(InternshipDB).filter(
        InternshipDB.id == internship_id
    ).first()

    if not internship:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Internship not found"
        )

    result = {
        "id": internship.id,
        "company": internship.company,
        "role": internship.role,
        "location": internship.location,
        "status": internship.status
    }

    db.close()

    return result


# UPDATE
@app.put("/internships/{internship_id}")
def update_internship(
    internship_id: int,
    internship: Internship
):

    db = SessionLocal()

    existing = db.query(InternshipDB).filter(
        InternshipDB.id == internship_id
    ).first()

    if not existing:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Internship not found"
        )

    existing.company = internship.company
    existing.role = internship.role
    existing.location = internship.location
    existing.status = internship.status

    db.commit()
    db.refresh(existing)

    result = {
        "id": existing.id,
        "company": existing.company,
        "role": existing.role,
        "location": existing.location,
        "status": existing.status
    }

    db.close()

    return {
        "message": "Internship updated successfully",
        "internship": result
    }


# DELETE
@app.delete("/internships/{internship_id}")
def delete_internship(internship_id: int):

    db = SessionLocal()

    existing = db.query(InternshipDB).filter(
        InternshipDB.id == internship_id
    ).first()

    if not existing:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Internship not found"
        )

    db.delete(existing)
    db.commit()
    db.close()

    return {
        "message": "Internship deleted successfully"
    }