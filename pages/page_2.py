import streamlit as st
import pandas as pd
import sqlalchemy
from PIL import Image


logo = Image.open("Small Curtis Logo.jpg")

st.set_page_config(page_title="Final Inspection Form", page_icon= logo, layout="centered")

st.image(logo, width=100, )
st.title("Final Inspection Form")
st.checkbox("Spanish")
st.subheader("Job Information")
st.markdown("---")
Job_Number = st.text_input(label="Job Number")
Item_Number = st.text_input(label="Item Number")
Customer = st.text_input(label="Customer")
Case_Count  = st.text_input(label="Case Qty")
st.subheader("Inspector Information")
st.markdown("---")