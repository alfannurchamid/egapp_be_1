from typing import List, Optional

import jwt
import sqlalchemy as sa
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.api_models import BaseResponseModel
from app.api_models.target_model import TargetModel
from app.config import config
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.models.target import Target
from app.models.user import User


class GetTargetsData(BaseModel):
    id_divisi : int 
    

class GetDataTargetsResponseModel(BaseResponseModel):
    data: List[object]

    class Config:
        json_schema_extra = {
            'example': {
                'data': {
                    'data':
                        [
                            {   "id_target":1,
                                "judul": "omset 200 jt per bulan",
                                "id_divisi": 2,
                                "deskripsi":"harus omset 200 jt per bulan",
                                "kpi":"ommset",
                                "deadline":2024/12/23,
                                "start_date":2024/12/23,
                                "catatan":"ini catatatn ",
                                "file_name":"filenname.jpg",
                                "modifed_at" : 2024/12/23
                            }
                        ],
                    'jum': 10
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_targets(data:GetTargetsData,payload=Depends(Autentication()), session=Depends(get_db_session)):
    access = 0
    divisi = ""
    data_ = jsonable_encoder(data)
    # ambill id payload
    user_id = payload.get('uid', 0)
    # access = payload.get('acceess',0)
    user_data = session.execute(sa.select(User.access,User.divisi).where(User.id_karyawan == user_id)).fetchone()
    # print(data_["id_divisi"],"ID DIVISI")
    print(user_id,"user id")
    access = user_data.access
    
    print(access,"access")
    if  access < 2 :
        raise HTTPException(400, detail='User not have access')
    elif access == 2: 
        divisi= f"WHERE id_divisi = {user_data.divisi}"
    else :
        divisi= f"WHERE id_divisi = {data_["id_divisi"]}"



    targets = session.execute(sa.text(f'SELECT * FROM target {divisi} ORDER BY id_target DESC' )).all()

    dataLList=[]

    for target in targets:
        dataLList.append(
            TargetModel(
                    id_target = target.id_target,
                    judul = target.judul,
                    kpi= target.kpi,
                    deskripsi=target.deskripsi,
                    start_date = target.start_date,
                    modifed_at = target.modifed_at,
                    deadline = target.deadline,
                    catatan = target.catatan,
                    file_name = target.file_name,
                    id_divisi = target.id_divisi,
                    status = target.status,
                    progres = target.progres,
                    prioritas= target.prioritas
            )
        )
    

    return GetDataTargetsResponseModel(
        data=dataLList)



