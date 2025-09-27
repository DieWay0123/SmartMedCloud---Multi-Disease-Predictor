from typing import Literal

from pydantic import BaseModel

from datetime import datetime


class BaseSchema(BaseModel):
    id_: int
    created_at: datetime


class CUMappingKeySchema(BaseModel):
    name: str


class MappingKeySchema(BaseSchema, CUMappingKeySchema): pass


class CUMappingValueSchema(BaseModel):
    name: str
    key_id: int


class MappingValueSchema(BaseSchema, CUMappingValueSchema): pass


class FullMappingKeySchema(MappingKeySchema):
    mapping_values: list[MappingValueSchema] = []


class FullMappingValueSchema(MappingValueSchema):
    mapping_key: MappingKeySchema


class DiabetesPredictInput(BaseModel):
    gender: Literal[0, 1]
    age: int
    bmi: float
    hba1c: float
    blood_sugar: float


class DiabetesPredictOutput(BaseModel):
    have_diabetes: bool
    diabetes_percentage: float
