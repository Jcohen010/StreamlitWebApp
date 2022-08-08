import streamlit as st
import pandas as pd
from PIL import Image
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:curtis1845@localhost:5433/CurtisDW")

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
                            "defectcode" : Defect_Code,
                            "defectivesamples" : Pieces_Defective,
                            "totalsamples" : Total_Pieces_Sampled
                        }

submit = st.button("Submit", key=1)

submissiondict = {
            "jobID" : JobID,
            "itemID" : ItemID, 
            "customerID" : CustomerID,
            "datefound": str(DateFound),
            "inspectshift": InspectShift, 
            "inspectgluer" : InspectStation, 
            "caseqty" : CaseQty,
            "defective case": Defective_Case
                }

columns = submissiondict.keys()

def insert_db(dataframe, engine, table):
    conn = engine.connect()
    try:
        dataframe.to_sql(table, conn, if_exists='append', index=False)
    except Exception:
        st.write("error submitting")
    else:
        st.success("Your submission was recorded.")
    finally:
        conn.close()

if submit:
    df = pd.DataFrame(submissiondict)
    df.insert(8,'defectcode', "")
    df.insert(9, 'defectivesamples', "")
    df.insert(10, 'totalsamples', "")
    
    for i,row in df.iterrows():
        df['defectcode'][i] = df.loc[i,'defective case'].get('defectcode')
        df['defectivesamples'][i] = df.loc[i,'defective case'].get('defectivesamples')
        df['totalsamples'][i] = df.loc[i,'defective case'].get('totalsamples')
    df = df.drop(df.columns[[7]], axis=1)
    df.to_csv(f"{str(DateFound)}"+f"_{Case_Number}.csv", index=False, )    
    st.write(df)
    # Lets try inserting the dataframe using the df.to_sequel method 
    insert_db(df, engine, "Stage_Defect_Event")

    

