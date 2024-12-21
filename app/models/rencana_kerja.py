import datetime
from email.policy import default

import sqlalchemy as sa

from app.models import Base


class RencanaKerja(Base):
    __tablename__ = 'rencana_kerja'
    id_renker = sa.Column('id_renker',sa.Integer,primary_key=True,autoincrement=True)
    judul =  sa.Column('judul',sa.String, unique=True)
    kpi =  sa.Column('kpi',sa.String)
    deskripsi =  sa.Column('deskripsi',sa.String)
    created_at =  sa.Column('created_at',sa.DateTime, default=datetime.datetime.now())
    start_date  =  sa.Column('start_date',sa.DateTime)
    deadline  =  sa.Column('deadline',sa.DateTime)
    catatan =  sa.Column('catatan',sa.String)
    file_name =  sa.Column('file_name',sa.String)
    id_target =  sa.Column('id_target',sa.String)
    modifed_at = sa.Column('modifed_at',sa.DateTime)
    id_divisi = sa.Column('id_divisi',sa.Integer)
    status = sa.Column('status',sa.Integer,default=0)
    progres = sa.Column('progres',sa.Integer,default=0)
    prioritas = sa.Column('prioritas',sa.Integer,default=4)

