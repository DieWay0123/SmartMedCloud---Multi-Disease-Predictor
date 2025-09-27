from fastapi import APIRouter, Depends, Response

from models import MappingValue, MappingKey

from sqlalchemy.orm import Session
from sqlalchemy import desc

from dependencies import get_db

from schemas import FullMappingValueSchema, CUMappingValueSchema


router = APIRouter(prefix="/mapping_values")

@router.get("", response_model=list[FullMappingValueSchema])
def get_mapping_values(db: Session = Depends(get_db)):
    mapping_values = db.query(MappingValue).order_by(desc(MappingValue.id_)).all()
    return mapping_values

@router.post("", response_model=FullMappingValueSchema)
def create_mapping_value(data: CUMappingValueSchema, db: Session = Depends(get_db)):
    mapping_value_exist = db.query(MappingValue).filter(
        MappingValue.name == data.name,
        MappingKey.id_ == data.key_id).first()
    if mapping_value_exist:
        raise Exception()
    mapping_key_exist = db.query(MappingKey).filter(MappingKey.id_ == data.key_id).first()
    if not mapping_key_exist:
        raise Exception()
    new_mapping_value = MappingValue(name=data.name, key_id=data.key_id)
    db.add(new_mapping_value)
    db.commit()
    return new_mapping_value

@router.get("/{mapping_value_id}", response_model=FullMappingValueSchema)
def get_one_mapping_value(mapping_value_id: int, db: Session = Depends(get_db)):
    mapping_value = db.query(MappingValue).filter(MappingValue.id_ == mapping_value_id).first()
    if not mapping_value:
        raise Exception()
    return mapping_value

@router.put("/{mapping_value_id}", response_model=FullMappingValueSchema)
def fully_update_mapping_value(mapping_value_id: int, data: CUMappingValueSchema, db: Session = Depends(get_db)):
    mapping_value = db.query(MappingValue).filter(MappingValue.id_ == mapping_value_id).first()
    if not mapping_value:
        raise Exception()
    mapping_value_exist = db.query(MappingValue).filter(
        MappingValue.id_ != mapping_value_id, 
        MappingValue.name == data.name,
        MappingValue.key_id == data.key_id).first()
    if mapping_value_exist:
        raise Exception()
    mapping_key_exist = db.query(MappingKey).filter(MappingKey.id_ == data.key_id).first()
    if not mapping_key_exist:
        raise Exception()
    mapping_value.name = data.name
    mapping_value.key_id = data.key_id
    db.commit()
    return mapping_value

@router.delete("/{mapping_value_id}")
def delete_one_mapping_value(mapping_value_id: int, db: Session = Depends(get_db)):
    mapping_value = db.query(MappingValue).filter(MappingValue.id_ == mapping_value_id).first()
    if not mapping_value:
        raise Exception()
    db.delete(mapping_value)
    db.commit()
    return Response(status_code=204)