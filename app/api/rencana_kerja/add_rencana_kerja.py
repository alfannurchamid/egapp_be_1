from fastapi import Depends,HTTPException,Response
import sqlalchemy as sa
from pydantic import BaseModel, model_validator
import datetime
from app.dependencies.autentication import Autentication

from app.models.rencana_kerja import RencanaKerja
from app.models.target import Target
from app.dependencies.get_db_session import get_db_session
from app.dependencies.str_to_date import str_to_date

class AddRencanaKerjaData(BaseModel):
    judul:str
    deskripsi :str
    kpi: str
    start_date : str
    deadline: str
    id_target: int

async def rencana_kerja_add(data:AddRencanaKerjaData,payload=Depends(Autentication()),session=Depends(get_db_session)):
    judul_exis = session.execute(
        sa.select(RencanaKerja.judul).where(RencanaKerja.judul == data.judul)
        ).scalar()

    # cek nik tersedia
    if judul_exis :
        raise HTTPException(
            400, detail='judul sudah terdaftar')
    
    id_divisi = session.execute(sa.select(Target.id_divisi).where(Target.id_target == data.id_target)).scalar()


    target = RencanaKerja(
        judul = data.judul,
        deskripsi = data.deskripsi,
        kpi = data.kpi,
        start_date = str_to_date(data.start_date),
        deadline = str_to_date(data.deadline),
        id_divisi = id_divisi,
        id_target = data.id_target
    )


    session.add(target)
    session.commit()

    return