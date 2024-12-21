from typing import List, Optional
from sqlalchemy import func

import jwt
import sqlalchemy as sa
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.api_models import BaseResponseModel
from app.api_models.profile_model import ProfileModel
from app.config import config
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.models.divisi import Divisi
from app.models.user import User
from app.api_models.divisi_model import DivisiModel


class GetDataDivisiesResponseModel(BaseResponseModel):
    data: List[object]

    class Config:
        json_schema_extra = {
            'example': {
                'data': {
                    'data':
                        [
                            {   "id_divisi":2,
                                "nama_divisi":"",
                               
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


async def get_divisies(payload=Depends(Autentication()), session=Depends(get_db_session)):
    access = 0
    param =""
    # data_get = jsonable_encoder(data)

    # ambill id payload
    # user_id = payload.get('uid', 0)
    # user_data = session.execute(sa.select(User.access,User.divisi).where(User.id_karyawan == user_id)).fetchone()
    # print(user_data)




    divisies = session.execute(sa.select(Divisi.id_divisi,Divisi.nama_divisi,Divisi.path_foto)).all()

    dataLList=[]
    def jml_karyawan(x:int):
        jumlah_karyawans = session.execute(sa.text(f"select count(id_karyawan) as jml_karyawan from user where divisi = {x} ")).fetchone()
        return jumlah_karyawans.jml_karyawan

    def manager(x:int): 
        profile =  session.execute(sa.select(
                User.id_karyawan,
                User.username,
                User.full_name,
                User.email,
                User.noWa,
                User.nik,
                User.alamat,
                User.access,
                User.path_foto,
                User.divisi,
                User.jabatan
            ).where(
               sa.and_( User.divisi == x , User.access >2)
            )
            ).fetchone()

        if not profile :
            return
        
        manger_nya = ProfileModel(
            id_karyawan= profile.id_karyawan,
            username=profile.username,
            full_name=profile.full_name,
            email=profile.email,
            noWa=profile.noWa,
            access=profile.access,
            path_foto=profile.path_foto,
            nik=profile.nik,
            alamat=profile.alamat,
            divisi=profile.divisi,
            jabatan=profile.jabatan,
            nama_divisi='x'
            )
        return manger_nya
        

        
    for divisi in divisies:
        dataLList.append(
            DivisiModel(
                id_divisi=divisi.id_divisi,
                nama_divisi=divisi.nama_divisi,
                path_foto='',
                jml_karyawan = jml_karyawan(divisi.id_divisi),
                manager=manager(divisi.id_divisi)

            )
        )
    

    return GetDataDivisiesResponseModel(
        data=dataLList)



