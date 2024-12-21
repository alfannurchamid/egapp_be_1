
from pydantic import BaseModel
from app.api_models.profile_model import ProfileModel
 
class DivisiModel(BaseModel):
    id_divisi:int
    nama_divisi:str
    path_foto:str
    jml_karyawan:int
    manager:ProfileModel | None
   