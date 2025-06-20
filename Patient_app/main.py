from fastapi import FastAPI,Path,HTTPException, Query
import json


app = FastAPI()

#load data from patients.json file
def load_data():
    with open('patient.json', 'r') as f:
        data = json.load(f)

        return data

@app.get("/")
def hello():
    return "Welcome to Patient API"

#view all the patients data
@app.get("/view")
def view():
    data = load_data()
    return data


#path parameter and path function example getting specific patient id data
@app.get("/patient/{patient_id}")
def view(patient_id:str = Path(..., description="This is Patient ID in database", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    #return {'error': 'Patient not found'}
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str=Query(..., description="Patient sort on the basis of weight, height, bmi"),order: str=Query('asc', description="Patient sort in asc or dsc")):
    valid_fields = ['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Sort field must be one of {valid_fields}")
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail=f"Sort order must be one of asc or desc")

    data = load_data()

    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key=lambda x:x.get(sort_by,0),reverse=sort_order)
    return sorted_data


