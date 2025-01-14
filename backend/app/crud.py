from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_admin=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Hero CRUD
def get_hero_by_name(db: Session, name: str):
    return db.query(models.Hero).filter(models.Hero.name == name).first()

def create_hero(db: Session, hero: schemas.HeroCreate):
    db_hero = models.Hero(name=hero.name)
    db.add(db_hero)
    db.commit()
    db.refresh(db_hero)
    return db_hero

def get_hero(db: Session, hero_id: str):
    return db.query(models.Hero).filter(models.Hero.id == hero_id).first()

# UserHeroRelationship CRUD
def add_hero_to_user(db: Session, user_id: str, hero_relationship: schemas.UserHeroRelationshipCreate):
    db_relationship = models.UserHeroRelationship(
        user_id=user_id,
        hero_id=hero_relationship.hero_id,
        level=hero_relationship.level,
        settings=hero_relationship.settings
    )
    db.add(db_relationship)
    db.commit()
    db.refresh(db_relationship)
    return db_relationship

def get_user_heroes(db: Session, user_id: str):
    return db.query(models.UserHeroRelationship).filter(models.UserHeroRelationship.user_id == user_id).all()

# Site CRUD
def get_site(db: Session, site_id: str):
    return db.query(models.Site).filter(models.Site.id == site_id).first()

def create_site(db: Session, site: schemas.SiteCreate):
    db_site = models.Site(
        name=site.name,
        x=site.x,
        y=site.y,
        z=site.z,
        owner_id=site.owner_id,
        metal_stock_level=0.0,
        available_metal=0.0,
        crystal_stock_level=0.0,
        available_crystals=0.0,
        deuterium_stock_level=0.0,
        available_deuterium=0.0,
        beans_factory_level=0,
        mana_extraction_plan_level=0,
        gotcha_temple_level=0,
        cannon_meat_farm_level=0,
    )
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site

def get_user_sites(db: Session, user_id: str):
    return db.query(models.Site).filter(models.Site.owner_id == user_id).all()

# Army CRUD
def get_army(db: Session, army_id: str):
    return db.query(models.Army).filter(models.Army.id == army_id).first()

def create_army(db: Session, army: schemas.ArmyCreate, owner_id: str):
    db_army = models.Army(
        owner_id=owner_id,
        starting_site_id=army.starting_site_id,
        destination_site_id=army.destination_site_id,
        departure_time=army.departure_time,
        starlight_sprinter=army.starlight_sprinter,
        nebula_noodle_hauler=army.nebula_noodle_hauler,
        astro_idol_cruiser=army.astro_idol_cruiser,
        photon_feather=army.photon_feather,
        waifu_wing_destroyer=army.waifu_wing_destroyer,
        pudding_mecha=army.pudding_mecha,
    )
    db.add(db_army)
    db.commit()
    db.refresh(db_army)
    return db_army

def get_user_armies(db: Session, user_id: str):
    return db.query(models.Army).filter(models.Army.owner_id == user_id).all()
