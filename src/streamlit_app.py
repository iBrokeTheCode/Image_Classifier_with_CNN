import os

import streamlit as st
from PIL import Image

from predictor import predict_image

APP_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(APP_DIR, "assets")

# 📌 PAGE SETUP
st.set_page_config(page_title="Image Classifier App", page_icon="🤖", layout="centered")
st.html("""
<style>
    .stMainBlockContainer {
        max-width: 70rem;
    }
</style>
""")

# 📌 INITIALIZE SESSION STATE
# We initialize session state variables to manage app state
if "uploaded_image" not in st.session_state:
    st.session_state["uploaded_image"] = None
if "example_selected" not in st.session_state:
    st.session_state["example_selected"] = False
if "prediction_result" not in st.session_state:
    st.session_state["prediction_result"] = None

# 📌 MAIN APP LAYOUT
with st.container():
    st.title(
        body="🖼️ Image Classifier with CNN",
        help="An interactive application to classify images into over 1000 categories.",
    )
    st.html("<br>")

    # Use tabs for different sections of the app
    tab_app, tab_description = st.tabs(["**App**", "**Description**"])

    # 📌 APP TAB
    with tab_app:
        # Create a two-column layout for the app interface
        col_upload, col_results = st.columns(2, gap="large")

        # 📌 IMAGE UPLOAD & EXAMPLE SELECTION
        with col_upload:
            st.header("Upload an Image", divider=True)

            # File uploader widget
            uploaded_file = st.file_uploader(
                label="Drag and drop an image here or click to browse",
                type=["jpg", "jpeg", "png"],
                help="Maximum file size is 200MB",
                key="image_uploader",
            )

            # Update state when a new file is uploaded
            if uploaded_file is not st.session_state.uploaded_image:
                st.session_state.uploaded_image = uploaded_file
                st.session_state.example_selected = False
                st.session_state.prediction_result = None

            st.html("<br>")
            st.subheader("Or Try an Example", divider=True)

            # Segmented control for selecting example images
            selected_example = st.segmented_control(
                label="Categories",
                options=["Animal", "Vehicle", "Object", "Building"],
                default="Animal",
                help="Select one of the pre-loaded examples",
            )

            st.html("<br>")

            # --- THE SINGLE CLASSIFY BUTTON ---
            classify_button = st.button(
                label="Classify Image",
                key="classify_btn",
                type="primary",
                icon="✨",
            )

        # 📌 PREDICTION RESULTS
        with col_results:
            st.header("Results", divider=True)

            image_to_process = None

            # Logic to handle which image to display
            if st.session_state.uploaded_image:
                # Get the image from the uploaded file
                image_to_process = Image.open(st.session_state.uploaded_image)
            elif selected_example:
                # Load the selected example image using a robust path
                try:
                    img_path = os.path.join(
                        ASSETS_DIR, f"{selected_example.lower()}.jpg"
                    )
                    image_to_process = Image.open(img_path)
                except FileNotFoundError:
                    st.error(
                        f"Error: The example image '{selected_example.lower()}.jpg' was not found."
                    )
                    st.stop()

            # Display image and run prediction when button is clicked
            if image_to_process:
                st.image(image_to_process, caption="Image to be classified")

                if classify_button:
                    # Run the prediction logic
                    with st.spinner("Analyzing image..."):
                        try:
                            # 📌 Prediction function call 📌
                            from predictor import predict_image

                            predicted_label, predicted_score = predict_image(
                                image_to_process
                            )
                            st.session_state.prediction_result = {
                                "label": predicted_label.replace("_", " ").title(),
                                "score": predicted_score,
                            }
                        except Exception as e:
                            st.error(f"An error occurred during prediction: {e}")

                # Display the prediction result if available
                if st.session_state.prediction_result:
                    st.metric(
                        label="Prediction",
                        value=st.session_state.prediction_result["label"],
                        delta=f"{st.session_state.prediction_result['score'] * 100:.2f}%",
                        help="The predicted category and its confidence score.",
                        delta_color="normal",
                    )
                    st.balloons()
                else:
                    st.info("Click 'Classify Image' to see the prediction.")
            else:
                st.info("Choose an image to get a prediction.")

# 📌 DESCRIPTION TAB
with tab_description:
    st.header("About This Project", divider=True)
    st.markdown(
        """
        This project showcases a Convolutional Neural Network (CNN) model that automatically
        classifies images into over 1000 different categories.

        ### Original Architecture
        The original project was built as a multi-service architecture, featuring:
        * **Streamlit:** For the web user interface.
        * **FastAPI:** As a RESTful API to handle image processing and model serving.
        * **Redis:** A message broker for communication between the services.

        ### Portfolio Adaptation
        For a live and cost-effective demo, this application has been adapted into a single-service
        solution. The core logic of the FastAPI backend has been integrated directly into
        the Streamlit app. This demonstrates the ability to adapt a solution for
        specific deployment and resource constraints.

        ### Technologies Used
        * **Streamlit:** For the interactive web interface.
        * **TensorFlow:** For loading and running the pre-trained CNN model.
        * **Pre-trained Model:** ResNet50 with weights trained on the ImageNet dataset.
        """
    )
