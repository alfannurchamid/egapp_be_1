
from typing import Optional

import sqlalchemy as sa
from fastapi import Depends, HTTPException, Response
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel , model_validator
from app.dependencies.autentication import Autentication

from app.dependencies.get_db_session import get_db_session
from app.models.user import User


class EditKaryawanData(BaseModel):
    id_karyawan :str
    full_name: Optional[str] =None
    email: Optional[str] =None
    noWa: Optional[str] =None
    nik: Optional[str] =None
    access: Optional[int] =None

    
    @model_validator(mode='before')
    def validate_confirm_password(cls, values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')

        if password and confirm_password != password:
            raise HTTPException(
                400, 'katasandi tidak sama ,ulangi dengan  benar !')

        return values


async def edit_karyawan(data: EditKaryawanData, payload=Depends(Autentication()), session=Depends(get_db_session)):
    id_strong_user = payload.get('uid', 0)

    user_access = session.execute(sa.select(User.access).where(User.id_karyawan == id_strong_user)).scalar()
    print("Uacc",user_access) 
    if user_access < 3 :
        raise HTTPException(400, detail='anda tidak memiliki akses')

    profile_data = jsonable_encoder(data)
    user_id = data.id_karyawan


    # TODO:
    values_to_update = {}

    if 'full_name' in profile_data and profile_data['full_name']:
        values_to_update.update({'full_name': profile_data['full_name']})


    if 'email' in profile_data and profile_data['email']:
        check_email = session.execute(
            sa.select(User.id_karyawan).where(
                sa.and_(
                    User.email == profile_data['email'],
                    User.id_karyawan != user_id
                )
            )
        ).fetchone()

        if check_email:
            raise HTTPException(400, 'email telah digunakan akun lain')
        values_to_update.update({'email': profile_data['email']})

    if 'noWa' in profile_data and profile_data['noWa']:
        check_noWa = session.execute(
            sa.select(User.id_karyawan).where(
                sa.and_(
                    User.noWa == profile_data['noWa'],
                    User.id_karyawan != user_id
                )
            )
        ).fetchone()

        if check_noWa:
            raise HTTPException(
                400, 'nomor whatsapp telah digunakan akun lain')
        values_to_update.update({'noWa': profile_data['noWa']})


    if 'alamat' in profile_data and profile_data['alamat']:
        values_to_update.update({'alamat': profile_data['alamat']})

    result = session.execute(
        sa.update(User).values(**values_to_update).where(User.id_karyawan == user_id)
    )

    if result.rowcount == 0:
        raise HTTPException(400, detail='User not found')

    session.commit()
    return Response(status_code=204)
