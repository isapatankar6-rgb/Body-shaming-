import streamlit as st
from PIL import Image
import requests
import io
import base64

st.set_page_config(page_title="AI Virtual Fitting Room", page_icon="👗", layout="wide")

st.title("👗 AI Virtual Fitting Room")
st.write("Upload a target person photo along with a garment image to generate an automated AI outfit try-on.")

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
    api_key = st.text_input("Segmind API Key (Optional for live generation)", type="password")
    run_button = st.button("Generate AI Try-On", type="primary", use_container_width=True)

if run_button:
    if not person_file or not garment_file:
        st.error("Please upload both a person image and a garment image before generating.")
    else:
        if not api_key:
            st.warning("⚠️ No API Key provided. To run real-time IDM-VTON AI diffusion models without free-tier queuing issues, get a free API key at segmind.com.")
            st.info("Showing preview setup with input images loaded successfully.")
        else:
            with st.spinner("Calling IDM-VTON AI serverless engine... warping garment & generating fit..."):
                try:
                    # Convert images to base64 or upload
                    person_b64 = base64.b64encode(person_file.getvalue()).decode('utf-8')
                    garment_b64 = base64.b64encode(garment_file.getvalue()).decode('utf-8')

                    url = "https://api.segmind.com/v1/idm-vton"
                    headers = {"x-api-key": api_key}
                    
                    payload = {
                        "category": category,
                        "human_img": f"data:image/jpeg;base64,{person_b64}",
                        "garm_img": f"data:image/jpeg;base64,{garment_b64}",
                        "crop": False,
                        "seed": 42,
                        "steps": 30
                    }

                    response = requests.post(url, json=payload, headers=headers)

                    if response.status_code == 200:
                        st.success("AI Virtual Try-On Rendered!")
                        st.image(response.content, caption="AI Rendered Result", use_container_width=True)
                    else:
                        st.error(f"API Error ({response.status_code}): {response.text}")

                except Exception as e:
                    st.error(f"Processing error: {str(e)}")
