from fastapi import Depends,HTTPException,Response
import sqlalchemy as sa
from pydantic import BaseModel, model_validator

from app.models.user import User
from app.dependencies.get_db_session import get_db_session
from werkzeug.security import generate_password_hash



class AddKaryawantData(BaseModel):
    id_karyawan:str
    nik :str
    full_name: str
    alamat : str
    jenis_kelamin: str
    divisi : int
    jabatan : int
    access : int


async def karyawan_add(data:AddKaryawantData,session=Depends(get_db_session)):
    nik_exis = session.execute(
        sa.select(User.nik).where(User.nik == data.nik)
        ).scalar()

    # cek nik tersedia
    if nik_exis :
        raise HTTPException(
            400, detail='nik sudah terdaftar')
    
    id_karyawan = session.execute(
        sa.select(User.id_karyawan).where(User.id_karyawan == data.id_karyawan)
        ).scalar()

    # cek nik tersedia
    if id_karyawan :
        raise HTTPException(
            400, detail='id karyawan sudah terdaftar')
    
    user = User(
        id_karyawan= data.id_karyawan,
        nik = data.nik,
        full_name = data.full_name,
        alamat = data.alamat,
        jenis_kelamin = data.jenis_kelamin,
        divisi = data.divisi,
        jabatan = data.jabatan,
        access = data.access 
    )

    session.add(user)
    session.commit()

    return