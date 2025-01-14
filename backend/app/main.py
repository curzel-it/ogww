# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud, auth
from .database import engine, SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ogame with Heroes")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User Registration (existing)
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Token Endpoint (existing)
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Get Current User (existing)
@app.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

# Hero Endpoints
@app.post("/heroes/", response_model=schemas.Hero)
def create_hero(hero: schemas.HeroCreate, db: Session = Depends(get_db), 
                current_user: models.User = Depends(auth.get_current_user)):
    db_hero = crud.get_hero_by_name(db, name=hero.name)
    if db_hero:
        raise HTTPException(status_code=400, detail="Hero already exists")
    return crud.create_hero(db=db, hero=hero)

@app.get("/heroes/", response_model=list[schemas.Hero])
def read_heroes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    heroes = db.query(models.Hero).offset(skip).limit(limit).all()
    return heroes

# User-Hero Relationship Endpoints
@app.post("/users/me/heroes/", response_model=schemas.UserHeroRelationship)
def add_hero_to_user(
    hero_relationship: schemas.UserHeroRelationshipCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Check if hero exists
    hero = crud.get_hero(db, hero_id=hero_relationship.hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    # Check if relationship already exists
    existing = (
        db.query(models.UserHeroRelationship)
        .filter(
            models.UserHeroRelationship.user_id == current_user.id,
            models.UserHeroRelationship.hero_id == hero_relationship.hero_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Hero already added to user")
    return crud.add_hero_to_user(db=db, user_id=current_user.id, hero_relationship=hero_relationship)

@app.get("/users/me/heroes/", response_model=list[schemas.UserHeroRelationship])
def get_user_heroes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return crud.get_user_heroes(db, user_id=current_user.id)

# Site Endpoints
@app.post("/sites/", response_model=schemas.Site)
def create_site(
    site: schemas.SiteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if site.owner_id and site.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot create site for another user")
    
    return crud.create_site(db=db, site=site)

@app.get("/sites/", response_model=list[schemas.Site])
def read_sites(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return crud.get_user_sites(db, user_id=current_user.id)

@app.get("/sites/{site_id}", response_model=schemas.Site)
def read_site(
    site_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    site = crud.get_site(db, site_id=site_id)
    if site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    if site.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this site")
    return site

# Army Endpoints
@app.post("/armies/", response_model=schemas.Army)
def create_army(
    army: schemas.ArmyCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Verify starting site ownership
    starting_site = crud.get_site(db, site_id=army.starting_site_id)
    if not starting_site or starting_site.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Invalid starting site")
    # If destination_site_id is provided, verify ownership or allow movement to others
    if army.destination_site_id:
        destination_site = crud.get_site(db, site_id=army.destination_site_id)
        if not destination_site:
            raise HTTPException(status_code=404, detail="Destination site not found")
    return crud.create_army(db=db, army=army, owner_id=current_user.id)

@app.get("/armies/", response_model=list[schemas.Army])
def read_armies(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return crud.get_user_armies(db, user_id=current_user.id)

@app.get("/armies/{army_id}", response_model=schemas.Army)
def read_army(
    army_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    army = crud.get_army(db, army_id=army_id)
    if army is None:
        raise HTTPException(status_code=404, detail="Army not found")
    if army.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this army")
    return army
