import streamlit as st
import pandas as pd
from PIL import Image
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:curtis1845@localhost:5433/CurtisDW")


logo = Image.open("Small Curtis Logo.jpg")

st.set_page_config(page_title="Final Inspection Form", page_icon= logo, layout="centered")

st.image(logo, width=100, )
st.title("Final Inspection Data Collection")
st.checkbox("Spanish")

expander = st.expander("View all Submissions")
with expander:
    conn = engine.connect()
    df = pd.read_sql("Stage_Defect_Event", engine)
    st.write(df)
    

