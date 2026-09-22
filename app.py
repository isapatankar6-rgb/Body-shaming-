import streamlit as st
from PIL import Image
from gradio_client import Client, handle_file
import tempfile
import os

st.set_page_config(page_title="AI Virtual Fitting Room", page_icon="👗", layout="wide")

st.title("👗 AI Virtual Fitting Room")
st.write("Upload a target model/person photo along with a garment image to generate an automated outfit preview.")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.subheader("1. Person Photo")
    person_file = st.file_uploader("Upload person image", type=["jpg", "jpeg", "png"], key="person")
    if person_file:
        st.image(person_file, caption="Target Person", use_container_width=True)

with col2:
    st.subheader("2. Garment Photo")
    garment_file = st.file_uploader("Upload clothing item", type=["jpg", "jpeg", "png"], key="garment")
    if garment_file:
        st.image(garment_file, caption="Apparel Item", use_container_width=True)

with col3:
    st.subheader("3. Configuration")
    category = st.selectbox("Category", ["upper_body", "lower_body", "dresses"])
    run_button = st.button("Generate Preview", type="primary", use_container_width=True)

if run_button:
    if not person_file or not garment_file:
        st.error("Please upload both a person image and a garment image before generating.")
    else:
        with st.spinner("Processing pose estimation, garment warping, and diffusion blend..."):
            try:
                # Save uploaded files temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_person:
                    tmp_person.write(person_file.getvalue())
                    person_path = tmp_person.name

                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_garment:
                    tmp_garment.write(garment_file.getvalue())
                    garment_path = tmp_garment.name

                # Connect to open-source IDM-VTON inference space
                client = Client("yisol/IDM-VTON")
                
                result = client.predict(
                    dict={"background": handle_file(person_path), "layers": [], "composite": None},
                    garm_img=handle_file(garment_path),
                    garment_des="Virtual Try-On",
                    is_checked=True,
                    is_checked_crop=False,
                    denoise_steps=30,
                    seed=42,
                    api_name="/tryon"
                )

                # Clean up temporary files
                os.remove(person_path)
                os.remove(garment_path)

                # Render result
                st.success("Try-On Rendered Successfully!")
                st.image(result[0], caption="Virtual Try-On Result", use_container_width=True)

            except Exception as e:
                st.error(f"Inference processing error: {str(e)}")
