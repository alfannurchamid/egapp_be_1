import datetime
from email.policy import default

import sqlalchemy as sa

from app.models import Base


class CatatanRenker(Base):
    __tablename__ = 'catatan_renker'
    id_catatan = sa.Column('id_catatan',sa.Integer,primary_key=True,autoincrement=True)
    id_renker =  sa.Column('id_renker',sa.Integer)
    catatan =  sa.Column('catatan',sa.String)


