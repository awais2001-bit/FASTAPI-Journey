from pydantic import BaseModel, EmailStr, AnyUrl,Field, field_validator
from typing import List, Dict, Optional, Annotated

#why we use field validation because we can have some constraitns acc to our business req like we can give discount only to our customers of bank so we should validate bank email.
#a field validator works in two modes i.e before mode and after mode
#field validation here
class Patient(BaseModel):


    name: str
    age: int
    email: EmailStr
    weight: float
    allergies: List[str] #we are not using list only here because we have to validate what inside the list also same for dict
    contact_details: Dict[str, str]
    married: Optional[bool] = False

    @field_validator('email')
    @classmethod
    def validate_email(cls, value): #cls means we can access to other methods in our class
        valid_domains = ['allied.com', 'hbl.com', 'meezan.com']

        domain = value.split('@')[-1]
        if domain not in valid_domains:
            raise ValueError(f'Domain {domain} not valid')
        return value

    @field_validator('name',) #transformation happening here also mode means that we will get the value after type coercion and by deefault it is after
    @classmethod
    def validate_name(cls, value):
        return value.upper()

    @field_validator('age', mode='after') #mode means that we will get the value after type coercion and by deefault it is after
    @classmethod
    def validate_age(cls, value): #in this example the method is taking value before type coercion if it will be string it will not do it and raise error
        if 0 < value <= 50:
            return value
        else:
            raise ValueError(f'Age {value} is not valid')

def insert_patient(patient: Patient):
        print(patient.name)
        print(patient.age)
        print(patient.weight)
        print(patient.allergies)
        print(patient.contact_details)
        print('inserted patient')


patient_info = {"name": "Ravi Mehta", "age": 27,'email':'abc@allied.com', "weight": 30.5, "allergies":['dust','pollen'], 'married': True,"contact_details":{'phone':'03074996048'}}

patient = Patient(**patient_info)

insert_patient(patient)