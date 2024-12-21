from typing import List, Optional

import jwt
import sqlalchemy as sa
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.api_models import BaseResponseModel
from app.api_models.tugas_model import TugasModel
from app.config import config
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session

from app.models.user import User


class GetTugasModel(BaseModel):
    id_tugas : int


class GetTugasDataResponseModel(BaseResponseModel):
    data: TugasModel

    class Config:
        json_schema_extra = {
            'example': {
                'data': {
                    'data':
                        
                            {   "id_renker":1,
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
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_tugas(data:GetTugasModel ,payload=Depends(Autentication()), session=Depends(get_db_session)):
    access = 0
    divisi = ""

    # ambill id payload
    user_id = payload.get('uid', 0)
    user_data = session.execute(sa.select(User.access,User.divisi).where(User.id_karyawan == user_id)).fetchone()
    print(user_data)
    if  user_data.access < 2 :
        raise HTTPException(400, detail='User not have access')

    tugas = session.execute(sa.text(f'SELECT * FROM tugas WHERE id_tugas = {data.id_tugas}')).fetchone()

    if tugas and len(tugas) == 0:
        raise HTTPException(400, detail='Target Tidak tersedia')

    def pelaksana(id_karyawan):
        print(id_karyawan)
        profile = session.execute(
        sa.select(
            User.full_name
        ).where(
            User.id_karyawan == id_karyawan
        )
        ).scalar()
        return profile

    tugas_ =  TugasModel(
                    id_tugas = tugas.id_tugas,
                    id_renker = tugas.id_renker,
                    judul = tugas.judul,
                    kpi= tugas.kpi,
                    deskripsi=tugas.deskripsi,
                    start_date = tugas.start_date,
                    modifed_at = tugas.modifed_at,
                    deadline = tugas.deadline,
                    catatan = tugas.catatan,
                    file_name = tugas.file_name,
                    id_divisi = tugas.id_divisi,
                    status = tugas.status,
                    id_karyawan = tugas.id_karyawan,
                    prioritas = tugas.prioritas,
                    progres = tugas.progres,
                    pelaksana=pelaksana(tugas.id_karyawan)


            )
    
 
    

    return GetTugasDataResponseModel(
        data=tugas_)



