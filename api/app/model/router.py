import os

from app import settings as config
from app import utils
from app.auth.jwt import get_current_user
from app.model.schema import PredictResponse
from app.model.services import model_predict
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status  # File

router = APIRouter(tags=["Model"], prefix="/model")


@router.post("/predict")
async def predict(file: UploadFile, current_user=Depends(get_current_user)):
    rpse = {"success": False, "prediction": None, "score": None}

    # Check a file was sent and that file is an image
    if not file or not utils.allowed_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type is not supported.",
        )

    # Store the image to disk, calculate hash before to avoid re-writing an image already uploaded.
    new_filename = await utils.get_file_hash(file)
    file_path = os.path.join(config.UPLOAD_FOLDER, new_filename)

    if not os.path.exists(file_path):
        with open(file_path, "wb") as out_file:
            content = await file.read()
            out_file.write(content)

        # Reset file pointer to the beginning
        await file.seek(0)

    # Send the file to be processed by the model service
    prediction, score = await model_predict(file_path)

    # Update and return rpse dict with the corresponding values
    rpse["success"] = True
    rpse["prediction"] = prediction
    rpse["score"] = score
    rpse["image_file_name"] = new_filename

    return PredictResponse(**rpse)
