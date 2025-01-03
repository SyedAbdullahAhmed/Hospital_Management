from fastapi import FastAPI,Request,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pymongo import MongoClient
from bson import ObjectId
import controllers.loginController as loginController
import controllers.patientController as patientController
import controllers.doctorController as doctorController


uri = ""

client = MongoClient(uri)
database = client.get_database("hospital-management")
admins = database.get_collection("admins")

app = FastAPI()

origins = ["http://localhost:3000"]  
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

# admin login
@app.get("/hospitalManagement/login/{name}")
async def root(name):
    return await loginController.admin_login(name)
    
@app.post("/hospitalManagement/addAdmin")
async def root(request:Request):
    return await loginController.add_admin(request)
    
# patient
@app.get("/hospitalManagement/patient")
async def root():
    return patientController.get_patient()

@app.post("/hospitalManagement/patient")
async def root(request:Request):
    return await patientController.add_patient(request)

@app.put("/hospitalManagement/patient/{id}")
async def root(request:Request,id):
    return await patientController.update_patient(request,id)

@app.delete("/hospitalManagement/patient/{id}")
async def root(id):
    return patientController.delete_patient(id)


# doctor
@app.get("/hospitalManagement/doctor")
async def root():
    return doctorController.get_doctor()

@app.post("/hospitalManagement/doctor")
async def root(request: Request):
    return await doctorController.add_doctor(request)

@app.put("/hospitalManagement/doctor/{id}")
async def root(request: Request, id):
    return await doctorController.update_doctor(request, id)

@app.delete("/hospitalManagement/doctor/{id}")
async def root(id):
    return doctorController.delete_doctor(id)




if __name__ == "__main__": 
    loginController.load_admins()
    patientController.load_patients()
    doctorController.load_doctors()
    uvicorn.run(app, host="0.0.0.0", port=4000, reload=True)