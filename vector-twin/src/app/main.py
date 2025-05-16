import os
import streamlit as st
from PIL import Image  # type: ignore

from vector_twin.qdrant import get_qdrant_client, get_top_k_similar_images
from vector_twin.models import initialize_models, process_single_image

LOGO = Image.open("assets/logo.png")

st.set_page_config(
    page_title="CelebTwin",
    page_icon=LOGO,
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

# Initialize session state variables
if 'matched_celebrity' not in st.session_state:
    st.session_state.matched_celebrity = None
    
if 'qdrant_client' not in st.session_state:
    st.session_state.qdrant_client = get_qdrant_client()
    
if 'models' not in st.session_state:
    st.session_state.models = initialize_models()

if not st.session_state.matched_celebrity:
    with st.sidebar:
        st.image(LOGO)
        st.markdown("<h1 style='text-align: center;'>Celebrity Twin</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-style: italic; color: #888;'>Because everyone deserves to know which famous person<br>they could've been if their parents had better connections 😉</p>", unsafe_allow_html=True)
        
    enable = st.checkbox("Enable Camera", help="Click to enable/disable camera")
    img_file_buffer = st.camera_input("Take a picture", disabled=not enable)

    if img_file_buffer is not None:
        img = Image.open(img_file_buffer)
        device, mtcnn, resnet = st.session_state.models
        img_embedding = process_single_image(img, device, mtcnn, resnet)
        
        similar_imgs = get_top_k_similar_images(
            st.session_state.qdrant_client,
            img_embedding,
            k=1
        )

        matches = [result.payload["label"] for result in similar_imgs]
        
        if matches:
            st.session_state.matched_celebrity = matches[0] 
            st.rerun()
        else:
            st.warning("No celebrity matches found!")
else:
    st.sidebar.empty()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"<h2 style='text-align: center;'>Your Celebrity Twin is ...</h2>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center; color: #FF69B4;'> {st.session_state.matched_celebrity} </h1>", unsafe_allow_html=True)
        
        # Add celebrity images
        celebrity_name = st.session_state.matched_celebrity.lower().replace(" ", "_")
        celebrity_dir = f"assets/celebrities/{celebrity_name}"
        
        if os.path.exists(celebrity_dir):
            image_files = [f for f in os.listdir(celebrity_dir) if f.endswith(('.jpg', '.jpeg', '.png'))][:4]
            
            if image_files:
                st.markdown("<h3 style='text-align: center;'>Celebrity Photos</h3>", unsafe_allow_html=True)
                cols = st.columns(2)
                
                for idx, image_file in enumerate(image_files):
                    col_idx = idx % 2
                    with cols[col_idx]:
                        img_path = os.path.join(celebrity_dir, image_file)
                        st.image(img_path, use_container_width=True)
        
        # Add a try again button
        if st.button("Try Again", use_container_width=True):
            st.session_state.matched_celebrity = None
            st.rerun()
    st.balloons()