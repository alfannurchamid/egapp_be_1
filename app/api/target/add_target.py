from fastapi import Depends,HTTPException,Response
import sqlalchemy as sa
from pydantic import BaseModel, model_validator
import datetime
from app.dependencies.autentication import Autentication

from app.models.target import Target
from app.dependencies.get_db_session import get_db_session
from app.dependencies.str_to_date import str_to_date

class AddTargettData(BaseModel):
    judul:str
    deskripsi :str
    kpi: str
    start_date : str
    deadline: str
    id_divisi : int

async def target_add(data:AddTargettData,payload=Depends(Autentication()),session=Depends(get_db_session)):
    judul_exis = session.execute(
        sa.select(Target.judul).where(Target.judul == data.judul)
        ).scalar()

    # cek nik tersedia
    if judul_exis :
        raise HTTPException(
            400, detail='judul sudah terdaftar')


    target = Target(
        judul = data.judul,
        deskripsi = data.deskripsi,
        kpi = data.kpi,
        start_date = str_to_date(data.start_date),
        deadline = str_to_date(data.deadline),
        id_divisi = data.id_divisi
    )

    session.add(target)
    session.commit()

    return