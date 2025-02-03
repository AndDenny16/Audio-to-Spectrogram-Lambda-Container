import librosa 
from PIL import Image
import io
import librosa
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import base64
import os
import boto3
from dotenv import load_dotenv

os.environ["NUMBA_CACHE_DIR"] = "/tmp"  #Need this cache for Librosa to work effectively
load_dotenv()
BUCKET_NAME = os.getenv("BUCKET_NAME")

def save_to_s3(image):
    s3 = boto3.client('s3')
    image_buffer = io.BytesIO()
    image.save(image_buffer, format="PNG")
    image_buffer.seek(0) 
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key="spectrogram.png",
        Body=image_buffer,
        ContentType="image/png"  # Set the correct content type
    )

def create_image(audio_data, img_size):
    """
    Take in a audio file and create a Image of size (225, 225,3) for input into CNN
    Input: 
        audio_data: base64 encoded audio file
        img_size: (225, 225)

    Output:
        Image of size (225, 225,3)
    """

    audio_file = io.BytesIO(audio_data)
    audio, sr = librosa.load(audio_file, sr=16000)
    print("Librosa load complete")

    trimmed_audio, _ = librosa.effects.trim(audio, top_db=10)
    mel_spectrogram = librosa.feature.melspectrogram(y=trimmed_audio, sr=sr, n_fft=2048, hop_length=16, n_mels=64, fmin=50, fmax=350)
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
    print("Librosa Spectrogram Complete")

    fig = plt.figure(figsize=(2.5, 2.5)) 
    plt.axis('off')  
    librosa.display.specshow(mel_spectrogram_db, sr=sr, hop_length=16, x_axis=None, y_axis=None)
    plt.tight_layout(pad=0)
    fig.canvas.draw() 
    w, h = fig.canvas.get_width_height()
    img_array = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
    img_array = img_array.reshape((h,w,4)) 
    image = Image.fromarray(img_array).resize(img_size).convert('RGB')
    print("Image Spectrogram Complete")
    plt.close(fig)
    return image

def lambda_handler(event, context):
    try: 
        print("Process Beginning")
        audio = event.get("audio")
        if not audio:
            return {
                'statusCode': 400,
                'body': "Ensure to pass an Encoded Audio File inside request body,  /{/audio: <encoded_audio> /}/ }"
            }
        audio_data = base64.b64decode(audio)
        image = create_image(audio_data, (225, 225))
        save_to_s3(image)
        return {
             'statusCode': 200,
            'body': "Image Successfully Created"
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': "Audio to Image Failed"
        }