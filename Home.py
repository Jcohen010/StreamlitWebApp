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

expander = st.expander("View Recent Submissions")
with expander:
    conn = engine.connect()
    df = pd.read_sql("stage_defect_event", engine)
    st.write(df)