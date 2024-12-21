from typing import Optional
from fastapi import Depends,HTTPException,Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete
import sqlalchemy as sa
from pydantic import BaseModel, model_validator
import datetime
from app.dependencies.autentication import Autentication

from app.models.target import Target
from app.dependencies.get_db_session import get_db_session
from app.dependencies.str_to_date import str_to_date
from app.models.user import User

class DeleteTargetData(BaseModel):
    id_target:Optional[int] = None




async def delete_target(data:DeleteTargetData,payload=Depends(Autentication()),session=Depends(get_db_session)):

    # cek akses
    id_strong_user = payload.get('uid', 0)

    user_access = session.execute(sa.select(User.access).where(User.id_karyawan == id_strong_user)).scalar()
    print("Uacc",user_access) 
    if user_access < 3 :
        raise HTTPException(400, detail='anda tidak memiliki akses')

    # cek id tersedia
    id_exis = session.execute(
        sa.select(Target.id_target).where(Target.id_target == data.id_target)
        ).scalar()

    if not id_exis :
        raise HTTPException(
            400, detail='target yang dimaksud tidak tersedia')

    target_data = jsonable_encoder(data)
    # TODO:
    values_to_update = {}

    result = session.execute(
        sa.delete(Target).where(Target.id_target == data.id_target)
    )
    if result.rowcount == 0:
        raise HTTPException(400, detail='Target not found')


    session.commit()

    return