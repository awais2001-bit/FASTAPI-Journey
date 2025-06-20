from typing_extensions import Self

from pydantic import BaseModel, EmailStr, AnyUrl,Field, field_validator, model_validator
from typing import List, Dict, Optional, Annotated, Any


class Patient(BaseModel):
    name: str
    age: int        #model validator means if we have two fields or more and whole pydantic model like if age is above 60 than there should be an emergency contact in the contact details
    email: EmailStr
    weight: float
    allergies: List[str]
    contact_details: Dict[str, str]
    married: Optional[bool] = False


    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError("no emergency contact")
        return model

def insert_patient(patient: Patient):
        print(patient.name)
        print(patient.age)
        print(patient.weight)
        print(patient.allergies)
        print(patient.contact_details)
        print('inserted patient')


patient_info = {"name": "Ravi Mehta", "age": 65, 'email': 'abc@allied.com', "weight": 30.5,
                "allergies": ['dust', 'pollen'], 'married': True, "contact_details": {'phone': '03074996048','emergency':'123456'}}

patient = Patient(**patient_info)

insert_patient(patient)