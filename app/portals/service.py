from sqlalchemy.orm import Session
from app.portals.models_orm import PortalConfig, PortalMapping
from app.portals.schemas import (
    PortalConfigCreate,
    PortalConfigUpdate,
    PortalMappingCreate,
    PortalMappingUpdate,
)


# ---------------------------------------------------------
# PORTAL CONFIG SERVICE
# ---------------------------------------------------------

class PortalConfigService:

    @staticmethod
    def get_all(db: Session):
        return db.query(PortalConfig).all()

    @staticmethod
    def get_by_name(db: Session, portal_name: str):
        return db.query(PortalConfig).filter(PortalConfig.portal_name == portal_name).first()

    @staticmethod
    def create(db: Session, data: PortalConfigCreate):
        obj = PortalConfig(**data.dict())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def update(db: Session, portal_name: str, data: PortalConfigUpdate):
        obj = PortalConfigService.get_by_name(db, portal_name)
        if not obj:
            return None

        for key, value in data.dict(exclude_unset=True).items():
            setattr(obj, key, value)

        db.commit()
        db.refresh(obj)
        return obj


# ---------------------------------------------------------
# PORTAL MAPPING SERVICE
# ---------------------------------------------------------

class PortalMappingService:

    @staticmethod
    def get_all(db: Session, portal_name: str):
        return db.query(PortalMapping).filter(PortalMapping.portal_name == portal_name).all()

    @staticmethod
    def create(db: Session, data: PortalMappingCreate):
        obj = PortalMapping(**data.dict())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def update(db: Session, mapping_id: int, data: PortalMappingUpdate):
        obj = db.query(PortalMapping).filter(PortalMapping.id == mapping_id).first()
        if not obj:
            return None

        for key, value in data.dict(exclude_unset=True).items():
            setattr(obj, key, value)

        db.commit()
        db.refresh(obj)
        return obj
