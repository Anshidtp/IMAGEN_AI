# Model mappings based on styles
styles_mapping = {
    "general": "{prompt}, high quality, detailed, visually appealing",
    "cinematic": "cinematic film still of {prompt}, highly detailed, high budget hollywood movie, cinemascope, moody, epic, gorgeous, film grain",
    "anime": "anime artwork of {prompt}, anime style, key visual, vibrant, studio anime, highly detailed",
    "photographic": "cinematic photo of {prompt}, 35mm photograph, film, professional, 4k, highly detailed",
    "comic": "comic of {prompt}, graphic illustration, comic art, graphic novel art, vibrant, highly detailed",
    "realistic": "realistic rendering of {prompt}, photorealistic, highly detailed, professional photography, ultra-high resolution",
    "3d": "3D rendering of {prompt}, highly detailed, realistic textures, CGI, high definition, professional quality",
    "cyberpunk": "cyberpunk style depiction of {prompt}, futuristic, neon lights, dystopian, high-tech, dark atmosphere, highly detailed",
    "abstract": "abstract representation of {prompt}, surreal, imaginative, vibrant colors, highly detailed, unique, artistic",
    "cartoon": "cartoon style illustration of {prompt}, bright colors, simple shapes, playful, highly detailed, animation style"
}

negative_prompts = {
    "General": "blurry, low quality, low detail,(deformed, distorted, disfigured:1.3),wrong anatomy,",
    "cinematic": "blurry, low resolution, amateur, poorly lit, unprofessional, unrealistic,distorted, disfigured:1.3),wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4)",
    "anime": "bland, unexpressive, poorly drawn, low detail, unrealistic proportions, dull colors,distorted, disfigured:1.3),wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4)",
    "photographic": "grainy, out of focus, poorly composed, bad lighting, overexposed, unprofessional,distorted, disfigured:1.3),wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4)",
    "comic": "boring, poorly illustrated, low detail, dull colors, uninteresting composition,distorted, disfigured:1.3),wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4)",
    "realistic": "cartoonish, unrealistic, low detail, poorly textured, unconvincing,(deformed, distorted, disfigured:1.3),wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4)",
    "3d": "flat, poorly rendered, low poly, unrealistic lighting, untextured, low quality,distorted, disfigured:1.3), floating limbs, (mutated hands and fingers:1.4)",
    "cyberpunk": "dull, low tech, uninteresting, outdated, bland, poorly detailed,(deformed, distorted, disfigured:1.3)",
    "abstract": "literal, boring, uninspired, plain, uncreative, predictable,(deformed, distorted, disfigured:1.3)",
    "cartoon": "dull, uninteresting, poorly animated, low quality, boring colors, lack of expression,distorted, disfigured:1.3),wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4)"
}

background_mapping = { #goes with every style
    'forest': 'a lush, green forest with tall trees and dappled sunlight',
    'beach': 'a serene beach with golden sand and gentle waves',
    'mountains': 'majestic mountains with clear blue sky',
    'city': 'a bustling cityscape with towering skyscrapers and busy streets',
    'desert': 'a vast desert with rolling dunes and a scorching sun',
    'space': 'the vast expanse of space with distant stars and galaxies',
    'underwater': 'an underwater scene with colorful coral reefs and diverse marine life',
    'countryside': 'a peaceful countryside with rolling hills and quaint cottages',
    'castle': 'a grand castle with towering spires and a surrounding moat',
    'jungle': 'a dense jungle with thick foliage and exotic wildlife',
    'night_sky': 'a clear night sky filled with twinkling stars and a bright moon',
    'garden': 'a beautiful garden with blooming flowers and manicured lawns'
}
camera_angle_mapping = { #goes with every-style
    'birds_eye_view': "((Capture from above1.9)), providing a high perspective.",
    'worms_eye_view': "(Capture from below), giving a dramatic and towering perspective.",
    'dutch_angle': "Tilt the camera to create a sense of unease or dynamism.",
    'close_up': "Focus closely on the subject for detailed shots.",
    'wide_shot': "Capture a broad view, encompassing more background and context.",
    'over_the_shoulder': "Frame the shot from (behind a character’s shoulder), creating an immersive perspective.",
    'point_of_view': "Simulate the perspective of a character to put the viewer in their shoes.",
    'low_angle': "Shoot from a low position to make the subject appear powerful or imposing.",
    'high_angle': "Shoot from a high position to make the subject appear smaller or more vulnerable.",
    'tracking_shot': "Follow a moving subject to maintain focus and context."
}
character_style_mapping = { #goes with every-style
    'japanese_traditional': "Japanese traditional style with kimono and traditional accessories.",
    'samurai': "Samurai warrior attire with armor and katana sword.",
    'manga': "Manga/anime style with exaggerated features and vibrant colors.",
    'cyberpunk': "Cyberpunk style with futuristic clothing, cybernetic enhancements, and neon lights.",
    'superhero': "Superhero style with colorful costumes and superpowers.",
    'high_tech': "High-tech style with sleek, futuristic clothing and advanced gadgets.",
    'western': "Western style with cowboy hats, boots, and rugged clothing.",
    'historical': "Historical style based on a specific time period, such as medieval or Renaissance.",
    'futuristic': "Futuristic style with avant-garde fashion and cutting-edge technology.",
    'cyborg': "Cyborg style with a fusion of human and machine elements.",
    'space_explorer': "Space explorer style with astronaut suits and space gear."
}

character_style_mapping_anime = {
    'magical_girl': "Stylized, colorful outfits with magical themes and accessories, often including wands, ribbons, and elaborate dresses.",
    'shonen_hero': "Outfits typically seen on young male protagonists in shonen anime, including practical clothing with a touch of ruggedness.",
    'mecha_pilot': "Futuristic suits with mechanical or robotic elements, often including helmets and armor, designed for piloting giant robots.",
    'ninja': "Traditional ninja attire with modern, anime-inspired twists such as masks, headbands, and weapon pouches.",
    'idol': "Flashy, stage-worthy costumes seen on pop idols, complete with sequins, bows, and other eye-catching accessories.",
    'school_uniform': "Classic Japanese school uniforms, such as sailor suits for girls and gakuran for boys, often personalized with unique touches.",
    'yokai': "Traditional Japanese mythological creatures with a supernatural twist, including elaborate costumes and fantastical elements.",
    'samurai_armor': "Detailed samurai armor with a blend of traditional and futuristic elements, often including swords and other weapons.",
    'sports_gear': "Athletic wear specific to various sports, often with bold colors and team logos.",
    'fantasy_knight': "Armor and clothing inspired by medieval fantasy, often with ornate details and magical elements."
}


lighting_mapping = { #does not go with anime,comic,abstract and cartoon and maybe Cyberpunk
    'natural_sunlight': "Natural sunlight illuminating the scene with warm, soft light.",
    'soft_light': "Soft, diffused lighting creating gentle shadows and highlights.",
    'backlighting': "Backlighting emphasizing the silhouette of the subject against a bright background.",
    'candlelight': "Warm, flickering candlelight creating a cozy atmosphere.",
    'moonlight': "Gentle moonlight casting a soft glow over the scene.",
    'fluorescent': "Cool, fluorescent lighting providing bright, even illumination.",
    'firelight': "Warm, dynamic lighting from a crackling fire.",
    'neon': "Neon lighting with vibrant colors and a futuristic aesthetic.",
    'spotlight': "Focused spotlight drawing attention to a specific area or subject.",
    'underwater': "Underwater lighting with dappled sunlight filtering through the water.",
    'dusk': "Soft, fading light at dusk creating a serene atmosphere.",
    'dawn': "Soft, gentle light at dawn signaling the beginning of a new day.",
    'stormy': "Moody, atmospheric lighting during a storm with dramatic clouds and lightning.",
    'twilight': "Mysterious twilight lighting between day and night.",
}

poses_mapping_photographic = {
    'candid_laugh': "A natural, unposed shot capturing the subject mid-laughter.",
    'walking_toward_camera': "The subject walking confidently towards the camera, creating a dynamic and engaging composition.",
    'over_the_shoulder_look': "The subject looking over their shoulder back at the camera, adding a sense of intrigue or connection.",
    'sitting_relaxed': "The subject sitting in a relaxed position, often with one leg crossed over the other or leaning back comfortably.",
    'leaning_against_wall': "The subject casually leaning against a wall, conveying a sense of ease and confidence.",
    'arms_crossed': "The subject standing with arms crossed, often used to portray strength or self-assurance.",
    'looking_away': "The subject looking off into the distance, creating a thoughtful or contemplative mood.",
    'hands_in_pockets': "The subject with hands in their pockets, providing a laid-back and casual vibe.",
    'jumping_in_air': "A mid-air shot capturing the subject in a jump, adding a sense of fun and energy.",
    'profile_view': "A side profile shot of the subject, highlighting their features and silhouette."
}

atmosphere_mapping_cinematic = {
    'tense': "A suspenseful and tense atmosphere with dramatic lighting and intense background music.",
    'romantic': "A romantic atmosphere with soft lighting, warm tones, and gentle, melodic background music.",
    'epic': "An epic atmosphere with grand, sweeping views, dynamic camera angles, and powerful orchestral music.",
    'mysterious': "A mysterious atmosphere with shadowy lighting, fog, and an eerie, subtle soundtrack.",
    'action_packed': "An action-packed atmosphere with fast-paced camera movements, high-energy scenes, and intense music.",
    'somber': "A somber atmosphere with muted colors, slow pacing, and melancholic music.",
    'dreamlike': "A dreamlike atmosphere with soft focus, surreal visuals, and ethereal background music.",
    'gritty': "A gritty atmosphere with harsh lighting, urban settings, and a raw, unpolished aesthetic.",
    'nostalgic': "A nostalgic atmosphere with warm, faded colors, retro props, and evocative music from past eras.",
    'heroic': "A heroic atmosphere with bold lighting, triumphant music, and inspirational scenes."
}


expressions_mapping = { #goes with all the styles
    'smile': "A friendly smile, showing happiness or amusement.",
    'frown': "A frown, indicating sadness, displeasure, or concentration.",
    'surprise': "A look of surprise, with raised eyebrows and widened eyes.",
    'anger': "An expression of anger, with furrowed brows and a tense mouth.",
    'joy': "An expression of joy, with wide eyes and a big smile.",
    'disgust': "A look of disgust, with a wrinkled nose and narrowed eyes.",
    'fear': "An expression of fear, with wide eyes and a raised brow.",
    'confusion': "An expression of confusion, with a furrowed brow and quizzical look.",
    'excitement': "An expression of excitement, with wide eyes and an open mouth.",
    'sadness': "An expression of sadness, with downturned lips and drooping eyes.",
    'shock': "A shocked expression, with wide eyes and dropped jaw.",
    'contempt': "A contemptuous expression, with a sneer and narrowed eyes.",
    'skepticism': "A skeptical expression, with raised eyebrows and a questioning look.",
    'determination': "A determined expression, with a firm jaw and focused eyes.",
    'relief': "An expression of relief, with relaxed features and a sigh.",
    'amusement': "An amused expression, with a slight smile and twinkling eyes.",
}
color_palette_mapping = { #goes with all the styles
    'monochrome': "A monochrome color palette featuring shades of a single color.",
    'pastel': "A pastel color palette with soft, muted tones.",
    'vibrant': "A vibrant color palette with bold, saturated hues.",
    'earthy': "An earthy color palette featuring natural tones like browns, greens, and tans.",
    'cool_tones': "A color palette dominated by cool tones like blues and greens.",
    'warm_tones': "A color palette dominated by warm tones like reds, oranges, and yellows.",
    'neon': "A neon color palette with bright, fluorescent colors.",
    'desaturated': "A desaturated color palette with muted, faded colors.",
    'autumnal': "An autumnal color palette featuring warm, rich tones like oranges, browns, and yellows.",
    'spring': "A spring color palette with fresh, light tones like greens, pinks, and yellows.",
    'winter': "A winter color palette with cool, icy tones like blues, whites, and silvers.",
    'summer': "A summer color palette with bright, sunny tones like yellows, blues, and greens.",
    'tropical': "A tropical color palette with vibrant, exotic colors like turquoise, magenta, and coral.",
    'metallic': "A metallic color palette featuring shiny, reflective colors like gold, silver, and bronze.",
    'teal_and_orange': "A color grading style that emphasizes cool teal shadows and warm orange highlights.",
    'black_and_white': "A monochromatic color grading style, removing color to focus on contrast and texture.",
    'sepia': "A warm, brownish tone giving the image a nostalgic, old-fashioned look."
}





# def create_full_prompt(prompt: str, style: str, **kwargs) -> str:
#     style_prompt = styles_mapping.get(style.lower(), "{prompt}")

#     full_prompt = style_prompt.format(prompt=prompt)

#     if kwargs.get('background'):
#         full_prompt += f",{background_mapping.get(kwargs['background'], '')}"
#     if kwargs.get('camera_angle'):
#         full_prompt += f",{camera_angle_mapping.get(kwargs['camera_angle'], '')}"
#     if kwargs.get('lighting'):
#         full_prompt += f",{lighting_mapping.get(kwargs['lighting'], '')}"
#     if kwargs.get('color_palette'):
#         full_prompt += f",{color_palette_mapping.get(kwargs['color_palette'], '')}"
#     if kwargs.get('character_style'):
#         full_prompt += f",{character_style_mapping.get(kwargs['character_style'], '')}"
#     if kwargs.get('expressions'):
#        full_prompt += f",{expressions_mapping.get(kwargs['expressions'], '')}"
#     if kwargs.get('hair_style'):
#        full_prompt += f",{hair_style_mapping.get(kwargs['hair_style'], '')}"
#     if kwargs.get('eye_style'):
#        full_prompt += f",{eye_style_mapping.get(kwargs['eye_style'], '')}"  
#     if kwargs.get('character_anime'):
#        full_prompt += f",{character_style_mapping_anime.get(kwargs['character_anime'], '')}" 
#     if kwargs.get('poses'):
#        full_prompt += f",{poses_mapping_photographic.get(kwargs['poses'], '')}" 
#     if kwargs.get('atmosphere'):
#        full_prompt += f",{atmosphere_mapping_cinematic.get(kwargs['atmosphere'], '')}" 

#     return full_prompt

# def generate_full_negative_prompt(negative_prompt, style):
#     predefined_negative_prompt = negative_prompts.get(style, "")
#     if negative_prompt:
#         full_negative_prompt = f"{predefined_negative_prompt}, {negative_prompt}"
#     else:
#         full_negative_prompt = predefined_negative_prompt
#     return full_negative_prompt