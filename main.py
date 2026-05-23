import streamlit as st

pages = {
    "Home" : [
        st.Page("A. Home/01_about_me.py", title = "About Me"),          # Note : done (cek link aja)
        # st.Page("A. Home/02_contact.py", title = "Contact")
    ],
    "Project Showcase" : [
        st.Page("B. Project/prj_app_01.py", title = "Customer Geo Tagging"),    # loc branch, loc customer, customer info
        # st.Page("B. Project/prj_app_02.py", title = "Warehouse Monitoing"),     # DOI, ED, 
        # st.Page("B. Project", title = "Finance Dashboard"),       # Net sales, BS, PL
    ],
    "For Fun" : [
        # st.Page("C. For Fun/app.py", title = "How to optimize you chart"),
        st.Page("C. For Fun/ff_app_01.py", title = "Body Mass Index")
    ]
}

pg = st.navigation(pages)
pg.run()
