from pymongo import MongoClient
from datetime import datetime
from app.config import MONGO_URI

# MongoDB Atlas configuration

client = MongoClient(MONGO_URI)
db = client.image_generator
collection = db.images

def save_metadata(request_id:str,image_id: str, prompt: str,style:str, background:str,custom_background:str,negative_prompt:str,image_size:str,lighting:str,color_palette:str,camera_angle:str,character_expression:str,character_style:str,s3_url: str):
    image_data = {

        "_id": request_id,
        "generations":[{
            "image_id":image_id,
            "prompt": prompt,
            "style": style,
            "background":background,
            "custom_background":custom_background,
            "negative_prompt": negative_prompt,
            "image_size": image_size,
            "character_style": character_style,
            "image_urls": s3_url,
            "created_at":datetime.utcnow()
        }]
    }
    collection.insert_one(image_data)

def update_metadata(request_id:str,image_id: str, prompt: str,style:str,background:str, custom_background:str,negative_prompt:str,image_size:str,lighting:str,color_palette:str,camera_angle:str,character_expression:str,character_style:str,s3_url: str):
    collection.update_one({"_id": request_id}, 
                          {"$push":{
                            "generations":{
                                "image_id":image_id,
                                "prompt": prompt,
                                "style":style, 
                                "background": background,
                                "custom_background":custom_background,
                                "negative_prompt": negative_prompt,
                                "image_size": image_size,
                                "character_style": character_style,
                                "image_urls": s3_url,
                                "created_at":datetime.utcnow()
                                }
                            }}
                         )
                            
def get_metadata(request_id: str):
    return collection.find_one({"_id": request_id})

def delete_metadata(request_id: str,image_id:str):
    collection.update_one({"_id": request_id},
                          {"$pull":{"generations":{"image_id":image_id}}}
                          )


