import streamlit as st
import pandas as pd
import sqlalchemy
from PIL import Image
import psycopg2

conn = psycopg2.connect(
    database="CurtisDW",
    user='postgres',
    password='curtis1845',
    host='localhost',
    port= '5433'
)
conn.autocommit = True
cursor = conn.cursor()

def single_insert(conn, insert_req):
    """ Execute a single INSERT request """
    cursor = conn.cursor()
    try:
        cursor.execute(insert_req)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    cursor.close()

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
                            "DefectCode" : Defect_Code,
                            "DefectiveSamples" : Pieces_Defective,
                            "TotalSamples" : Total_Pieces_Sampled
                        }

submit = st.button("Submit", key=1)

submissiondict = {
            "JobID" : Job_Number,
            "ItemID" : Item_Number, 
            "CustomerID" : Customer,
            "DateFound": str(Inspection_Date),
            "InspectShift": Inspection_Shift, 
            "InspectGluer" : Inspection_Station, 
            "CaseQty" : Case_Count,
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
    st.write(df)





        # for i in df.index:
        #     query = """
        #     INSERT into Fact_Defect_Event(JobID, 
        #         ItemID, 
        #         CustomerID, 
        #         DateFound, 
        #         InspectShift, 
        #         InspectGluer, 
        #         DefectCode, 
        #         CaseQty, 
        #         DefectiveSamples,
        #         TotalSamples
        #         ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s, %s);
        #         """ % (df['JobID'], df['ItemID'], df['CustomerID'], df['DateFound'], df['InspectShift'], df['InspectGluer'], df['DefectCode'], df['CaseQty'], df['DefectiveSamples'], df['TotalSamples'])
        #     cursor.execute(query)

    
    # sql = f'''INSERT INTO Fact_Defect_Event(
    #     JobID, 
    #     ItemID, 
    #     CustomerID, 
    #     DateFound, 
    #     InspectShift, 
    #     InspectGluer, 
    #     DefectCode, 
    #     CaseQty, 
    #     DefectiveSamples, 
    #     TotalSamples) VALUES (df);'''
    # cursor.execute(sql)
    st.success("Your submission was recorded.")

