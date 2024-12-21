from typing import Optional
from fastapi import Depends,HTTPException,Response
import sqlalchemy as sa
from pydantic import BaseModel
from app.dependencies.autentication import Autentication

from app.models.rencana_kerja import RencanaKerja
from app.dependencies.get_db_session import get_db_session

from app.models.user import User

class DeleteRencanaKerjaData(BaseModel):
    id_rencana_kerja: int  = None

async def delete_rencana_kerja(data:DeleteRencanaKerjaData,payload=Depends(Autentication()),session=Depends(get_db_session)):

    # cek akses
    id_strong_user = payload.get('uid', 0)

    user_access = session.execute(sa.select(User.access).where(User.id_karyawan == id_strong_user)).scalar()
    print("Uacc",user_access) 
    if user_access < 3 :
        raise HTTPException(400, detail='anda tidak memiliki akses')

    # cek id tersedia
    id_exis = session.execute(
        sa.select(RencanaKerja.id_renker).where(RencanaKerja.id_renker == data.id_rencana_kerja)
        ).scalar()

    if not id_exis :
        raise HTTPException(
            400, detail='target yang dimaksud tidak tersedia')


    result = session.execute(
        sa.delete(RencanaKerja).where(RencanaKerja.id_renker == data.id_rencana_kerja)
    )
    if result.rowcount == 0:
        raise HTTPException(400, detail='Rencana kerja not found')


    session.commit()

    return