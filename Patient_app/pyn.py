#learning  pydantic

from pydantic import BaseModel, EmailStr, AnyUrl,Field
from typing import List, Dict, Optional, Annotated


#type validation here
class Patient(BaseModel):
    #by default all fields are required

    name: str
    age: int
    weight: float
    allergies: List[str] #we are not using list only here because we have to validate what inside the list also same for dict
    contact_details: Dict[str, str]
    married: Optional[bool] = False #to make a field optional we use Optional, we can give a default value to fields also like given in this one

def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.allergies)
    print(patient.contact_details)
    print('inserted patient')

patient_info = {"name": "Ravi Mehta", "age": 27, "weight": 30.5, "allergies":['dust','pollen'], 'married': True,"contact_details":{'email':'abc@gmail.com','phone':'03074996048'}}


patient1 = Patient(**patient_info)

insert_patient(patient1)

#data validation here

class Patient(BaseModel):

    #using field now we are adding constraints and also aadding meta data
    name: Annotated[str, Field(max_length=50,title='name of patient', description='Give name of patient in less than 50 char')]
    age: Annotated[int, Field(gt=0, strict=True)] #strict means it cannot validate the type it should be int if an int is given in str it will not allow it
    email: EmailStr #datatype for email validation
    linkedin: AnyUrl #datatype for URL validation
    weight: float=Field(gt=0) #using Field here for custom data types validation and conditions acc to the business requirements
    allergies: Annotated[List[str], Field(max_length=5)]
    contact_details: Dict[str, str]
    married: Optional[bool] = False

def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.linkedin)
    print(patient.contact_details)
    print('inserted patient')

patient_info = {"name": "Ravi Mehta", "age": 27,'email':'abc@gmail.com','linkedin':'https://www.linkedin.com/feed/', "weight": 30.5, "allergies":['dust','pollen'], 'married': True,"contact_details":{'phone':'03074996048'}}


patient1 = Patient(**patient_info)

insert_patient(patient1)


