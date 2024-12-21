import datetime
import sqlalchemy as sa
from fastapi import Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from app.api_models import BaseResponseModel
from app.config import config
from app.dependencies.get_db_session import get_db_session
from app.models.user import User
from app.models.user_login import UserLogin
from app.utils.generate_access_token import generate_access_token


class RefreshTokenData(BaseModel):
    refresh_token: str


class RefreshTokenDataResponseModel(BaseModel):
    access_token: str
    expired_at: int


class RefreshTokenResponseMode(BaseResponseModel):
    data: RefreshTokenDataResponseModel

    class Config:
        json_schema_extra = {
            'example': {
                'data': {
                    'refresh_token': 'abc.def.ghi',
                    'expired_at': 123456
                },
                'meta': {},
                'message': 'Success',
                'success': True,
                'code': 200
            }
        }


async def auth_refresh_token(data: RefreshTokenData, session=Depends(get_db_session)):
    # cek refresh token
    user_login = session.execute(
        sa.select(
            UserLogin.id_karyawan,
            User.id_karyawan.label('id_karyawan'),
            User.username,
            sa.func.if_(
                UserLogin.expired_at > sa.func.NOW(), 0, 1
            ).label(
                'expired'
            )
        ).where(
            UserLogin.id_karyawan == User.id_karyawan,
            UserLogin.refresh_token == data.refresh_token
        )
    ).fetchone()

    if not user_login:
        raise HTTPException(status_code=400, detail='Reftesh token not found')

    if user_login.expired:
        print(user_login.expired,"expired")
        raise HTTPException(status_code=403, detail={
            'message': 'Reftesh token expaied',
            'code': 40301
        }
        )
    # extend expiration of refresh token
    session.execute(
        sa.update(
            UserLogin
        ).values(
            expired_at=sa.func.TIMESTAMPADD(
                sa.text('SECOND'),
                config.REFRESH_TOKEN_EXPIRATION,
                datetime.datetime.now()
            )
        )
    )

    # generate acces token yang baru
    payload = {
        'uid': user_login.id_karyawan,
        'username': user_login.username,
    }
    access_token, expired_at = generate_access_token(payload)  # type: ignore

    session.commit()

    return RefreshTokenResponseMode(
        data=RefreshTokenDataResponseModel(
            access_token=access_token,
            expired_at=expired_at
        )

    )
