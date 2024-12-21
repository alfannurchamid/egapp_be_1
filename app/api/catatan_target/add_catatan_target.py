from fastapi import Depends,HTTPException,Response
import sqlalchemy as sa
from pydantic import BaseModel, model_validator
import datetime
from app.dependencies.autentication import Autentication

from app.models.catatan_target import CatatanTarget
from app.models.user import User
from app.dependencies.get_db_session import get_db_session
from app.dependencies.str_to_date import str_to_date

class AddCatatanTargrtData(BaseModel):
    id_target:int
    catatan :str

async def add_catatan_target(data:AddCatatanTargrtData,payload=Depends(Autentication()),session=Depends(get_db_session)):

    catatan_target = CatatanTarget(
        id_target = data.id_target,
        catatan = data.catatan,
       
    )

    session.add(catatan_target)
    session.commit()

    return