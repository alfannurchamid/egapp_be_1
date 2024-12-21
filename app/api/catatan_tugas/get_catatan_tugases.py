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
from app.models.catatan_tugas import CatatanTugas

from app.utils.generate_hash import generate_hash


class DataGetCatatanTugases(BaseModel):
    id_tugas: int 

class Catatan(BaseModel):
    id_catatan:int
    catatan:str


class GetCatatanTugasesResponseModel(BaseModel):
    data: List[object]



class GetDataCatatanTugasesResponseModel(BaseResponseModel):
    data: GetCatatanTugasesResponseModel

    class Config:
        json_schema_extra = {
            'example': {
                'data': {
                    'data':
                        [
                            {
                                "id_catatan": 9,
                                "id_tugas": 3,
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


async def get_catatan_tugases(request: DataGetCatatanTugases, payload=Depends(Autentication()), session=Depends(get_db_session)):
    
    response = session.execute(sa.select(CatatanTugas.catatan, CatatanTugas.id_catatan).where(CatatanTugas.id_tugas == request.id_tugas)).all()
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


    return GetDataCatatanTugasesResponseModel(data=GetCatatanTugasesResponseModel(
        data=datalist,
      
    ))
