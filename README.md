# 🎵 Audio to Spectrogram Image Converter (AWS Lambda)

This project processes audio files into spectrogram images and uploads them to AWS S3. It is designed to be deployed as an AWS Lambda function using a Docker container.

## Functionality

- Converts base64-encoded audio files into mel spectrogram images.
  
      - (225, 225) size
  
      - Sample Rate:16000
  
      - Audio Trimmed: top_db: 10
  
      - n_fft=2048, hop_length=16, n_mels=64, fmin=50, fmax=350
  
- Uses **Librosa** for audio processing.
- Saves spectrogram images to AWS S3.
- Designed for deployment as an AWS Lambda function.
- Packaged using a **Docker container**.


---

## Prerequisites

1. **AWS CLI** configured with appropriate credentials (if running locally)
2. **Docker** installed and running.
3. **An S3 bucket** created in AWS.
4. **A .env file** with the following content:

   ```plaintext
   BUCKET_NAME=<your-s3-bucket-name>


## Project Structure
- **DockerFile**
- **app.py**
- **requirements.txt**
- **.env file** 
---

## Requirements.txt

- **Librosa** - Audio processing, Spectrogram Generation
- **Matplotlib** - Spectrogram visualization
- **Pillow (PIL)** - Image manipulation
- **NumPy** - Numerical operations
- **Boto3** - AWS SDK for Python
---

## Testing Locally
1. Clone the Repo
2. ``docker build -t <desired_name> . ``
3. ``docker run -p 9000:8080 <desired_name>``
4. Example Python request
   ```
   with open("<mp3 or wav file>", 'rb') as file:
        encoded_audio = base64.b64encode(file.read()).decode('utf-8')
    payload = {
            "audio": encoded_audio,
    }

    response = requests.post(
    'http://localhost:9000/2015-03-31/functions/function/invocations',    
        json=payload)

    print(response.text)
   ```

---

## Uploading to AWS Lambda

**Upload 2 Options**
  - Use AWS CLI to create Lambda Container straight from Docker Image 
  - I opted to first push Container to ECR, then create through the console
    
    ```
    aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<your-region>.amazonaws.com

    aws ecr create-repository --repository-name <desired_name>

    docker tag audio-to-spectrogram:latest <aws_account_id>.dkr.ecr.<your-region>.amazonaws.com/<desired_name>:latest

    docker push <aws_account_id>.dkr.ecr.<your-region>.amazonaws.com/<desired_name>:latest

    ```
**IAM Role** Ensure to create an IAM Role for this container that allows write access to your S3 Bucket

**API Gateway** Integrate the Lambda to an API Gateway



  

