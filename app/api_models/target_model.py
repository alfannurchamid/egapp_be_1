from datetime import datetime
from typing import List
from pydantic import BaseModel
 
class TargetModel(BaseModel):
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
    progres : int
    prioritas : int