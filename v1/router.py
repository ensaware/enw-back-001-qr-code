from fastapi import APIRouter, Depends, status, Request, Response
from sqlalchemy.orm import Session
from typing import Union

from utils.database import ENGINE, get_db
from utils.qr import QR
from . import crud, models, schema



router = APIRouter(
    prefix='/api/v1'
)
models.Base.metadata.create_all(bind=ENGINE)


@router.post(
    '/qr-code',
    tags=['v1 - QR Code'],
    status_code=status.HTTP_201_CREATED,
    response_model=schema.QRCode
)
def create_qr_code(
    qr_code: schema.QRCodeBase,
    db: Session = Depends(get_db)
):
    return crud.create_qr_code(
        db,
        qr_code
    )


@router.get(
    '/qr-code/{id}',
    tags=['v1 - QR Code'],
    status_code=status.HTTP_200_OK,
    response_model=schema.QRCode,
    responses={
        204: {'model': None}
    }
)
def get_qr_code(
    id: str,
    response: Response,
    db: Session = Depends(get_db),
):
    qr_code = crud.get_qr_code(
        db,
        id
    )

    if qr_code:
        return qr_code
    
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get(
    '/qr-code/{email}/generate',
    tags=['v1 - QR Code'],
    status_code=status.HTTP_200_OK,
)
def qr_code_generate(
    request: Request,
    email: str,
    background: Union[str, None] = None,
    color: Union[str, None] = None,
    show_logo: bool = True,
    db: Session = Depends(get_db),
):
    url = str(request.base_url)
    result = QR(db)
    qr = result.generate(email, url, show_logo, background, color)
    
    return Response(content=qr, media_type='image/png')


@router.get(
    '/qr-code/{email}/read',
    tags=['v1 - QR Code'],
    status_code=status.HTTP_200_OK,
    response_model=schema.QRCode,
)
def qr_code_read(
    email: str,
    token: str,
    db: Session = Depends(get_db),
):
    result = QR(db)
    return result.read(email, token)