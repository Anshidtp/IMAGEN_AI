from fastapi import APIRouter,HTTPException,FastAPI
import replicate
import uuid
import requests
import os

import logging

from datetime import datetime
from app.config import API_KEY
from app.texttoimg.models.schema import GenerateRequest,RegenerateRequest,GenerateResponse
from app.texttoimg.utils.s3_utils import upload_to_s3,delete_from_s3
from app.texttoimg.utils.db_utils import save_metadata,update_metadata,get_metadata,delete_metadata


session = requests.Session()
session.cache_disabled = True


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Authenticating the token
client = replicate.Client(api_token=API_KEY)

# directory for storing downloaded images 
img_dir = "temp_storage"
os.makedirs(img_dir,exist_ok=True)

# Model mappings based on styles
styles_mapping = {
    "general": "{prompt}, high quality, detailed, visually appealing",
    "cinematic": "\"cinematic\" film still of {prompt}, highly detailed, high budget hollywood movie, cinemascope, moody, epic, gorgeous, film grain",
    "anime": "\"anime artwork\" of {prompt}, anime style, key visual, vibrant, studio anime, highly detailed",
    "photographic": "cinematic photo of {prompt}, 35mm photograph, film, professional, 8k, highly detailed",
    "comic": "comic of {prompt}, graphic illustration, comic art, graphic novel art, vibrant, highly detailed",
    "realistic": "\"realistic\" rendering of {prompt}, photorealistic, highly detailed, professional photography, ultra-high resolution,16K,HD",
    "3d": "\"3D rendering\" of {prompt}, highly detailed, realistic textures, CGI, high definition, professional quality",
    "cyberpunk": "\"cyberpunk style depiction\" of {prompt}, futuristic, neon lights, dystopian, high-tech, dark atmosphere, highly detailed",
    "abstract": "\"abstract representation\" of {prompt}, surreal, imaginative, vibrant colors, highly detailed, unique, artistic",
    "cartoon": "\"cartoon style\" illustration of {prompt}, bright colors, simple shapes, playful, highly detailed, animation style"
}
#negative_prompt = "(deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation, NSFW"
negative_prompts = {
    "general": "blurry, low quality, low detail,(deformed, distorted, disfigured:1.3),wrong anatomy,",
    "cinematic": "blurry, low resolution, amateur, poorly lit, cartoonish ,unprofessional, unrealistic,distorted, disfigured:1.3),wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4)",
    "anime": "bland, unexpressive, poorly drawn, low detail, unrealistic proportions, dull colors,distorted, disfigured:1.3),wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4)",
    "photographic": "grainy, out of focus, poorly composed, bad lighting, overexposed, unprofessional,distorted, disfigured:1.3),wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4)",
    "comic": "boring, poorly illustrated, low detail, dull colors, uninteresting composition,distorted, disfigured:1.3),wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4)",
    "realistic": "cartoonish, unrealistic, low detail, poorly textured, unconvincing,(deformed, distorted, disfigured:1.3),wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4)worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, NSFW",
    "3d": "flat, poorly rendered, low poly, unrealistic lighting, untextured, low quality,distorted, disfigured:1.3), floating limbs, (mutated hands and fingers:1.4)",
    "cyberpunk": "dull, low tech, uninteresting, outdated, bland, poorly detailed,(deformed, distorted, disfigured:1.3)",
    "abstract": "literal, boring, uninspired, plain, uncreative, predictable,(deformed, distorted, disfigured:1.3)",
    "cartoon": "dull, uninteresting, poorly animated, low quality, boring colors, lack of expression,distorted, disfigured:1.3),wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4)"
}
lightings = {
    "Natural sunlight": "Bright, (clear light from the sun), casting sharp shadows and highlighting natural colors and textures",
    "Soft light": "Gentle, diffused sunlight, creating a smooth and flattering light with minimal shadows, ideal for portraits and close-ups.",
    "Backlight": "Light from behind the subject, creating a silhouette effect or emphasizing the edges with a halo of light",
    "Candlelight": "Warm, flickering (light from candles), producing soft, romantic, and intimate scenes with deep shadows",
    "Moonlight": "Cool, \"serene ((moonlight)) with soft shadows\", creating a serene and mystical atmosphere with  muted colors,\"clear night sky\"",
    "Fluorescent": "Bright, artificial light, often with a cool or greenish tint, commonly found in offices or industrial settings",
    "Firelight": "Warm, dynamic light from a fire, casting dancing shadows and creating a cozy or dramatic effect",
    "Neon": "Bright, vibrant light from (neon signs), vivid, glowing neon lights,, creating a retro or futuristic ambiance",
    "Spotlight": "Focused, intense beam of light illuminating a specific area or subject",
    "Underwater": "Soft, diffused ((light filtering through water), with a (bluish-green tint)",
    "Dusk": "Soft, fading light just after (sunset), with a blend of warm and cool tones and gentle shadows",
    "Dawn": "Soft, emerging light just before (sunrise), with cool tones and a fresh, hopeful atmosphere",
    "Stormy": "Dark, ominous light with heavy clouds, often with dramatic contrasts and occasional lightning",
    "Twilight": "Soft, ((diffused light after sunset or before sunrise)), with a mix of blue and purple tones",
    "None": ""
}

color_palettes = {
    "Monochrome": "A single color in varying shades, often black and white",
    "Pastel": "Soft, light colors like baby blue, pink, and mint green",
    "Vibrant": "Bright, saturated colors that are eye-catching and energetic",
    "Earthy": "Natural colors like browns, greens, and ochres, evoking nature",
    "Cool tones": "Colors like blue, green, and purple, creating a calm and serene feel",
    "Warm tones": "Colors like (red, orange, and yellow), creating a cozy and energetic feel",
    "Neon": "Extremely bright and (glowing neon colors), highly saturated, often used for a modern or futuristic look",
    "Desaturated": "Muted colors with low saturation, creating a vintage or somber feel",
    "Autumnal": "Warm, earthy colors like orange, red, and brown, reminiscent of fall",
    "Spring": "Fresh, vibrant colors like pink, green, and yellow, evoking springtime",
    "Winter": "Cool, icy colors like blue, white, and silver, evoking winter",
    "Patriotic": "Colors representing national pride, often red, white, and blue",
    "Tropical": "Bright,lush colors associated with tropical environments, vibrant colors like turquoise, coral, and lime green, evoking a tropical paradise",
    "Metallic": "Shiny, reflective colors like gold, silver, and bronze",
    "None": ""
}

camera_angles = {
    "Birds eye view": "A high,((\"Capture from above1.9\")), overhead angle looking down on the scene, creating a sense of scale and perspective",
    "Worms eye view": "A (low angle looking up from the ground), making subjects appear larger and more imposing",
    "Dutch angle": "A (tilted angle) creating a sense of unease or dynamic movement, often used in dramatic or action scenes",
    "Close up": "A tight shot (focusing on a subject's ((face)) or a specific detail), highlighting emotions or intricate details",
    "Wide shot": "A ((broad view)) (capturing the entire scene), providing context and emphasizing the surroundings",
    "Over the shoulder": "(view from behind a (character's shoulder1.5)), focusing on what they see,creating a sense of perspective and immersion",
    "Point of view": " A shot that represents the perspective of a character, ((making the viewer feel like they are seeing through their eyes))",
    "Low angle": "(camera positioned low), looking up at the subject,making the subject appear powerful or dominant",
    "High angle": "(camera positioned high), looking down at the subject,making the subject appear smaller or weaker",
    "Tracking shot": "camera ((follows the subject)), maintaining a continuous view",
    "None": ""
}

character_expressions = {
    "Smile": "(character is \"smiling\"), conveying happiness or friendliness",
    "Frown": "(character is \"frowning\"), indicating displeasure or concentration",
    "Surprise": "(character has a \"surprised expression\"), eyes wide ,raised eyebrows, and mouth open,indicating shock or astonishment",
    "Anger": "(character looks \"angry\"), with furrowed brows and a tense expression,indicating (frustration or rage)",
    "Joy": "(character shows joy), with a \"broad smile and bright eyes\", indicating great happiness or delight",
    "Disgust": "(character displays disgust), with a wrinkled nose,pursed lips and a grimace",
    "Fear": "(character looks \"fearful\"), ((with wide eyes and a tense posture))",
    "Confusion": "(character has a \"confused look\"), with \"furrowed brows and a tilted head\",indicating puzzlement",
    "Excitement": "(character shows excitement), with wide eyes and an eager expression or enthusiasm",
    "Sadness": "(character \"looks sad\"), with downturned eyes and mouth",
    "Shock": "(character is \"shocked\"), with wide eyes and a gaping mouth,indicating intense surprise",
    "Contempt": "(character shows contempt), with a slight sneer and raised eyebrow",
    "Skepticism": "(character looks skeptical), with a raised eyebrow,curled lip and pursed lips",
    "Determination": "(character is determined), with a focused and resolute expression with a set jaw and intense eyes, indicating resolve",
    "Relief": "(character shows relief), with a relaxed expression and slight smile,indicating the release of tension",
    "Amusement": "(character is amused), with a light smile and twinkling eyes,indicating entertainment",
    "None": ""
}

character_styles = {
    "Japanese traditional": "Classic (Japanese clothing) and aesthetics, such as (kimonos, samurai armor), and traditional hairstyles",
    "Samurai": "Feudal (Japanese warrior attire), including armor, swords, and a stern, disciplined demeanor",
    "Manga": "Artistic style inspired by Japanese comics, with exaggerated features and expressive eyes",
    "Cyberpunk": "Futuristic, high-tech fashion with a gritty, urban aesthetic, often including neon elements",
    "Superhero": "Costumes inspired by (comic book heroes), often with capes, masks, and emblems",
    "High tech": "Sleek, modern fashion with advanced technology, often with a minimalist design",
    "Western": "Clothing inspired by the (American Old West), such as cowboy hats and boots",
    "Historical": "Fashion inspired by a specific historical period, such as Victorian or Medieval",
    "Futuristic": "Clothing and accessories with a sci-fi aesthetic, often with metallic or unconventional materials",
    "Cyborg": "A blend of human and machine, featuring mechanical enhancements and futuristic elements",
    "Space explorer": "Fashion inspired by astronauts or sci-fi space travelers, often including spacesuits",
    "None": ""
}

backgrounds = {
    "Forest": "a lush, green forest with tall trees and dappled sunlight",
    "Beach": "a serene beach with golden sand and gentle waves",
    "Mountains": "majestic mountains with snow-capped peaks and a clear blue sky",
    "City": "a bustling cityscape with towering skyscrapers and busy streets",
    "Desert": "a vast desert with rolling dunes and a scorching sun",
    "Space": "the vast expanse of space with distant stars and galaxies",
    "Underwater": "an underwater scene with colorful coral reefs and diverse marine life",
    "Countryside": "a peaceful countryside with rolling hills and quaint cottages",
    "Castle": "a grand castle with towering spires and a surrounding moat",
    "Jungle": "a dense jungle with thick foliage and exotic wildlife",
    "Night sky": "a clear night sky filled with twinkling stars and a bright moon",
    "Garden": "a beautiful garden with blooming flowers and manicured lawns",
    "None": ""
}




def generate_full_prompt(prompt, style, background, custom_background, lighting, color_palette, camera_angle, character_expression, character_style):
    style_prompt = styles_mapping.get(style, "{prompt}")
    full_prompt = style_prompt.format(prompt=prompt)
    
    if custom_background:
        full_prompt += f", {custom_background}"
    elif background and backgrounds.get(background):
        full_prompt += f", {backgrounds[background]}"
    
    if lighting and lightings.get(lighting):
        full_prompt += f", {lightings[lighting]}"
    if color_palette and color_palettes.get(color_palette):
        full_prompt += f", {color_palettes[color_palette]}"
    if camera_angle and camera_angles.get(camera_angle):
        full_prompt += f", {camera_angles[camera_angle]}"
    if character_expression and character_expressions.get(character_expression):
        full_prompt += f", {character_expressions[character_expression]}"
    if character_style and character_styles.get(character_style):
        full_prompt += f", {character_styles[character_style]}"
    
    return full_prompt
# def generate_full_prompt(prompt, style, background):
#     style_prompt = styles_mapping.get(style, "{prompt}")
#     full_prompt = style_prompt.format(prompt=prompt)
#     if background:
#         full_prompt += f", background:{background}"
#     return full_prompt

def generate_full_negative_prompt(negative_prompt, style):
    predefined_negative_prompt = negative_prompts.get(style, "")
    if negative_prompt:
        full_negative_prompt = f"{predefined_negative_prompt}, {negative_prompt}"
    else:
        full_negative_prompt = predefined_negative_prompt
    return full_negative_prompt

@router.post("/generate", response_model=GenerateResponse)
async def generate_image(request:GenerateRequest):
    #logger.info(f"Received generate request with prompt: {request.prompt}, style: {request.style}")
    try:
        
        #prompt
        full_prompt = generate_full_prompt(
            request.prompt, request.style.lower(), request.background, request.custom_background, 
            request.lighting, request.color_palette, request.camera_angle, 
            request.character_expression, request.character_style)
        # full_prompt = generate_full_prompt(request.prompt, request.style.lower(), request.background)
        logger.info(f"prompt: {full_prompt}")
        
        #negative prompt
        full_negative_prompt = generate_full_negative_prompt(request.negative_prompt, request.style.lower())
        logger.info(f"Negative prompt: {full_negative_prompt}")

        logger.info(f"image_size:{request.image_size}")
        # generate image
        output = client.run("stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc",
                           input={
                               "prompt":full_prompt,
                               "width" : int(request.image_size.split('x')[0]),
                               "height" :int(request.image_size.split('x')[1]),
                                "num_inference_steps": 25,
                                "output_quality": 90,
                                "cfg": 4.5,
                                "refine": "expert_ensemble_refiner",
                                "scheduler": "K_EULER",
                                "lora_scale": 0.6,
                                "negative_prompt": full_negative_prompt
                                }
                           )    
        image_url  = output[0]
        
        logger.info(f"Image generated, URL: {image_url}")

        # # downloading the image from url
        image = requests.get(image_url).content
    
        #save image locally
        request_id = str(uuid.uuid4())
        image_id = str(uuid.uuid4())
        local_img_path =os.path.join(img_dir, f"{image_id}.png")
        with open(local_img_path,'wb') as f: 
            f.write(image)
        logger.info(f"Image saved locally: {local_img_path}")

        #uploading the file s3
        s3_url = upload_to_s3(local_img_path,f"{image_id}.png")
        
        
        # store metadata in mongodb
        save_metadata(request_id,image_id,request.prompt,request.style,request.background,request.custom_background,request.negative_prompt,request.image_size,request.lighting,request.color_palette,request.camera_angle,request.character_expression,request.character_style,s3_url)

        #removing the local image file
        os.remove(local_img_path)
        logger.info(f"Image uploaded to S3: {s3_url}")

        return {"request_id":request_id,"image_id":image_id,"prompt":request.prompt,"style": request.style,"background": request.background,"custom_background": request.custom_background,"negative_prompt":request.negative_prompt,"image_size":request.image_size ,"lighting": request.lighting,
            "color_palette": request.color_palette,
            "camera_angle": request.camera_angle,
            "character_expression": request.character_expression,
            "character_style": request.character_style,"image_url":s3_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/regenerate", response_model=GenerateResponse)
async def regenerate_image(request:RegenerateRequest):
    logger.info(f"Received regenerate request for request ID: {request.request_id}")
    try:
        image_data = get_metadata(request.request_id)
        if not image_data:
            raise HTTPException(status_code=404,detail='image id not found')
        #Use new prompt if provide otherwise use existing prompt
        new_prompt = request.prompt if request.prompt is not None else image_data["generations"][-1]["prompt"]
        logger.info(f"prompt{new_prompt} fetched success")
    
        new_style = image_data["generations"][-1]["style"]
        logger.info(f"prompt{new_style} fetched success")
        new_background =  request.background if request.background is not None else image_data["generations"][-1].get("background","")
        logger.info(f"prompt{new_background} fetched success")
        custom_background = request.custom_background if request.custom_background is not None else image_data["generations"][-1].get("custom_background", "")
        user_negative = request.negative_prompt if request.negative_prompt is not None else image_data["generations"][-1].get("negative_prompt","")
        logger.info(f"prompt{user_negative} fetched success")
        Image_size = request.image_size if request.image_size is not None else image_data["generations"][-1].get("image_size", "1024x1024")
        logger.info(f"prompt{Image_size} fetched success")
        lighting = request.lighting if request.lighting is not None else image_data["generations"][-1].get("lighting", "")
        color_palette = request.color_palette if request.color_palette is not None else image_data["generations"][-1].get("color_palette", "")
        camera_angle = request.camera_angle if request.camera_angle is not None else image_data["generations"][-1].get("camera_angle", "")
        character_expression = request.character_expression if request.character_expression is not None else image_data["generations"][-1].get("character_expression", "")
        character_style = request.character_style if request.character_style is not None else image_data["generations"][-1].get("character_style", "")

        full_prompt = generate_full_prompt(new_prompt, new_style, new_background,custom_background,lighting,color_palette,camera_angle,character_expression,character_style)
        logger.info(f"full_prompt: {full_prompt}")
        full_negative_prompt = generate_full_negative_prompt(user_negative, new_style)
        logger.info(f"Negative prompt: {full_negative_prompt}")

    
    
        # Regenerate the image using the same prompt
        output = client.run("stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc",
                           input={
                               "prompt":full_prompt,
                                "width" : int(Image_size.split('x')[0]),
                                "height" :int(Image_size.split('x')[1]),
                                "num_inference_steps": 25,
                                "refine": "expert_ensemble_refiner",
                                "scheduler": "K_EULER",
                                "lora_scale": 0.6,
                                "negative_prompt": full_negative_prompt
                                }
                           )    
        new_image_url  = output[0]
        logger.info(f"Image regenerated, URL: {new_image_url}")

        
        # downloading the image from url
        image = requests.get(new_image_url).content
        new_image_id = str(uuid.uuid4())
        #save image locally
        local_img_path =os.path.join(img_dir, f"{new_image_id}.png")
        with open(local_img_path,'wb') as f:
            f.write(image)
        logger.info(f"Image saved locally: {local_img_path}")

        #uploading the file s3
        s3_url = upload_to_s3(local_img_path,f"{new_image_id}.png")

        #update meta data in mongodb
        update_metadata(request.request_id,new_image_id,new_prompt,new_style,new_background,custom_background,user_negative,Image_size,lighting,color_palette,camera_angle,character_expression,character_style,s3_url)

        #remove the locally created image file
        os.remove(local_img_path)
        logger.info(f"Image uploaded to S3: {s3_url}")

        return {"request_id": request.request_id,"image_id":new_image_id, "prompt": new_prompt, "style":new_style,"background":new_background,"custom_background": custom_background,"negative_prompt":user_negative,"image_size":Image_size,"lighting":lighting,"color_palette": color_palette,
            "camera_angle": camera_angle,
            "character_expression": character_expression,
            "character_style": character_style,"image_url": s3_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error in regeneration of image: {str(e)}")
    
@router.get("/image/{request_id}", response_model=GenerateResponse)
async def get_image(request_id: str):
    logger.info(f"Received delete request for image ID: {request_id}")
    image_data = get_metadata(request_id)
    if not image_data:
        raise HTTPException(status_code=404, detail="Request ID not found")

    return {"image_id":image_data["generations"][-1]["image_id"], "prompt": image_data["generations"][-1]["prompt"], "style": image_data["generations"][-1]["style"],"background":image_data["generations"][-1]["background"],"negative_prompt":image_data["generations"][-1]["negative_prompt"],"image_size":image_data["generations"][-1]["image_size"],"image_url": image_data["image_url"]}

@router.delete("/image/{request_id}/{image_id}")
async def delete_image(request_id: str,image_id:str):
    logger.info(f"Received delete request for image ID: {request_id}")
    try:
        image_data = get_metadata(request_id)
        if not image_data:
            raise HTTPException(status_code=404, detail="Request ID not found")
        
        document =next((gen for gen in image_data["generations"] if gen["image_id"]==image_id),None)
        if not document:
            raise HTTPException(status_code=404,detail="image_id not found in given req ID ")

        #s3_key = document["image_id"]

        #delete meta data from s3
        delete_from_s3(f"{image_id}.png")
        
        #Delete the image from mongo 
        delete_metadata(request_id,image_id)
        logger.info(f"Image and metadata deleted for image ID: {image_id}")

        return {"message": "Image and prompt deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @router.get("/", response_class=HTMLResponse)
# def read_root():
#     with open("frontend/index.html") as f:
#         return f.read()