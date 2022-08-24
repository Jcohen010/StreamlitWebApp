import streamlit as st

import pandas as pd

from PIL import Image

from sqlalchemy import create_engine

from pyzbar.pyzbar import decode

import toml
from tomlkit import value

#fetch dbcredentials
credsfile = ".streamlit/secrets.toml"
content  = toml.load(credsfile)
conn_string = content['connection_string']
engine = create_engine(conn_string)

###### FUNCTIONS #######

# define database insert function
def insert_db(dataframe, _engine, table):
    conn = engine.connect()
    try:
        dataframe.to_sql(table, conn, if_exists='append', index=False)
    except Exception:
        st.error("⚠️Error Encountered. Were any fields skipped?⚠️")
    else:
        st.success("Your submission was recorded.")
        st.warning("**DON'T PRESS SUBMIT AGAIN.  To enter another submission, refresh the page. ↻**")
    finally:
        conn.close()

# define Defect List Generator function
def Defect_List_Generator(dataframe):
    Defectcode_desc = dataframe['defectcode'] + '-' + dataframe['defectdesc']
    List = Defectcode_desc.to_list()
    return List

# define auto-sample qty based on caseqty
Sample_Qty_dic = {15:2,25:3,90:5,150:8,280:13,500:20,1200:32,3200:50,10000:80,35000:125,150000:200,500000:315}
def Get_Sample_Qty(CaseQty):
    for key in Sample_Qty_dic:
        if CaseQty < key:
            return Sample_Qty_dic.get(key)


def Accept_Reject(DefQty):
    if DefQty > 3 and Defect_Severity == "Major":
        return "Reject"
    else:
        return "Accept"

# create arrays for multiple choice drop down inputs
Gluer_List = ['Gluer #2 Bobst', 'GLUER #4 Omega', 'GLUER #5 6FX', 'GLUER #6 6FX', 'GLUER #7 BOBST', 'GLUER #8 BOBST', 'GLUER #9 OMEGA', 'GLUER #10 OMEGA', 'GLUER#11 International']
Shift_List = ['1st Shift', '2nd Shift', 'Weekend Shift']
Customer_List = ['Titleist', 'Arden']

# Defects list
Defect_List = []
defects = pd.read_sql('dim_defect', engine)
Defect_List = Defect_List_Generator(defects)

######## FORM UI ##########

#Title Area

logo = Image.open("Small Curtis Logo.jpg")
st.set_page_config(page_title="Final Inspection Form", page_icon= logo, layout="centered")
st.image(logo, width=100, )
st.title("Final Inspection Form")

# try to use button to hid camera_input 

st.subheader("Job Information")
st.markdown("---")


JobID = st.text_input(label="Job Number", max_chars=6)

ItemID = st.text_input(label="Item Number", max_chars=9, value="CPC")

CustomerID = st.selectbox(label="Customer", options=Customer_List)
CaseQty  = st.number_input(label="Case Qty", step=1)
NumberofCases = st.number_input("Number of Cases", step=1)

st.subheader("Inspection Information")
st.markdown("---")
InspectorID = st.number_input(label="Inspector Number", step=1, value=0)
InspectStation = st.selectbox(label="Inspection Station", options=Gluer_List)
InspectShift  = st.selectbox(label="Inspection Shift", options=Shift_List)
DateFound = st.date_input("Inspection Date")
st.subheader("Cases")
st.markdown("---")

# create blank dictionary for defective cases
Defective_Case = {}

# formatting defective cases input looped section
## Create session state variable for storing number of rows
if 'n_rows' not in st.session_state:
    st.session_state.n_rows = 1
if NumberofCases:
    st.session_state.n_rows = NumberofCases


if st.button(label="Add Cases", key="add"):
    st.session_state.n_rows += 1
    # st.experimental_rerun()

for i in range(st.session_state.n_rows):
    #add text inputs here
    col1, col2, col3, col4, col5, col6 = st.columns([1,1.5,.95,1,1,.65])

    with col1:
        Case_Number = st.text_input(label=f"Case Number", key=f"case_number{i}")

    with col2:
        Defect_Code = st.selectbox(label="Defect Code", options=Defect_List, key=f"defect_code{i}", help="Select a defect. If no samples are defective, select None")
    
    with col3:
        Defect_Severity = st.selectbox(label="Severity", options=["Minor", "Major"], key=f"defect_severity{i}")
    
    with col4:
        Pieces_Defective  = st.number_input(label="Qty Defective", step=1, key=f"pieces_defective{i}")

    with col5:
        Sample_Qty = Get_Sample_Qty(CaseQty)
        Total_Pieces_Sampled = st.number_input(label="Total Samples", value=Sample_Qty, key=f"SampleQty{i}")

    with col6:
        Accept_Reject_Value = Accept_Reject(Pieces_Defective)
        Case_Verdict = st.text_input(label="Accept/Reject",value=Accept_Reject_Value, key=f"case_verdict{i}")

    Defective_Case[i] = {
                            "caseid" : Case_Number,
                            "defectcode" : Defect_Code,
                            "defectivesamples" : Pieces_Defective,
                            "totalsamples" : Total_Pieces_Sampled,
                            "caseverdict" : Case_Verdict
                        }

st.markdown("**Don't press submit again after submission confirmation.  To enter another submission, refresh the page.*")
submit = st.button("Submit", key=1)
# st.write(st.session_state)
# structure input data into dictionary 
submissiondict = {
            "jobid" : JobID,
            "itemid" : ItemID, 
            "customerid" : CustomerID,
            "datefound": str(DateFound),
            "inspectshift": InspectShift, 
            "inspectgluer" : InspectStation, 
            "caseqty" : CaseQty,
            "defective case": Defective_Case
                }

columns = submissiondict.keys()

# Configure database insert upon submission
if submit:
    df = pd.DataFrame(submissiondict)
    df.insert(8, 'caseid', "")
    df.insert(9,'defectcode', "")
    df.insert(10, 'defectivesamples', "")
    df.insert(11, 'totalsamples', "")
    df.insert(12, 'caseverdict', "")

    for i, row in df.iterrows():
        df['caseid'][i] = df.loc[i,'defective case'].get('caseid')
        df['defectcode'][i] = df.loc[i,'defective case'].get('defectcode')
        df['defectivesamples'][i] = df.loc[i,'defective case'].get('defectivesamples')
        df['totalsamples'][i] = df.loc[i,'defective case'].get('totalsamples')
        df['caseverdict'][i] = df.loc[i,'defective case'].get('caseverdict')

    df = df.drop(df.columns[[7]], axis=1)
    # df['defectcode']= [x.split('-')[-1] for x in df['defectcode']]
    # df['defectdesc']= [x.split('-')[0] for x in df['defectcode']]
    df[['defectcode','defectdesc']]= df['defectcode'].str.split('-', n=2, expand=True)
    df.to_csv("Q:\Final Inspection Form Raw Exports/TEST_"+f"{str(DateFound)}"+f"_{CustomerID}"+f"_{Case_Number}.csv", index=False, )  
    # st.write(df)
    insert_db(df, engine, "stage_defect_event")
