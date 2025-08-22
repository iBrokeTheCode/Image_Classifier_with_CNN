import json
import os
import time

import numpy as np
import redis
import settings
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image

# Connect to Redis and assign to variable db
db = redis.Redis(
    host=settings.REDIS_IP, port=settings.REDIS_PORT, db=settings.REDIS_DB_ID
)

# Load ML model
model = ResNet50(include_top=True, weights="imagenet")


def predict(image_name):
    """
    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.

    Parameters
    ----------
    image_name : str
        Image filename.

    Returns
    -------
    class_name, pred_probability : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    class_name = None
    pred_probability = None

    # Get image path
    image_path = os.path.join(settings.UPLOAD_FOLDER, image_name)

    # Load image
    img = image.load_img(image_path, target_size=(224, 224))

    # Apply preprocessing (convert to numpy array, match model input dimensions (including batch) and use the resnet50 preprocessing)
    # Convert Pillow image to np.array
    x = image.img_to_array(img)

    # Add an extra dimension because the model is expecting as input a batch of images
    x_batch = np.expand_dims(x, axis=0)

    # Scaled pixels values
    x_batch = preprocess_input(x_batch)

    # Make predictions
    predictions = model.predict(x_batch)

    # Get predictions using model methods and decode predictions using resnet50 decode_predictions
    top_pred = decode_predictions(predictions, top=1)[0][0]  # imagenet_id, label, score
    _, class_name, pred_probability = top_pred

    # Convert probabilities to float and round it
    pred_probability = round(float(pred_probability), 4)

    return class_name, pred_probability


def classify_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.

    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.
    """
    while True:
        # Take a new job from Redis
        q = db.brpop(settings.REDIS_QUEUE)[1]

        # Decode the JSON data for the given job
        q = json.loads(q.decode("utf-8"))

        # Important! Get and keep the original job ID
        job_id = q["id"]

        # Run the loaded ml model (use the predict() function)
        prediction, score = predict(q["image_name"])  # 👈 Verify image name

        # Prepare a new JSON with the results
        output = {"prediction": prediction, "score": score}

        # Store the job results on Redis using the original
        # job ID as the key
        db.set(job_id, json.dumps(output))

        # Sleep for a bit
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()
