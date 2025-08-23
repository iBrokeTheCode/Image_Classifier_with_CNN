import streamlit as st
from PIL import Image

from predictor import predict_image

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
if "selected_image" not in st.session_state:
    st.session_state["selected_image"] = None
if "prediction_placeholder" not in st.session_state:
    st.session_state["prediction_placeholder"] = {"label": "A Dog", "score": 0.9558}

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
            uploaded_image = st.file_uploader(
                label="Drag and drop an image here or click to browse",
                type=["jpg", "jpeg", "png"],
                help="Maximum file size is 200MB",
                key="image_uploader",
            )

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

            # This message is shown before any image is processed
            if st.session_state["selected_image"] is None and not classify_button:
                st.info("Choose an image to get a prediction.")

            # If the button is clicked, run the prediction logic
            if classify_button:
                # Check if an image is selected before running prediction
                if uploaded_image is not None:
                    # st.session_state["selected_image"] = uploaded_image
                    # Use Image.open() to convert the UploadedFile object into a PIL.Image object
                    st.session_state["selected_image"] = Image.open(uploaded_image)
                    st.session_state["uploaded_file"] = uploaded_image

                elif selected_example:
                    # Load the selected example image
                    try:
                        img_path = f"./assets/{selected_example.lower()}.jpg"
                        st.session_state["selected_image"] = Image.open(img_path)
                    except FileNotFoundError:
                        st.error(
                            f"Error: The example image '{selected_example.lower()}.jpg' was not found."
                        )
                        st.stop()

                if st.session_state["selected_image"] is not None:
                    st.image(
                        st.session_state["selected_image"],
                        caption="Image to be classified",
                    )

                    # Call the prediction function and display results
                    with st.spinner("Analyzing image..."):
                        # Call our modularized prediction function!
                        try:
                            predicted_label, predicted_score = predict_image(
                                st.session_state["selected_image"]
                            )

                            st.metric(
                                label="Prediction",
                                value=f"{predicted_label.replace('_', ' ').title()}",
                                delta=f"{predicted_score * 100:.2f}%",
                                help="The predicted category and its confidence score.",
                                delta_color="normal",
                            )
                            st.balloons()
                        except Exception as e:
                            st.error(f"An error occurred during prediction: {e}")
                else:
                    st.error("Please upload an image or select an example to classify.")


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
