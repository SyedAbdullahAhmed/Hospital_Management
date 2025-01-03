from fastapi import HTTPException
from pymongo import MongoClient
import json
from bson import ObjectId
from main import uri



def load_admins():
    client = MongoClient(uri)
    database = client.get_database("hospital-management")
    __admins = database.get_collection("admins")
    
    return __admins

async def admin_login(name):
    try:
        __admins=load_admins()
        
        admin = __admins.find_one({'name': name})
        

        if admin is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        admin['_id'] = str(admin['_id'])
        
        return {
            "success": True,
            "message": "User data found successfully",
            "data": admin
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")

async def add_admin(request): 
    try:
        __admins=load_admins()
        admin_info= await request.json()
        created_admin = __admins.insert_one(admin_info)
        
        if created_admin.inserted_id == None:
            print("Admin is not created")
            return {
                "success": False,
                "message": "Admin is not created",
                "data": []
            }
        print("Admin is created")
        res={
            "success": True,
            "message": "Admin created successfully",
            "data": str(created_admin.inserted_id)
        }
        return res

    except Exception as e:
        print("Admin is not created")
        raise HTTPException(status_code=500, detail=f"Some error occurred:{e}")
