import streamlit as st
from resizer import process_images
from pathlib import Path
import shutil

st.title("📸 Image Resizer & Optimizer")

input_folder = st.text_input("Input Folder Path")
output_folder = st.text_input("Output Folder Path")
width = st.number_input("Width", min_value=100, max_value=5000, value=1080)
quality = st.slider("Quality", 10, 100, 85)
watermark = st.text_input("Watermark", "Arya")

if st.button("Start"):
    if not Path(input_folder).exists():
        st.error("Invalid input folder!")
    else:
        process_images(
            Path(input_folder),
            Path(output_folder),
            width=width,
            height=None,
            quality=quality,
            format=None,
            watermark=watermark,
            workers=4,
            recursive=True
        )
        st.success("Done! Images processed.")
