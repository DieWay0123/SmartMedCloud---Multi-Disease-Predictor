from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from settings import settings

from dependencies import get_db

from datetime import datetime, timedelta, timezone

import pandas as pd

from io import BytesIO

from models import MappingKey, MappingValue


router = APIRouter(prefix="/files")

@router.post("")
def files_post(file: UploadFile, db: Session = Depends(get_db)):
    if file.content_type != "text/csv":
        raise Exception()
    
    dt = datetime.now(timezone(timedelta(hours=8)))
    dt_fmt = dt.strftime('%-Y-%m-%d-%H-%M-%S-%f')[:-2]
    
    filename_raw = dt_fmt + "_raw_" + file.filename
    filename = dt_fmt + "_" + file.filename

    mapping_keys = db.query(MappingKey).all()
    column_mappings: dict[str, list[str]] = {}

    #自資料庫讀取並建立鍵值對
    for mapping_key in mapping_keys:
        column_mappings[mapping_key.name] = [mapping_value.name for mapping_value in mapping_key.mapping_values]

    #轉為二進位資料
    file.file.seek(0)
    binary = BytesIO(file.file.read())

    #讀取csv檔並將原始資料存起來
    df = pd.read_csv(binary)
    df.to_csv(path_or_buf=f"{settings.fs_root}/{filename_raw}")

    #重命名所有欄位為全小寫英文字母
    df.rename(columns=lambda x: x.strip().lower(), inplace=True)

    #過濾所需欄位
    df_filtered = pd.DataFrame()
    for column_name in df.columns:
        for mapping_key in column_mappings:
            if column_name == mapping_key or column_name in column_mappings[mapping_key]:
                df_filtered[mapping_key] = df[column_name]
                break

    df_filtered.dropna(inplace=True)
    df_filtered.to_csv(path_or_buf=f"{settings.fs_root}/{filename}", index=0)
    
    return JSONResponse(content={"message": "Success"}, status_code=200)