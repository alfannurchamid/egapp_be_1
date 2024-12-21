from typing import List, Optional

import jwt
import sqlalchemy as sa
from sqlalchemy import select
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.api_models import BaseResponseModel
from app.api_models.tugas_model import TugasModel
from app.config import config
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.models.tugas import Tugas
from app.models.user import User
from app.api_models.profile_model import ProfileModel


class GetTugasData(BaseModel):
    id_divisi : Optional[int] = None
    id_renker : Optional[int] = None
    id_karyawan : Optional[str] = None
    bebas : int

class GetDatatuugassResponseModel(BaseResponseModel):
    data: List[object]

    class Config:
        json_schema_extra = {
            'example': {
                'data': {
                    'data':
                        [
                            {   "id_renker":2,
                                "id_tugas":1,
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


async def get_tugases(data:GetTugasData,payload=Depends(Autentication()), session=Depends(get_db_session)):
    access = 0
    param =""
    def cek_param(panjang):
        if panjang > 0 :
            return ' AND '
        else : 
            return ' WHERE '
        
    data_tugas = jsonable_encoder(data)

    # ambill id payload
    user_id = payload.get('uid', 0)
    user_data = session.execute(sa.select(User.access,User.divisi).where(User.id_karyawan == user_id)).fetchone()
    print(user_data)

    #  jika akses  ==0 maka akses ditolak
    if  user_data.access == 0 :
        raise HTTPException(400, detail='User not have access')
    #  jika akses < 3 maka sql dibatasi di divisi nya saja
    elif user_data.access < 3: 
        if data.id_divisi : 
             raise HTTPException(400, detail=f'User not have access {data.id_divisi}')
        param= f"WHERE id_divisi = {user_data.divisi}"
    elif user_data.access > 3 and data.id_divisi  : 
        param += cek_param(len(param))
    #  jika akses > 3 maka sql disesuaikann divisi yg dimminntaa
        param =f" id_divisi = {data.id_divisi}"

    if  "id_renker" in data_tugas and data_tugas['id_renker']  :
        param += cek_param(len(param))
        param = param + f" id_renker = {data.id_renker}"

    if data_tugas['id_karyawan'] and 'id_karyawan' in data_tugas :
        param += cek_param(len(param))
        param = param + f" id_karyawan ='{data.id_karyawan}'"

    tugases = session.execute(sa.text(f'SELECT * FROM tugas {param}')).all()

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


    dataLList=[]

    for tugas in tugases:
        dataLList.append(
            TugasModel(
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
        )
    

    return GetDatatuugassResponseModel(
        data=dataLList)



