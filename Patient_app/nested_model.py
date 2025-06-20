#using a pydantic model in another model as field is known as nested model
#benifits
#better organization of related data
#Reusability
#Readability
#Validation nested models are validated auto no extra work needed


from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin: int

class Patient(BaseModel):

    name: str
    age: int
    gender: str
    adress: Address #so in this adress we have multiple data types included so we can use a model here


adress_dict = {'city':'lahore','state':'punjab','pin':12345}
adress = Address(**adress_dict)

patient_dict={'name':'awais','age':21,'gender':'male','adress':adress}
patient = Patient(**patient_dict)

print(patient)

temp = patient.model_dump() #dictinory
#temp = patient.model_dump_json()
#temp = patient.model_dump(include=['name']) # this will include name and will print name only like include we have exclude option also
print(type(temp))


#pydantic gives us builtin methods to export our models in dict or json format i.e serialization
