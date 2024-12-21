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


class DataGetCatatanTugase(BaseModel):
    id_catatan: int 




class GetCatatanTugasResponseModel(BaseModel):
    catatan: str



class GetDataCatatanTugasResponseModel(BaseResponseModel):
    data: GetCatatanTugasResponseModel

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


async def get_catatan_tugas(request: DataGetCatatanTugase, payload=Depends(Autentication()), session=Depends(get_db_session)):
    
    response = session.execute(sa.select(CatatanTugas.catatan).where(CatatanTugas.id_catatan == request.id_catatan)).scalar()



    return GetDataCatatanTugasResponseModel(data=GetCatatanTugasResponseModel(
        catatan = response
      
    ))
