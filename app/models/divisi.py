import sqlalchemy as sa

from app.models import Base


class Divisi(Base):
    __tablename__ = 'divisi'
    id_divisi = sa.Column('id_divisi',sa.Integer,primary_key=True,autoincrement=True)
    nama_divisi = sa.Column('nama_divisi',sa.String)
    path_foto = sa.Column('path_foto',sa.String)