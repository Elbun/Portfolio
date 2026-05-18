import streamlit as st
from lib_function import lets_connect

#----------------------------- Set page layout
st.set_page_config(layout="wide")

#----------------------------- Set image location
pic_path = "A. Home/"

#----------------------------- Segment 1 : Contact info
st.header("Let's Connect!")
st.html('''<p style="text-align:justify;">Searching for a solution for your business problem? Or just want to discuss something with me? Don't hesitate to reach out me!</p>''')
col1, col2, col3, col4 = st.columns(4)
with col1:
    # LinkedIn
    lets_connect(pic_path, "pic6_linkedin.png", "Elvin Buntoro", "https://www.linkedin.com/in/elvin-buntoro-39b83b1b2/")
    # Email
    lets_connect(pic_path, "pic9_gmail.webp", "elvinbuntoro@gmail.com", None)
    # Whatsapp
    lets_connect(pic_path, "pic14_wa.png", "+6281280142251", "https://wa.me/6281280142251/")
