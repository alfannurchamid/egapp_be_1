from typing import List, Optional

import jwt
import sqlalchemy as sa
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.api_models import BaseResponseModel
from app.config import config
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.models.catatan_renker import CatatanRenker

from app.utils.generate_hash import generate_hash


class DataGetCatatanRenker(BaseModel):
    id_catatan: int 


class GetCatatanRenkerResponseModel(BaseModel):
    catatan: str



class GetDataCatatanRenkerResponseModel(BaseResponseModel):
    data: GetCatatanRenkerResponseModel

    class Config:
        json_schema_extra = {
            'example': {
                'data': {
                    'data':
                        [
                            {
                                "id_catatan": 9,
                                "id_renker": 3,
                                "catatan": "bla bla bla"
                            }
                        ],
                    'jum': 10
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_catatan_renker(request: DataGetCatatanRenker, payload=Depends(Autentication()), session=Depends(get_db_session)):
    
    response = session.execute(sa.select(CatatanRenker.catatan).where(CatatanRenker.id_catatan == request.id_catatan)).scalar()


    if len(response) == 0:
        raise HTTPException(400, detail='Target Tidak tersedia')

    return GetDataCatatanRenkerResponseModel(data=GetCatatanRenkerResponseModel(
        catatan = response
    ))
