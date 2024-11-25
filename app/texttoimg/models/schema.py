from pydantic import BaseModel
from typing import Optional

class GenerateRequest(BaseModel):
    prompt: str
    style: str
    background: str = ""
    custom_background: str = ""
    negative_prompt: str = ""
    image_size : Optional[str] = "1024x1024"
    character_style: str = ""

class GenerateResponse(BaseModel):
    request_id: str
    image_id: str
    prompt: str
    style: str
    background: str
    custom_background: str
    negative_prompt: str
    image_size: str
    character_style: str
    image_url: str
    

class RegenerateRequest(BaseModel):
    request_id: str
    prompt: str = None
    background: str = None
    custom_background: str = None
    negative_prompt: str = None
    image_size: str = None
    character_style: str = None
    