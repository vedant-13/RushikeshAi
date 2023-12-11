import streamlit as st
import requests
import os
from io import BytesIO
import io
from PIL import Image

# Set page configuration
st.set_page_config(layout="centered", page_title="Rushikesh Ai", page_icon="icon.png", initial_sidebar_state="auto")

# Add CSS styles
with open('style.css', 'r') as html_file:
    st.markdown(f'<style>{html_file.read()}</style>', unsafe_allow_html=True)

# Define input components
access_token = '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'
if not access_token:
    st.error("Access token not found. Please set the ACCESS_TOKEN environment variable.")

name=st.title("Generate images by text")
prompt = st.text_area("Enter Text Prompt", placeholder="Type a prompt...")

# Add a toggle button for negative prompts
negative_prompt_toggle = st.toggle("Add Negative Prompt")   
negative_prompt = ""
if negative_prompt_toggle:
    negative_prompt = st.text_area("Enter Negative Prompt")

title=st.sidebar.write("Rushikesh Ai")

# Select image style
image_style = st.sidebar.selectbox("Image Style", ["Default", "Leonardo", "Abstract Expressionism", "Chiaroscuro", "Cubism", "Fauvism", "Impressionism", "Minimalism", "Pop Art", "Post-Impressionism", "Realism", "Sfumato", "Perspective"]) 

# Select aspect ratio
aspect_ratio = st.sidebar.selectbox("Select Aspect Ratio", ["Original", "Portrait (3:4)", "Landscape (4:3)", "Square (1:1)", "Widescreen (16:9)"])

# Set aspect ratio
if aspect_ratio == "Original":
    aspect_ratio_width = None
    aspect_ratio_height = None
elif aspect_ratio == "Landscape (4:3)":
    aspect_ratio_width = 4
    aspect_ratio_height = 3
elif aspect_ratio == "Portrait(3:4)":
    aspect_ratio_width = 3
    aspect_ratio_height = 4
elif aspect_ratio == "Square (1:1)":
    aspect_ratio_width = 1
    aspect_ratio_height = 1
elif aspect_ratio == "Widescreen (16:9)":
    aspect_ratio_width = 16
    aspect_ratio_height = 9

# Select number of images to generate
num_images = st.sidebar.slider("Number of Images to Generate", min_value=1, max_value=8, value=1)

# Input for image dimensions
width = st.sidebar.slider("Image Width", min_value=100, max_value=2000, value=512)
height = st.sidebar.slider("Image Height", min_value=100, max_value=2000, value=512)

# Select guidance scale
guidance_scale = st.sidebar.slider("Guidance Scale", min_value=1, max_value=20, value=7)

# Check if the user wants to generate content
if st.button("Generate Image"):
    # Define the HTML and CSS for the flashing gradient text
    html_code = """
    <div class="flashing-text">
        Generating image...
    </div>

    <style>
    @keyframes gradient {
        0% {color: red;}
        14% {color: orange;}
        28% {color: yellow;}
        42% {color: lime;}
        57% {color: cyan;}
        71% {color: blue;}
        85% {color: purple;}
        100% {color: red;}
    }

    .flashing-text {
        animation: gradient 1s linear infinite;
        font-size: 20px;
        font-weight: bold;
    }
    </style>
    """

    # Display the flashing gradient text
    message = st.empty()
    message.markdown(html_code, unsafe_allow_html=True)

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    API_URL = "https://api-inference.huggingface.co/models/playgroundai/playground-v2-1024px-aesthetic"

    payload = {
        "inputs": prompt,
        "guidance_scale": guidance_scale,
    }

    image_bytes = None

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
    except requests.exceptions.RequestException as err:
        st.error("An error occurred while generating the image. Please try again later.")
    else:
        if response.status_code == 200:
            image_bytes = response.content

    if image_bytes:
        image = Image.open(io.BytesIO(image_bytes))
        st.image(image, caption='Generated Image', use_column_width=True)
        
        # Convert PIL Image to byte array
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Create a download button for the image
        st.download_button(
            label="Download Image",
            data=img_byte_arr,
            file_name='generated_image.png',
            mime='image/png'
        )
        
        message.empty()  # Clear the "Generating image..." message
    else:
        st.error("Failed to generate image.")
