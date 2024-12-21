import datetime
from email.policy import default

import sqlalchemy as sa

from app.models import Base


class CatatanTugas(Base):
    __tablename__ = 'catatan_tugas'
    id_catatan = sa.Column('id_catatan',sa.Integer,primary_key=True,autoincrement=True)
    id_tugas =  sa.Column('id_tugas',sa.Integer)
    catatan =  sa.Column('catatan',sa.String)

