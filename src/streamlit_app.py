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
        padding-bottom: 1rem;
    }
</style>
""")

# 📌 INITIALIZE SESSION STATE
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
    tab_app, tab_about, tab_architecture = st.tabs(
        ["**App**", "**About**", "**Architecture**"]
    )

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
                type=["jpg", "jpeg", "png", "webp", "avif"],
                help="Maximum file size is 200MB",
                key="image_uploader",
            )

            st.html("<br>")
            st.subheader("Or Try an Example", divider=True)

            # Segmented control for selecting example images
            selected_example = st.segmented_control(
                label="Categories",
                options=["Animal", "Vehicle", "Object", "Building"],
                default=None,
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

        # --- LOGIC FOR IMAGE SELECTION & PREDICTION ---
        # Clear the previous prediction result if a new input is selected
        if uploaded_file or selected_example:
            st.session_state.prediction_result = None

        image_to_process = None

        if uploaded_file:
            image_to_process = Image.open(uploaded_file)

        elif selected_example:
            try:
                img_path = os.path.join(
                    APP_DIR, "assets", f"{selected_example.lower()}.jpg"
                )
                image_to_process = Image.open(img_path)
            except FileNotFoundError:
                st.error(
                    f"Error: The example image '{selected_example.lower()}.jpg' was not found."
                )
                st.stop()

        # 📌 PREDICTION RESULTS
        with col_results:
            st.header("Results", divider=True)

            # Display a "get started" message if no image is selected
            if not image_to_process and not st.session_state.prediction_result:
                st.info("Choose an image or an example to get a prediction.")

            # Display the image if one is selected
            if image_to_process:
                st.image(image_to_process, caption="Image to be classified")

            # If the button is clicked, run the prediction logic
            if classify_button and image_to_process:
                with st.spinner(text="🧠 Analyzing image..."):
                    try:
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

            # Display the prediction result if available in session state
            if st.session_state.prediction_result:
                st.metric(
                    label="Prediction",
                    value=st.session_state.prediction_result["label"],
                    delta=f"{st.session_state.prediction_result['score'] * 100:.2f}%",
                    help="The predicted category and its confidence score.",
                    delta_color="normal",
                )
                st.balloons()

            elif image_to_process:
                st.info("Click 'Classify Image' to see the prediction.")


# 📌 ABOUT TAB
with tab_about:
    st.header("About This Project")
    st.markdown("""
- This project is an **image classification app** powered by a Convolutional Neural Network (CNN).  
- Simply upload an image, and the app predicts its category from **over 1,000 classes** using a pre-trained **ResNet50** model.  
- Originally developed as a **multi-service ML system** (FastAPI + Redis + Streamlit), this version has been **adapted into a single Streamlit app** for lightweight, cost-effective deployment on Hugging Face Spaces.  

### Model & Description  
- **Model:** ResNet50 (pre-trained on the **ImageNet** dataset with 1,000+ categories).  
- **Pipeline:** Images are resized, normalized, and passed to the model.  
- **Output:** The app displays the **Top prediction** with confidence score.  

[ResNet50](https://www.tensorflow.org/api_docs/python/tf/keras/applications/ResNet50) is widely used in both research and production, making it an excellent showcase of deep learning capabilities and transferable ML skills.  
""")

with tab_architecture:
    with st.expander("🛠️ View Original System Architecture"):
        st.image(
            image="./src/assets/architecture.jpg",
            caption="Original Microservices Architecture",
        )

    st.markdown("""
### Original Architecture  
- **FastAPI** → REST API for image processing  
- **Redis** → Message broker for service communication  
- **Streamlit** → Interactive web UI  
- **TensorFlow** → Deep learning inference engine  
- **Locust** → Load testing & benchmarking  
- **Docker Compose** → Service orchestration  

### Simplified Version  
- **Streamlit only** → UI and model combined in a single app  
- **TensorFlow (ResNet50)** → Core prediction engine  
- **Docker** → Containerized for Hugging Face Spaces deployment  

This evolution demonstrates the ability to design a **scalable microservices system** and also **adapt it into a lightweight single-service solution** for cost-effective demos.  
""")


# 📌 FOOTER
st.divider()
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <b>Connect with me:</b> 💼 <a href="https://www.linkedin.com/in/alex-turpo/" target="_blank">LinkedIn</a> • 
        🐱 <a href="https://github.com/iBrokeTheCode" target="_blank">GitHub</a> • 
        🤗 <a href="https://huggingface.co/iBrokeTheCode" target="_blank">Hugging Face</a>
    </div>
    """,
    unsafe_allow_html=True,
)
