from datetime import datetime
from fastapi import HTTPException

from app.database import SessionLocal
from app.portals.models_orm import PortalConfig, PortalMapping


# -------------------------
# LIST PORTALS
# -------------------------

def list_portals():
    db = SessionLocal()
    try:
        configs = db.query(PortalConfig).all()
        return [c.portal_name for c in configs]
    finally:
        db.close()


# -------------------------
# GET CONFIG
# -------------------------

def get_portal_config(portal: str):
    db = SessionLocal()
    try:
        cfg = db.query(PortalConfig).filter(PortalConfig.portal_name == portal).first()
        if not cfg:
            raise HTTPException(status_code=404, detail="Portal not found")

        return {
            "portal": cfg.portal_name,
            "settings": cfg.settings,
            "updated_at": cfg.updated_at
        }
    finally:
        db.close()


# -------------------------
# UPDATE CONFIG
# -------------------------

def update_portal_config(portal: str, key: str, value: str):
    db = SessionLocal()
    try:
        cfg = db.query(PortalConfig).filter(PortalConfig.portal_name == portal).first()
        if not cfg:
            raise HTTPException(status_code=404, detail="Portal not found")

        cfg.settings[key] = value
        cfg.updated_at = datetime.now()

        db.commit()
        return {"updated": True, "portal": portal, "settings": cfg.settings}
    finally:
        db.close()


# -------------------------
# HEALTH CHECK
# -------------------------

def get_portal_health(portal: str):
    db = SessionLocal()
    try:
        cfg = db.query(PortalConfig).filter(PortalConfig.portal_name == portal).first()
        if not cfg:
            raise HTTPException(status_code=404, detail="Portal not found")

        # health check semplice
        return {
            "portal": portal,
            "status": "ok",
            "last_update": cfg.updated_at
        }
    finally:
        db.close()


# -------------------------
# GET MAPPING
# -------------------------

def get_portal_mapping(portal: str):
    db = SessionLocal()
    try:
        mapping = db.query(PortalMapping).filter(PortalMapping.portal_name == portal).all()
        return {m.field: m.mapped_to for m in mapping}
    finally:
        db.close()


# -------------------------
# UPDATE MAPPING
# -------------------------

def update_portal_mapping(portal: str, field: str, mapped_to: str):
    db = SessionLocal()
    try:
        m = db.query(PortalMapping).filter(
            PortalMapping.portal_name == portal,
            PortalMapping.field == field
        ).first()

        if not m:
            # create new mapping
            m = PortalMapping(
                portal_name=portal,
                field=field,
                mapped_to=mapped_to
            )
            db.add(m)
        else:
            # update existing mapping
            m.mapped_to = mapped_to

        db.commit()
        return {"updated": True, "portal": portal, "field": field, "mapped_to": mapped_to}

    finally:
        db.close()
