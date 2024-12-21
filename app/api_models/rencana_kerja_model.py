from datetime import datetime
from typing import List
from pydantic import BaseModel
 
class RencanaKerjaModel(BaseModel):
    id_renker:int
    id_target :int
    judul : str
    kpi: str
    deskripsi:str
    start_date : datetime
    modifed_at : datetime | None
    deadline : datetime
    catatan : str | None
    file_name : str | None
    id_divisi : int
    status : int
    prioritas : int
    progres : int