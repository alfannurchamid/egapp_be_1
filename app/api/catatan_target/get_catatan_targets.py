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
from app.models.catatan_target import CatatanTarget

from app.utils.generate_hash import generate_hash


class DataGetCatatanTargets(BaseModel):
    id_target: int 

class Catatan(BaseModel):
    id_catatan:int
    catatan:str


class GetCatatanTargetsResponseModel(BaseModel):
    data: List[object]



class GetDataCatatanTargetsResponseModel(BaseResponseModel):
    data: GetCatatanTargetsResponseModel

    class Config:
        json_schema_extra = {
            'example': {
                'data': {
                    'data':
                        [
                            {
                                "id_catatan": 9,
                                "id_target": 3,
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


async def get_catatan_targets(request: DataGetCatatanTargets, payload=Depends(Autentication()), session=Depends(get_db_session)):
    
    response = session.execute(sa.select(CatatanTarget.catatan, CatatanTarget.id_catatan).where(CatatanTarget.id_target == request.id_target)).all()
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


    return GetDataCatatanTargetsResponseModel(data=GetCatatanTargetsResponseModel(
        data=datalist,
      
    ))
