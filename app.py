import streamlit as st
from PIL import Image
import replicate
import os

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
    api_token = st.text_input("Replicate API Token", type="password")
    run_button = st.button("Generate AI Try-On", type="primary", use_container_width=True)

if run_button:
    if not person_file or not garment_file:
        st.error("Please upload both a person image and a garment image before generating.")
    elif not api_token:
        st.error("Please paste your Replicate API Token above.")
    else:
        with st.spinner("Processing IDM-VTON model on Replicate GPU... Warping garment onto body..."):
            try:
                # Set environment variable for Replicate API authentication
                os.environ["REPLICATE_API_TOKEN"] = api_token

                # Call active cuuupid/idm-vton endpoint
                output = replicate.run(
                    "cuuupid/idm-vton:0513734a452173b8173e907e3a59d19a36266e55b48528559432bd21c7d7e985",
                    input={
                        "human_img": person_file,
                        "garm_img": garment_file,
                        "garment_des": f"Virtual try-on for {category}",
                        "category": category,
                        "crop": False,
                        "seed": 42,
                        "steps": 30
                    }
                )

                st.success("AI Virtual Try-On Rendered Successfully!")
                st.image(output, caption="AI Rendered Result", use_container_width=True)

            except Exception as e:
                st.error(f"Replicate API Error: {str(e)}")
