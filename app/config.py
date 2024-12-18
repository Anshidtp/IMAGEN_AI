import os
from dotenv import load_dotenv

load_dotenv()

#REPLICATE
API_KEY = os.getenv("API_TOKEN")

#MONGODB
MONGO_URI = os.environ["MONGODB_URL"]
# AWS S3 configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')