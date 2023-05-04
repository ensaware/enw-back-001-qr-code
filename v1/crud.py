from sqlalchemy.orm import Session
from . import models, schema


def create_qr_code(db: Session, qr_code: schema.QRCodeBase):
    db_qr_code = models.QRCode(email=qr_code.email)
    db.add(db_qr_code)
    db.commit()
    db.refresh(db_qr_code)
    return db_qr_code


def get_qr_code(db: Session, id: str):
    return db.query(models.QRCode).filter(models.QRCode.id == id).first()


def get_qr_code_email(db: Session, email: str):
    return db.query(models.QRCode).filter(models.QRCode.email == email).first()