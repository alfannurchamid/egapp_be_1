import datetime
from email.policy import default

import sqlalchemy as sa

from app.models import Base


class CatatanTarget(Base):
    __tablename__ = 'catatan_target'
    id_catatan = sa.Column('id_catatan',sa.Integer,primary_key=True,autoincrement=True)
    id_target =  sa.Column('id_target',sa.Integer)
    catatan =  sa.Column('catatan',sa.String)


