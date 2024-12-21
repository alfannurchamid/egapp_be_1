from app.models import Base
import datetime

import sqlalchemy as sa


class User(Base):
    __tablename__ = 'user'
    id_karyawan = sa.Column('id_karyawan', sa.String, primary_key=True)
    username = sa.Column('username', sa.String,default=sa.null)
    nik = sa.Column('nik', sa.String, default=sa.null)
    password = sa.Column('password', sa.String,default=sa.null)
    full_name = sa.Column('full_name', sa.String)
    email = sa.Column('email', sa.String, default=sa.null)
    alamat = sa.Column('alamat', sa.String, default=sa.null)
    noWa = sa.Column('noWa', sa.String,default=sa.null)
    access = sa.Column('access', sa.Integer, default=0)
    path_foto = sa.Column('path_foto', sa.String, default=sa.null)
    created_at = sa.Column('created_at', sa.DateTime(
        timezone=True), default=datetime.datetime.now())
    modifed_at = sa.Column('modifed_at', sa.DateTime(timezone=True),
                           default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    divisi = sa.Column('divisi', sa.Integer)
    jabatan = sa.Column('jabatan',sa.String)
    jenis_kelamin = sa.Column('jenis_kelamin',sa.String)
    tgl_lahir = sa.Column('tgl_lahir', sa.DateTime())

 

