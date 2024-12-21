from fastapi import Depends,HTTPException,Response
import sqlalchemy as sa
from pydantic import BaseModel, model_validator
import datetime
from app.dependencies.autentication import Autentication

from app.models.catatan_renker import CatatanRenker
from app.models.user import User
from app.dependencies.get_db_session import get_db_session
from app.dependencies.str_to_date import str_to_date

class AddCatatanRenkerData(BaseModel):
    id_renker:int
    catatan :str

async def add_catatan_renker(data:AddCatatanRenkerData,payload=Depends(Autentication()),session=Depends(get_db_session)):

    catatan_renker = CatatanRenker(
        id_renker = data.id_renker,
        catatan = data.catatan,
       
    )

    session.add(catatan_renker)
    session.commit()

    return