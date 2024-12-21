import datetime
from email.policy import default

import sqlalchemy as sa

from app.models import Base


class UserLogin(Base):
    __tablename__ = 'userLogin'
    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    id_karyawan = sa.Column('id_karyawan', sa.String)
    refresh_token = sa.Column('refresh_token', sa.String)
    expired_at = sa.Column('expired_at', sa.DateTime,
                           default=datetime.datetime.now())
    created_at = sa.Column('created_at', sa.DateTime,
                           default=datetime.datetime.now())
    modified_at = sa.Column('modified_at', sa.DateTime,
                            default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    user_number = sa.Column('user_number',sa.Integer) #baru
