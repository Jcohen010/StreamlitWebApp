import streamlit as st
import pandas as pd
from PIL import Image


logo = Image.open("Small Curtis Logo.jpg")

st.set_page_config(page_title="Final Inspection Form", page_icon= logo, layout="centered")

st.image(logo, width=100, )
st.title("Final Inspection Data Collection")
st.checkbox("Spanish")

st.button("Add Defects")

st.expander("See all Submissions")


    


# st.text_input(label="Column Name", key=i) #Pass index as key