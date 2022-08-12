import streamlit as st

import pandas as pd

from PIL import Image

from sqlalchemy import create_engine

import toml

#fetch dbcredentials
credsfile = ".streamlit/secrets.toml"
content  = toml.load(credsfile)
conn_string = content['connection_string']
engine = create_engine(conn_string)

logo = Image.open("Small Curtis Logo.jpg")

st.set_page_config(page_title="Final Inspection Form", page_icon= logo, layout="centered")

st.image(logo, width=100, )
st.title("Final Inspection Data Collection")
checkbox = st.checkbox("Español")

if checkbox: 
    expander = st.expander("Ver todas las presentaciones")
    with expander:
        conn = engine.connect()
        df = pd.read_sql("Stage_Defect_Event", engine)
        st.write(df)
else:
    expander = st.expander("View all Submissions")
    with expander:
        conn = engine.connect()
        df = pd.read_sql("Stage_Defect_Event", engine)
        st.write(df)

