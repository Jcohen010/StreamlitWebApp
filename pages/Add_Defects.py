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

###### FUNCTIONS #######

# define database insert function
def insert_db(dataframe, engine, table):
    conn = engine.connect()
    try:
        dataframe.to_sql(table, conn, if_exists='append', index=False)
    except Exception:
        st.write("⚠️Error Encountered. Were any fields skipped?⚠️")
    else:
        st.success("Your submission was recorded.")
    finally:
        conn.close()

# define Defect List Generator function
def Defect_List_Generator(dataframe):
    Defectcode_desc = dataframe['Defect Code'] + '-' + dataframe['Defect Description']
    List = Defectcode_desc.to_list()
    return List

# define auto-sample qty based on caseqty
def Get_Sample_Qty(CaseQty):
    if CaseQty in range(2,15):
        return 2
    if CaseQty in range(15,25):
        return 3
    if CaseQty in range(25,90):
        return 5
    if CaseQty in range(90,150):
        return 8
    if CaseQty in range(150,280):
        return 13
    if CaseQty in range(280,500):
        return 20
    if CaseQty in range(500,1200):
        return 32
    if CaseQty in range(1200,3200):
        return 50
    if CaseQty in range(3200,10000):
        return 80
    if CaseQty in range(10000,35000):
        return 125
    if CaseQty in range(35000,150000):
        return 200
    if CaseQty in range(150000,500000):
        return 315
    else:
        return 0


# create arrays for multiple choice drop down inputs
Gluer_List = ['Gluer #2 Bobst', 'GLUER #4 Omega', 'GLUER #5 6FX', 'GLUER #6 6FX', 'GLUER #7 BOBST', 'GLUER #8 BOBST', 'GLUER #9 OMEGA', 'GLUER #10 OMEGA', 'GLUER#11 International']
Shift_List = ['1st Shift', '2nd Shift', 'Weekend Shift']
Customer_List = ['Titleist', 'Arden']

# Defects list
Defect_List = []

defects = pd.read_csv('Defects.csv')

Defect_List = Defect_List_Generator(defects)

######## FORM UI ##########

logo = Image.open("Small Curtis Logo.jpg")
st.set_page_config(page_title="Final Inspection Form", page_icon= logo, layout="centered")
st.image(logo, width=100, )
st.title("Final Inspection Form")
checkbox = st.checkbox("Español")

#Diverging UI upon spanish checkbox selection
if checkbox:
    st.subheader("Información de trabajo")
    st.markdown("---")
    JobID = st.text_input(label="Número de trabajo", max_chars=6)
    ItemID = st.text_input(label="Número de artículo", max_chars=4)
    CustomerID = st.selectbox(label="Cliente", options=Customer_List)
    CaseQty  = st.number_input(label="Cantidad de caso", step=1, )
    Case_Number = st.text_input(label="Número de caso")
    st.subheader("Información de inspección")
    st.markdown("---")
    InspectorID = st.number_input(label="Número de inspector", step=1, value=0)
    InspectStation = st.selectbox(label="Estación de inspección", options=Gluer_List)
    InspectShift  = st.selectbox(label="Turno de inspección", options=Shift_List)
    DateFound = st.date_input("Fecha de inspección")
    st.subheader("Casos defectuosos")
    st.markdown("---")





    # create blank dictionary for defective cases
    Defective_Case = {}

    # formatting defective cases input looped section
    if 'n_rows' not in st.session_state:
        st.session_state.n_rows = 1

    add = st.button(label="Añadir caso")

    if add:
        st.session_state.n_rows += 1
        st.experimental_rerun()

    for i in range(st.session_state.n_rows):
        #add text inputs here
        col1, col2, col3 = st.columns(3)

        with col1:
            Defect_Code = st.selectbox(label="Código de defectos", options=Defect_List, key=i)
            
        with col2:
            Pieces_Defective  = st.text_input(label="Cantidad de piezas defectuosas", key=i)

        with col3:
            Sample_Qty = Get_Sample_Qty(CaseQty)
            Total_Pieces_Sampled = st.number_input(label="Total de piezas muestreadas", value=Sample_Qty, key=i)

        Defective_Case[i] = {
                                "defectcode" : Defect_Code,
                                "defectivesamples" : Pieces_Defective,
                                "totalsamples" : Total_Pieces_Sampled
                            }

    submit = st.button("Enviar", key=1)
else:
    st.subheader("Job Information")
    st.markdown("---")
    JobID = st.text_input(label="Job Number", max_chars=6)
    ItemID = st.text_input(label="Item Number", max_chars=4)
    CustomerID = st.selectbox(label="Customer", options=Customer_List)
    CaseQty  = st.number_input(label="Case Qty", step=1, )
    Case_Number = st.text_input(label="Case Number")
    st.subheader("Inspection Information")
    st.markdown("---")
    InspectorID = st.number_input(label="Inspector Number", step=1, value=0)
    InspectStation = st.selectbox(label="Inspection Station", options=Gluer_List)
    InspectShift  = st.selectbox(label="Inspection Shift", options=Shift_List)
    DateFound = st.date_input("Inspection Date")
    st.subheader("Defective Cases")
    st.markdown("---")





    # create blank dictionary for defective cases
    Defective_Case = {}

    # formatting defective cases input looped section
    if 'n_rows' not in st.session_state:
        st.session_state.n_rows = 1

    add = st.button(label="Add Case")

    if add:
        st.session_state.n_rows += 1
        st.experimental_rerun()

    for i in range(st.session_state.n_rows):
        #add text inputs here
        col1, col2, col3 = st.columns(3)

        with col1:
            Defect_Code = st.selectbox(label="Defect Code", options=Defect_List, key=i)
            
        with col2:
            Pieces_Defective  = st.text_input(label="Quantity of Defective Pieces", key=i)

        with col3:
            Sample_Qty = Get_Sample_Qty(CaseQty)
            Total_Pieces_Sampled = st.number_input(label="Total Pieces Sampled", value=Sample_Qty, key=i)

        Defective_Case[i] = {
                                "defectcode" : Defect_Code,
                                "defectivesamples" : Pieces_Defective,
                                "totalsamples" : Total_Pieces_Sampled
                            }

    submit = st.button("Submit", key=1)

# structure input data into dictionary 
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

# Configure database insert upon submission
if submit:
    df = pd.DataFrame(submissiondict)
    df.insert(8,'defectcode', "")
    df.insert(9, 'defectivesamples', "")
    df.insert(10, 'totalsamples', "")
    
    for i, row in df.iterrows():
        df['defectcode'][i] = df.loc[i,'defective case'].get('defectcode')
        df['defectivesamples'][i] = df.loc[i,'defective case'].get('defectivesamples')
        df['totalsamples'][i] = df.loc[i,'defective case'].get('totalsamples')
    df = df.drop(df.columns[[7]], axis=1)
    df[['defectcode','defectdesc']]= df['defectcode'].str.split('-', expand=True)
    df.to_csv("Final_Inspection_Form_Output/TEST_"+f"{str(DateFound)}"+f"_{CustomerID}"+f"_{Case_Number}.csv", index=False, )  
    # st.write(df)
    insert_db(df, engine, "Stage_Defect_Event")