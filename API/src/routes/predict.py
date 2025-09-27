from fastapi import APIRouter, Depends, UploadFile

from settings import settings

import pandas as pd

import joblib

from schemas import DiabetesPredictInput, DiabetesPredictOutput


REQUIRED_COLUMNS = ['gender', 'age', 'bmi', 'HbA1c_level', 'blood_glucose_level']

router = APIRouter(prefix="/predict")

@router.post("/diabetes", response_model=DiabetesPredictOutput)
def predict_diabetes(data: DiabetesPredictInput):
    user_input = pd.DataFrame(data=[[data.gender, data.age, data.bmi, data.hba1c, data.blood_sugar]], columns=REQUIRED_COLUMNS)
    model = joblib.load(f"{settings.models_root}/{settings.diabetes_model_path}")
    have_diabetes = False if model.predict(user_input)[0] == 0 else True
    diabetes_percentage = round(float(model.predict_proba(user_input)[0][1] * 100), 2)
    return DiabetesPredictOutput(have_diabetes=have_diabetes, diabetes_percentage=diabetes_percentage).model_dump()