import numpy as np
from tensorflow.keras.applications.resnet50 import (
    ResNet50,
    decode_predictions,
    preprocess_input,
)
from tensorflow.keras.preprocessing import image

# Load the model outside the function to ensure it's loaded only once
model = ResNet50(include_top=True, weights="imagenet")


def predict_image(img):
    """
    Preprocesses an image and runs a pre-trained ResNet50 model to get a prediction.

    Parameters
    ----------
    img : PIL.Image
        The image object to classify.

    Returns
    -------
    class_name, pred_probability : tuple(str, float)
        The model's predicted class as a string and the corresponding confidence
        score as a number.
    """
    # Resize the image to match model input dimensions (224, 224)
    img = img.resize((224, 224))

    # Convert Pillow image to np.array
    x = image.img_to_array(img)

    # Add an extra dimension for the batch size
    x_batch = np.expand_dims(x, axis=0)

    # Apply ResNet50-specific preprocessing
    x_batch = preprocess_input(x_batch)

    # Make predictions
    predictions = model.predict(x_batch, verbose=0)

    # Get predictions using model methods and decode predictions
    top_pred = decode_predictions(predictions, top=1)[0][0]  # imagenet_id, label, score
    _, class_name, pred_probability = top_pred

    # Convert probability to float and round it
    pred_probability = round(float(pred_probability), 4)

    return class_name, pred_probability
