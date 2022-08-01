import streamlit as st
import pandas as pd
import sqlalchemy
from PIL import Image

logo = Image.open("Small Curtis Logo.jpg")
Gluer_List = []
Shift_List = []
Defective_Case = {}

st.set_page_config(page_title="Final Inspection Form", page_icon= logo, layout="centered")



st.image(logo, width=100, )
st.title("Final Inspection Form")
st.checkbox("Spanish")
st.subheader("Job Information")
st.markdown("---")
Job_Number = st.text_input(label="Job Number")
Item_Number = st.text_input(label="Item Number")
Customer = st.text_input(label="Customer")
Case_Count  = st.number_input(label="Case Qty", step=1)
st.subheader("Inspection Information")
st.markdown("---")
Inspector_Number = st.text_input(label="Inspector Number")
Inspection_Station = st.text_input(label="Inspection Station")
Inspection_Shift  = st.text_input(label="Inspection Shift")
Inspection_Date = st.date_input("Inspection Date")
st.subheader("Defective Cases")
st.markdown("---")


if 'n_rows' not in st.session_state:
    st.session_state.n_rows = 1

add = st.button(label="add")

if add:
    st.session_state.n_rows += 1
    st.experimental_rerun()

for i in range(st.session_state.n_rows):
    #add text inputs here
    col1, col2, col3 = st.columns(3)

    with col1:
        Defect_Code = st.text_input(label="Defect Code", key=i)
        
    with col2:
        Pieces_Defective  = st.text_input(label="Quantity of Defective Pieces", key=i)

    with col3:
        Total_Pieces_Sampled = st.text_input(label="Total Pieces Sampled", key=i)

    Defective_Case[i] = {
                            "Defect Code" : Defect_Code,
                            "Pieces Defective" : Pieces_Defective,
                            "Total Pieces Sample" : Total_Pieces_Sampled
                        }

submit = st.button("Submit", key=467)

if submit:
    st.json({
                    "JobID" : Job_Number,
                    "ItemID" : Item_Number, 
                    "CustomerID" : Customer,
                    "Date": Inspection_Date,
                    "InspectShift": Inspection_Shift, 
                    "InspectGluer" : Inspection_Station, 
                    "TotalSamples" : Case_Count,
                    "Defective Case": Defective_Case
                        })



