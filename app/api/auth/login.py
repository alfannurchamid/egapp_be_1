
# ========

import datetime
import time

import sqlalchemy as sa
from fastapi import Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from werkzeug.security import check_password_hash

from app.api_models import BaseResponseModel
from app.config import config
from app.dependencies.get_db_session import get_db_session
from app.models.user import User
from app.models.user_login import UserLogin
from app.utils.generate_access_token import generate_access_token
from app.utils.generate_refresh_token import generate_refresh_token




class LoginData(BaseModel):
    username: str
    password: str
    


class LoginDataResponseModel(BaseModel):
    id_karyawan: str
    refresh_token: str
    access_token: str
    expired_at: int


class LoginResponseModel(BaseResponseModel):
    data: LoginDataResponseModel

    class Config:
        json_schema_extra = {
            'example': {
                'data': {
                    'id_karyawan': 'A1000',
                    'refresh_token': 'abc.def.ghi',
                    'access_token': 'jkl,nmo.pqr',
                    'expired_at': 123456,
             
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def auth_login(data: LoginData, session=Depends(get_db_session)):
    # check username
    # jika device id = device id 
    username = data.username.lower()

    user = session.execute(
        sa.select(
            User.id_karyawan,
            User.password,
            User.access
        ).where(
            User.username == username
        )
    ).fetchone()

    if not user or not check_password_hash(user.password, data.password):
        raise HTTPException(400, detail='Username/password tidak sesuai')
    
    print(username)


    # expired_at = int(time.time()) + \
    #     config.REFRESH_TOKEN_EXPIRATION  # type: ignore

    payload = {
        'uid': user.id_karyawan,
        'username': username,
        'acceess':user.access,
    }
    refresh_token = generate_refresh_token(payload)  # type: ignore

    user_login = UserLogin(
        id_karyawan=user.id_karyawan,
        refresh_token=refresh_token,
        expired_at=sa.func.TIMESTAMPADD(
            sa.text('SECOND'),
            config.REFRESH_TOKEN_EXPIRATION,  # type: ignore
            datetime.datetime.now())
    )

    session.add(user_login)
    session.commit()

    access_token, access_token_expired_at = generate_access_token(payload)   # type: ignore

    return LoginResponseModel(
        data=LoginDataResponseModel(
            id_karyawan=user.id_karyawan,
            refresh_token=refresh_token,
            access_token=access_token,
            expired_at=access_token_expired_at,
        )
    )
