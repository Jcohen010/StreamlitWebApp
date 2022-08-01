import streamlit as st
import pandas as pd
import sqlalchemy
from PIL import Image


logo = Image.open("Small Curtis Logo.jpg")

st.set_page_config(page_title="Final Inspection Form", page_icon= logo, layout="centered")

st.image(logo, width=100, )
st.title("Final Inspection Data Collection")
st.checkbox("Spanish")
