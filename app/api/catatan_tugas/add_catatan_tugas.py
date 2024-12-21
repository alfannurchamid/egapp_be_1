from fastapi import Depends,HTTPException,Response
import sqlalchemy as sa
from pydantic import BaseModel, model_validator
import datetime
from app.dependencies.autentication import Autentication

from app.models.catatan_tugas import CatatanTugas
from app.models.user import User
from app.dependencies.get_db_session import get_db_session
from app.dependencies.str_to_date import str_to_date

class AddCatatanTugasData(BaseModel):
    id_tugas:int
    catatan :str

async def add_catatan_tugas(data:AddCatatanTugasData,payload=Depends(Autentication()),session=Depends(get_db_session)):

    catatan_tugas = CatatanTugas(
        id_tugas = data.id_tugas,
        catatan = data.catatan,
       
    )

    session.add(catatan_tugas)
    session.commit()

    return