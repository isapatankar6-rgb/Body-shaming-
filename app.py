import streamlit as st
import requests
from PIL import Image
import io

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
    category = st.selectbox("Category", ["upperbody", "lowerbody", "dress"])
    
    run_button = st.button("Generate Preview", type="primary", use_container_width=True)

if run_button:
    if not person_file or not garment_file:
        st.error("Please upload both a person image and a garment image before generating.")
    else:
        with st.spinner("Processing pose estimation, garment warping, and diffusion blend..."):
            try:
                files = {
                    "person_image": ("person.jpg", person_file.getvalue(), "image/jpeg"),
                    "garment_image": ("garment.jpg", garment_file.getvalue(), "image/jpeg"),
                }
                data = {"category": category}

                # Send request to FastAPI backend
                response = requests.post("http://localhost:8000/api/v1/try-on", files=files, data=data)

                if response.status_code == 200:
                    result_img = Image.open(io.BytesIO(response.content))
                    st.success("Try-On Rendered Successfully!")
                    st.image(result_img, caption="Virtual Try-On Result", use_container_width=True)
                else:
                    st.error(f"Backend processing failed: {response.text}")
            except Exception as e:
                st.error(f"Could not connect to backend server: {str(e)}")
