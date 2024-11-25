# IMAGEN_AI
ImagenAI: Where Words Shape Worlds

This project is a Fast API application that interacts with the Replicate API to generate and manage Ai-generated images using the Stable Diffusion XL model. The application Provides endpoints to generate images based on prompt , retrieve generated images, regenerate images using the same Prompt, and delete images

## Requirements

- Python 3.8+
- FastAPI
- Replicate API library 
- MongoDB
- AWS S3

## Steps To Run

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```

2. **Create and activate a virtual environment:**

    ```bash
    conda activate -n <env_name> python=3.11 -y
    conda activate <env_name>
    ```
    Repalce the <env_name> with the name of your environment 

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory of the project and add your Replicate API token, AWS KEY ,MONGODB URL:

    ```env
    #REPLICATE
    REPLICATE_API_TOKEN=your_replicate_api_token

    #MONGODB
    MONGO_URI = os.environ["MONGODB_URL"]

    # AWS S3 configuration
    AWS_ACCESS_KEY_ID = 'YOUR AWS_ACCESS_KEY_ID'
    AWS_SECRET_ACCESS_KEY = 'YOUR AWS_SECRET_ACCESS_KEY'
    AWS_REGION = 'YOUR AWS_REGION'
    S3_BUCKET_NAME = 'YOUR S3_BUCKET_NAME'
    ```

5. **Running the Application:**

    Launch your terminal and execute the following command:

    ```bash
    python run.py
    ```

    The server will be accessible at `http://127.0.0.1:8000`.