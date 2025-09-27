from fastapi import APIRouter, Depends, Response

from models import MappingKey, MappingValue

from sqlalchemy.orm import Session
from sqlalchemy import desc

from dependencies import get_db

from schemas import FullMappingKeySchema, CUMappingKeySchema


router = APIRouter(prefix="/mapping_keys")

@router.get("", response_model=list[FullMappingKeySchema])
def get_mapping_keys(db: Session = Depends(get_db)):
    mapping_keys = db.query(MappingKey).order_by(desc(MappingKey.id_)).all()
    return mapping_keys

@router.post("", response_model=FullMappingKeySchema)
def create_mapping_keys(data: CUMappingKeySchema, db: Session = Depends(get_db)):
    mapping_key_exist = db.query(MappingKey).filter(MappingKey.name == data.name).first()
    if mapping_key_exist:
        raise Exception()
    new_mapping_key = MappingKey(name=data.name)
    db.add(new_mapping_key)
    db.commit()
    return new_mapping_key

@router.get("/{mapping_key_id}", response_model=FullMappingKeySchema)
def get_one_mapping_key(mapping_key_id: int, db: Session = Depends(get_db)):
    mapping_key = db.query(MappingKey).filter(MappingKey.id_ == mapping_key_id).first()
    if not mapping_key:
        raise Exception()
    return mapping_key

@router.put("/{mapping_key_id}", response_model=FullMappingKeySchema)
def fully_update_mapping_key(mapping_key_id: int, data: CUMappingKeySchema, db: Session = Depends(get_db)):
    mapping_key = db.query(MappingKey).filter(MappingKey.id_ == mapping_key_id).first()
    if not mapping_key:
        raise Exception()
    mapping_key_exist = db.query(MappingKey).filter(
        MappingKey.id_ != mapping_key_id, 
        MappingKey.name == data.name).first()
    if mapping_key_exist:
        raise Exception()
    mapping_key.name = data.name
    db.commit()
    return mapping_key

@router.delete("/{mapping_key_id}")
def delete_one_mapping_key(mapping_key_id: int, db: Session = Depends(get_db)):
    mapping_key = db.query(MappingKey).filter(MappingKey.id_ == mapping_key_id).first()
    if not mapping_key:
        raise Exception()
    mapping_value_exist = db.query(MappingValue).filter(MappingValue.key_id == mapping_key_id).first()
    if mapping_value_exist:
        raise Exception()
    db.delete(mapping_key)
    db.commit()
    return Response(status_code=204)