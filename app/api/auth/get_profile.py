
from typing import List
from fastapi import Depends, HTTPException
import sqlalchemy as sa

from app.api_models import BaseResponseModel
from app.api_models.profile_model import ProfileModel
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session

from app.models.divisi import Divisi
from app.models.user import User




class GetProfileResponseModel(BaseResponseModel):
    data: ProfileModel

    class Config:
        json_schema_extra = {
            'example': {
                'data': {
                    'id_karyawan': '1000',
                    'username': 'alpen',
                    'access_token': 'access token',
                    'email': 'alfannurchamid@gmial.com',
                    'noWa': '089681709727',
                    'access': '0',
                    'path_foto': 'skjdalk.jpg',
                    'alamat': 'rt1,rw2,ngalian,wadaslintang',
                    'nik': '3307080409009990',
                    'id_divisi': 1,
                    'nama_divisi':'agro bisnis',
                    'jabatan':'staff'

                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_profile(payload=Depends(Autentication()), session=Depends(get_db_session)):
    # #optimistik (aku yakin di payload ada 'uid')
    # user_id = payload['uid']

    # pesimistik (aku tdk yakin di payload ada 'uid' ,dikasih default 0)
    user_id = payload.get('uid', 0)
    dataPengguna = False
    profile = session.execute(
        sa.select(
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
            User.id_karyawan == user_id
        )
    ).fetchone()
    
    if not profile:
        raise HTTPException(400, detail='User not found')
    
    nama_divisi = session.execute(sa.Select(Divisi.nama_divisi).where(Divisi.id_divisi == profile.divisi)).scalar()
    print(nama_divisi)

    return GetProfileResponseModel(data=ProfileModel(
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
        nama_divisi=nama_divisi
    ))
    
           

