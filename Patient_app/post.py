from fastapi import FastAPI,Path,Query,HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
import json
from typing import Annotated, Literal,Optional


app = FastAPI()



class Patient(BaseModel):
    id: Annotated[str,Field(...,description="id of the patient")]
    name: Annotated[str,Field(...,description="name of the patient")]
    city: Annotated[str,Field(...,description="city of the patient")]
    age: Annotated[int,Field(...,gt=0,lt=110,description="age of the patient")]
    gender: Annotated[Literal['male','female','others'],Field(...,description="gender of the patient")]
    height: Annotated[float,Field(...,gt=0,description="height of the patient in mtr")]
    weight: Annotated[float,Field(...,gt=0,description="weight of the patient in kg")]


    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight / (self.height * self.height), 2)
        return bmi

    @computed_field
    @property
    def verdict(self)-> str:
        if self.bmi<18.5:
            return 'underweight'
        elif self.bmi<30:
            return 'normal'
        else:
            return 'obese'

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field( gt=0, lt=110, default=None)]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None)]
    height: Annotated[Optional[float], Field(gt=0, default=None)]
    weight: Annotated[Optional[float], Field(gt=0, default=None)]

def load_data():
    with open('patient.json', 'r') as f:
        data = json.load(f)

        return data

def save_data(data):
    with open('patient.json', 'w') as f:
        json.dump(data, f)


@app.post('/create')
def create_patient(patient: Patient):

    #load existing data

    data = load_data()

    #check if patient already exist

    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient with this id already exists')

    #add patient object to data dictionary
    data[patient.id] = patient.model_dump()

    #save data to json file
    save_data(data)


    return JSONResponse(status_code=201, content={'message':'patient created successfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient with this id does not exist')

    patient_info = data[patient_id]

    updated_info = patient_update.model_dump(exclude_unset=True)

    for key,value in updated_info.items():
         patient_info[key] = value

    patient_info['id'] = patient_id
    patient_obj = Patient(**patient_info)
    patient_info = patient_obj.model_dump(exclude='id')

    data[patient_id] = patient_info

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated successfully'})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient with this id does not exist')

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted successfully'})