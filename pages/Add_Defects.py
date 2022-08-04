import streamlit as st
import pandas as pd
from PIL import Image



logo = Image.open("Small Curtis Logo.jpg")
Gluer_List = []
Shift_List = []
Defective_Case = {}


# Creating Structure of Form
st.set_page_config(page_title="Final Inspection Form", page_icon= logo, layout="centered")
st.image(logo, width=100, )
st.title("Final Inspection Form")
st.checkbox("Spanish")
st.subheader("Job Information")
st.markdown("---")
JobID = st.text_input(label="Job Number", max_chars=6)
ItemID = st.text_input(label="Item Number")
CustomerID = st.text_input(label="Customer")
CaseQty  = st.number_input(label="Case Qty", step=1)
Case_Number = st.text_input(label="Case Number")
st.subheader("Inspection Information")
st.markdown("---")
InspectorID = st.text_input(label="Inspector Number")
InspectStation = st.text_input(label="Inspection Station")
InspectShift  = st.text_input(label="Inspection Shift")
DateFound = st.date_input("Inspection Date")
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
                            "DefectCode" : Defect_Code,
                            "DefectiveSamples" : Pieces_Defective,
                            "TotalSamples" : Total_Pieces_Sampled
                        }

submit = st.button("Submit", key=1)

submissiondict = {
            "JobID" : JobID,
            "ItemID" : ItemID, 
            "CustomerID" : CustomerID,
            "DateFound": str(DateFound),
            "InspectShift": InspectShift, 
            "InspectGluer" : InspectStation, 
            "CaseQty" : CaseQty,
            "Defective Case": Defective_Case
                }

columns = submissiondict.keys()
if submit:
    df = pd.DataFrame(submissiondict)
    df.insert(8,'DefectCode', "")
    df.insert(9, 'DefectiveSamples', "")
    df.insert(10, 'TotalSamples', "")
    
    for i,row in df.iterrows():
        df['DefectCode'][i] = df.loc[i,'Defective Case'].get('DefectCode')
        df['DefectiveSamples'][i] = df.loc[i,'Defective Case'].get('DefectiveSamples')
        df['TotalSamples'][i] = df.loc[i,'Defective Case'].get('TotalSamples')
    df = df.drop(df.columns[[7]], axis=1)
    df.to_csv(f"{str(DateFound)}"+f"_{Case_Number}.csv", index=False, )    
    st.write(df)

    st.success("Your submission was recorded.")

