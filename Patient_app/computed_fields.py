#the field which is created with the help of other fields and not provided from the user is known as computed fields
#example we are going to calculate bmi on the basis of weight and height

from pydantic import BaseModel, EmailStr, AnyUrl,Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated, Any


class Patient(BaseModel):
    name: str
    age: int
    email: EmailStr
    weight: float
    height: float
    allergies: List[str]
    contact_details: Dict[str, str]
    married: Optional[bool] = False


    @computed_field
    @property
    def cal_bmi(self) ->float:
        bmi = round(self.weight / (self.height * self.height), 2)
        return bmi

def insert_patient(patient: Patient):
        print(patient.name)
        print(patient.age)
        print(patient.weight)
        print(patient.allergies)
        print(patient.contact_details)
        print(patient.cal_bmi) #method name will be called if we call bmi it will give error, example given below
        #print(patient.bmi)
        print('inserted patient')


patient_info = {"name": "Ravi Mehta", "age": 65, 'email': 'abc@allied.com', "weight": 60,'height':1500,
                "allergies": ['dust', 'pollen'], 'married': True,
                "contact_details": {'phone': '03074996048', 'emergency': '123456'}}

patient = Patient(**patient_info)

insert_patient(patient)