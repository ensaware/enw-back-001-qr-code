from io import BytesIO
from os import remove
from uuid import uuid4

import pyqrcode
from PIL import Image
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session

from utils.settings import Settings
from . import crud


class QR:
    def __init__(self) -> None:
        self.__settings = Settings()
        self.__fernet_pass = self.__settings.fernet_pass
        self.__fernet = Fernet(self.__fernet_pass)
        self.encode = 'UTF-8'


    def generate(self, db: Session, email: str, url: str) -> bytes:
        qr_email = crud.get_qr_code_email(
            db,
            email
        )

        if not(qr_email):
            raise ValueError(
                'Error recuperando información del código QR.'
            )
    
        encrypt = self.__fernet.encrypt(qr_email.id.encode(self.encode)).decode(self.encode)

        url = f'{url}api/v1/qr-code/{email}/read?token={encrypt}'

        qr = pyqrcode.create(url, error='H')
        name_qr = f'{str(uuid4())}.png'
        qr.png(name_qr, scale=10, module_color='#2db3ff', background='#eff7ff')
        img = Image.open(name_qr)
        img = img.convert('RGBA')
        

        logo_cua = Image.open('logo-cua.png')
        logo_cua = logo_cua.resize((150, 150))
        pos = ((img.size[0] - logo_cua.size[0]) // 2, 
               (img.size[1] - logo_cua.size[1]) // 2)
        img.paste(logo_cua, pos)

        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = buffered.getvalue()

        remove(name_qr)

        return img_str
    

    def read(self, db: Session, email: str, token: str):
        decrypt = self.__fernet.decrypt(token).decode(self.encode)
        qr_id = crud.get_qr_code(db, decrypt)

        if not(qr_id):
            raise ValueError(
                'Error leyendo la información del código QR.'
            )

        if qr_id.email.lower() != email.lower():
            raise ValueError(
                'El correo electrónico no pertenece al código QR.'
            )
        
        return qr_id
        