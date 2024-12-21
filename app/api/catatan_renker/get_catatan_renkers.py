from typing import List, Optional

import jwt
import sqlalchemy as sa
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import desc

from app.api_models import BaseResponseModel
from app.config import config
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.models.catatan_renker import CatatanRenker

from app.utils.generate_hash import generate_hash


class DataGetCatatanRenkeres(BaseModel):
    id_renker: int 

class Catatan(BaseModel):
    id_catatan:int
    catatan:str


class GetCatatanRenkeresResponseModel(BaseModel):
    data: List[object]



class GetDataCatatanRenkeresResponseModel(BaseResponseModel):
    data: GetCatatanRenkeresResponseModel

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


async def get_catatan_renkers(request: DataGetCatatanRenkeres, payload=Depends(Autentication()), session=Depends(get_db_session)):
    
    response = session.execute(sa.select(CatatanRenker.catatan, CatatanRenker.id_catatan).where(CatatanRenker.id_renker == request.id_renker).order_by(CatatanRenker.id_catatan.desc())).all()
    if len(response) == 0:
        raise HTTPException(400, detail='Target Tidak tersedia')
    
    datalist = []

    for catatan in response:
        datalist.append(
            Catatan(
                id_catatan=catatan.id_catatan,
                catatan=catatan.catatan
            )             
        )


    return GetDataCatatanRenkeresResponseModel(data=GetCatatanRenkeresResponseModel(
        data=datalist,
      
    ))
