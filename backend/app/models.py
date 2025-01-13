import uuid
from sqlalchemy import (
    Column,
    Boolean,
    String,
    Float,
    Integer,
    ForeignKey,
    UniqueConstraint,
    BigInteger,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import BigInteger as BigIntegerType

from .database import Base

# Helper function to generate UUIDs
def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=True)

    # Relationships
    heroes = relationship(
        "UserHeroRelationship",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    sites = relationship(
        "Site",
        back_populates="owner",
        cascade="all, delete-orphan",
    )
    armies = relationship(
        "Army",
        back_populates="owner",
        cascade="all, delete-orphan",
    )


class Hero(Base):
    __tablename__ = 'heroes'

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    name = Column(String, unique=True, index=True, nullable=False)

    # Relationships
    users = relationship(
        "UserHeroRelationship",
        back_populates="hero",
        cascade="all, delete-orphan",
    )


class UserHeroRelationship(Base):
    __tablename__ = 'user_hero_relationships'
    __table_args__ = (
        UniqueConstraint('user_id', 'hero_id', name='uix_user_hero'),
    )

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    hero_id = Column(String, ForeignKey('heroes.id'), nullable=False)
    level = Column(Integer, default=1)
    settings = Column(String, nullable=True)  # JSON string or similar for settings

    # Relationships
    user = relationship("User", back_populates="heroes")
    hero = relationship("Hero", back_populates="users")


class Site(Base):
    __tablename__ = 'sites'

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    owner_id = Column(String, ForeignKey('users.id'), nullable=True)
    name = Column(String, nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    z = Column(Integer, nullable=False)

    # Resources
    stockable_metal = Column(Float, default=0.0)
    available_metal = Column(Float, default=0.0)
    stockable_crystals = Column(Float, default=0.0)
    available_crystals = Column(Float, default=0.0)
    stockable_deuterium = Column(Float, default=0.0)
    available_deuterium = Column(Float, default=0.0)

    # Buildings
    beans_factory_level = Column(Integer, default=0)
    mana_extraction_plan_level = Column(Integer, default=0)
    gotcha_temple_level = Column(Integer, default=0)
    cannon_meat_farm_level = Column(Integer, default=0)

    # Relationships
    owner = relationship("User", back_populates="sites")
    armies_starting_here = relationship(
        "Army",
        back_populates="starting_site",
        foreign_keys='Army.starting_site_id',
    )
    armies_destination_here = relationship(
        "Army",
        back_populates="destination_site",
        foreign_keys='Army.destination_site_id',
    )


class Army(Base):
    __tablename__ = 'armies'

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    owner_id = Column(String, ForeignKey('users.id'), nullable=False)
    starting_site_id = Column(String, ForeignKey('sites.id'), nullable=False)
    destination_site_id = Column(String, ForeignKey('sites.id'), nullable=True)
    departure_time = Column(BigIntegerType, nullable=True)  # Unix timestamp as u64

    # Troops and Ships
    starlight_sprinter = Column(Integer, default=0)
    nebula_noodle_hauler = Column(Integer, default=0)
    astro_idol_cruiser = Column(Integer, default=0)
    photon_feather = Column(Integer, default=0)
    waifu_wing_destroyer = Column(Integer, default=0)
    pudding_mecha = Column(Integer, default=0)

    # Relationships
    owner = relationship("User", back_populates="armies")
    starting_site = relationship(
        "Site",
        back_populates="armies_starting_here",
        foreign_keys=[starting_site_id],
    )
    destination_site = relationship(
        "Site",
        back_populates="armies_destination_here",
        foreign_keys=[destination_site_id],
    )
