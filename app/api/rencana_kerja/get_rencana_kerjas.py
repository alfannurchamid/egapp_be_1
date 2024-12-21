from typing import List, Optional

import jwt
import sqlalchemy as sa
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.api_models import BaseResponseModel
from app.api_models.rencana_kerja_model import RencanaKerjaModel
from app.api_models.target_model import TargetModel
from app.config import config
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.models.target import Target
from app.models.user import User


class GetRencanaKerjaData(BaseModel):
    id_target: Optional[int] = None
    id_divisi: Optional[int] = None
    bebas : int

class GetDataRencanaKerjasResponseModel(BaseResponseModel):
    data: List[object]

    class Config:
        json_schema_extra = {
            'example': {
                'data': {
                    'data':
                        [
                            {   "id_renker":2,
                                "id_target":1,
                                "judul": "omset 200 jt per bulan",
                                "id_divisi": 2,
                                "deskripsi":"harus omset 200 jt per bulan",
                                "kpi":"ommset",
                                "deadline":2024/12/23,
                                "start_date":2024/12/23,
                                "catatan":"ini catatatn ",
                                "file_name":"filenname.jpg",
                                "modifed_at" : 2024/12/23
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


async def get_rencana_kerjas(data:GetRencanaKerjaData,payload=Depends(Autentication()), session=Depends(get_db_session)):
    access = 0
    divisi =""
    minta_data = jsonable_encoder(data)
    # ambill id payload

    if 'id_target' in minta_data and minta_data['id_target']:
        divisi = divisi + f' WHERE id_target = {minta_data['id_target']}'

    if 'id_divisi' in minta_data and minta_data['id_divisi']:
        divisi = divisi + f' WHERE id_divisi = {minta_data['id_divisi']}'

    renkers = session.execute(sa.text(f'SELECT * FROM rencana_kerja  {divisi}')).all()

    dataLList=[]

    for renker in renkers:
        dataLList.append(
            RencanaKerjaModel(
                    id_renker = renker.id_renker,
                    id_target =renker.id_target,
                    judul = renker.judul,
                    kpi= renker.kpi,
                    deskripsi=renker.deskripsi,
                    start_date = renker.start_date,
                    modifed_at = renker.modifed_at,
                    deadline = renker.deadline,
                    catatan = renker.catatan,
                    file_name = renker.file_name,
                    id_divisi = renker.id_divisi,
                    status = renker.status,
                    progres = renker.progres,
                    prioritas = renker.prioritas
            )
        )


    return GetDataRencanaKerjasResponseModel(
        data=dataLList)



