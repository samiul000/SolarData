# style

import streamlit as st
import base64

import os


# Set background from an image URL
def set_background_from_url(url):
    css = f"""
    <style>
    .stApp {{
        background-image: url("{url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# Set background from a local image file
def set_background_from_local(image_path):
    try:
        # Convert relative path to absolute path
        abs_path = os.path.join(os.path.dirname(__file__), image_path)

        with open(abs_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        css = f"""
                <style>
                .stApp {{
                    background-image: url("data:image/png;base64,{encoded}");
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
                </style>
                """
        st.markdown(css, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ Background image not found. Check your path.")


# Set a soft gradient background
def set_background_gradient():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #f0f4f7, #dbe9f4);
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# Set text styles
def set_text_style():
    st.markdown("""
        <style>
        /* Title (st.title) */
        .stApp h1 {
            color: #FF9900;
            text-align: center;
            font-weight: 900;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
        }

        /* All paragraph text (st.write, st.markdown) */
        .stApp p {
            color: #FFFFF0;
            font-size: 18px;
            font-weight: 500;
            text-align: center;
        }

        /* Subheaders (st.subheader, h3, etc.) */
        .stApp h3 {
            color: #000000;
            font-weight: bold;
        }

        /* Optional: Chart titles */
        .stPlotlyChart text {
            fill: #FFFFFF;
        }
        </style>
    """, unsafe_allow_html=True)


# Customize data container
def set_glassmorphism_style():
    st.markdown(
        """
        <style>
        /* Apply glass effect to the main content */
        .stApp {
            background: url("{url}") no-repeat center center fixed;
            background-size: cover;
        }

        /* Glass card effect on widget container */
        .block-container {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }

        /* Softer scrollbars */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
