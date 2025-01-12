# app/schemas.py
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID


# Hero Schemas
class HeroBase(BaseModel):
    name: str


class HeroCreate(HeroBase):
    pass


class Hero(HeroBase):
    id: str

    class Config:
        from_attributes = True


# UserHeroRelationship Schemas
class UserHeroRelationshipBase(BaseModel):
    hero_id: str
    level: int = 1

class UserHeroRelationshipCreate(UserHeroRelationshipBase):
    pass


class UserHeroRelationship(UserHeroRelationshipBase):
    id: str
    hero: Hero

    class Config:
        from_attributes = True


# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    heroes: List[UserHeroRelationship] = []
    sites: List['Site'] = []
    armies: List['Army'] = []

    class Config:
        from_attributes = True


# Site Schemas
class SiteBase(BaseModel):
    name: str
    x: int
    y: int
    z: int


class SiteCreate(SiteBase):
    owner_id: Optional[str] = None


class Site(SiteBase):
    id: str
    owner_id: Optional[str]
    stockable_metal: float
    available_metal: float
    stockable_crystals: float
    available_crystals: float
    stockable_deuterium: float
    available_deuterium: float
    beans_factory_level: int
    mana_extraction_plan_level: int
    gotcha_temple_level: int
    cannon_meat_farm_level: int
    armies_starting_here: List['Army'] = []
    armies_destination_here: List['Army'] = []

    class Config:
        from_attributes = True


# Army Schemas
class ArmyBase(BaseModel):
    starting_site_id: str
    destination_site_id: Optional[str] = None
    departure_time: Optional[int] = None  # Unix timestamp


class ArmyCreate(ArmyBase):
    starlight_sprinter: int = 0
    nebula_noodle_hauler: int = 0
    astro_idol_cruiser: int = 0
    photon_feather: int = 0
    waifu_wing_destroyer: int = 0
    pudding_mecha: int = 0


class Army(ArmyBase):
    id: str
    owner_id: str
    starlight_sprinter: int
    nebula_noodle_hauler: int
    astro_idol_cruiser: int
    photon_feather: int
    waifu_wing_destroyer: int
    pudding_mecha: int

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    username: Optional[str] = None

    class Config:
        from_attributes = True


# Update forward references
User.update_forward_refs()
Site.update_forward_refs()
Army.update_forward_refs()
