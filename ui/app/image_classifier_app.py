from typing import Optional

import requests
import streamlit as st
from app.settings import API_BASE_URL
from PIL import Image


def login(username: str, password: str) -> Optional[str]:
    """This function calls the login endpoint of the API to authenticate the user
    and get a token.

    Args:
        username (str): email of the user
        password (str): password of the user

    Returns:
        Optional[str]: token if login is successful, None otherwise
    """
    # Construct the API endpoint URL
    url = "{}/{}".format(API_BASE_URL, "login")

    # Set up the request headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Prepare the data payload
    data = {
        "username": username,  # Required
        "password": password,  # Required
        "grant_type": "",  # Optionals
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }

    # Send the API request
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")

    return None


def predict(token: str, uploaded_file: Image) -> requests.Response:
    """This function calls the predict endpoint of the API to classify the uploaded
    image.

    Args:
        token (str): token to authenticate the user
        uploaded_file (Image): image to classify

    Returns:
        requests.Response: response from the API
    """
    # Create a dictionary with the file data
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}

    # Add the token to the headers
    headers = {"Authorization": f"Bearer {token}"}

    # Make a POST request to the predict endpoint
    url = f"{API_BASE_URL}/model/predict"
    response = requests.post(url, files=files, headers=headers)

    return response


def send_feedback(
    token: str, feedback: str, score: float, prediction: str, image_file_name: str
) -> requests.Response:
    """This function calls the feedback endpoint of the API to send feedback about
    the classification.

    Args:
        token (str): token to authenticate the user
        feedback (str): string with feedback
        score (float): confidence score of the prediction
        prediction (str): predicted class
        image_file_name (str): name of the image file

    Returns:
        requests.Response: _description_
    """
    # Create a dictionary with the feedback data including feedback, score, predicted_class, and image_file_name
    data = {
        "feedback": feedback,
        "score": score,
        "predicted_class": prediction,
        "image_file_name": image_file_name,
    }

    # Add the token to the headers
    headers = {"Authorization": f"Bearer {token}"}

    # Make a POST request to the feedback endpoint
    url = f"{API_BASE_URL}/feedback"
    response = requests.post(url, json=data, headers=headers)

    return response


# User Interface
st.set_page_config(page_title="Image Classifier", page_icon="📷")
st.markdown(
    "<h1 style='text-align: center; color: #4B89DC;'>Image Classifier</h1>",
    unsafe_allow_html=True,
)

# Login Form
if "token" not in st.session_state:
    st.markdown("## Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        token = login(username, password)
        if token:
            st.session_state.token = token
            st.success("Login successful!")
            st.rerun()  # Refresh UI
        else:
            st.error("Login failed. Please check your credentials.")
else:
    st.success("You are logged in!")


if "token" in st.session_state:
    token = st.session_state.token

    # Load image
    uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

    print(type(uploaded_file))

    # Display scaled image if uploaded
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagen subida", width=300)

    if "classification_done" not in st.session_state:
        st.session_state.classification_done = False

    # Classification button
    if st.button("Classify"):
        if uploaded_file is not None:
            response = predict(token, uploaded_file)
            if response.status_code == 200:
                result = response.json()
                st.write(f"**Prediction:** {result['prediction']}")
                st.write(f"**Score:** {result['score']}")
                st.session_state.classification_done = True
                st.session_state.result = result
            else:
                st.error("Error classifying image. Please try again.")
        else:
            st.warning("Please upload an image before classifying.")

    # Display feedback field only if image has been classified
    if st.session_state.classification_done:
        st.markdown("## Feedback")
        feedback = st.text_area("If the prediction was wrong, please provide feedback.")
        if st.button("Send Feedback"):
            if feedback:
                token = st.session_state.token
                result = st.session_state.result
                score = result["score"]
                prediction = result["prediction"]
                image_file_name = result.get("image_file_name", "uploaded_image")
                response = send_feedback(
                    token, feedback, score, prediction, image_file_name
                )
                if response.status_code == 201:
                    st.success("Thanks for your feedback!")
                else:
                    st.error("Error sending feedback. Please try again.")
            else:
                st.warning("Please provide feedback before sending.")
                st.warning("Please provide feedback before sending.")

    # Footer
    st.markdown("<hr style='border:2px solid #4B89DC;'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #4B89DC;'>2024 Image Classifier App</p>",
        unsafe_allow_html=True,
    )
