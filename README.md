# StreamlitWebApp
Web Application for Final Inspection Data Collection

![Header Image](https://www.sas.com/en_us/insights/big-data/what-is-big-data/_jcr_content/par/styledcontainer_335204280/image.img.jpg/1457718453446.jpg)

## The Problem
Throughout my time at my current company, I've invested a lot of energy into the transition away from paper forms as a method of internal data collection. The advantages of making the change to digital data capture are numerous:
* Improvement in data accuracy
* No lag time in potential analysis due to lack of need for manual entry
* Environmental friendliness
* Increased productivity due to no time wasted manually entering data
* Decrease in data redundancy
* Removes clutter typically accompanied by storing paper documents

*...and the list goes on*

One form in particular caught my eye as a perfect candidate for kicking off the transition away from paper data collection. It captures vital quality data which is utilized in giving stakeholders on the production team a clear idea of production performance, and also happens to steal much precious time from our quality engineer, who currently manually enters the collected data. 

## The Solution

### Plan A
I initially started searching for a third party form building application with a similar use case. One aspect of the candidate app was vital: the capability to loop a particular section/question an arbitrary amount of times, allowing inspectors to only have to enter header inpection information once, even if there ends up being several cases with defects. Furthermore, the JSON or .csv schema would have to match that of target table in the data warehouse.

*Example below:*

|jobID|itemID|customerID|datefound |inspectshift|inspectgluer|caseqty|defectcode|defsamples|totalsamples|
|-----|------|----------|----------|------------|------------|-------|----------|----------------|------------|
|4200 |7576|Test  |2022-08-10|1st Shift   |Machine 12    |1200   |F1        |12              |32          |
|4200 |7576|Test  |2022-08-10|1st Shift   |Machine 12    |1200   |F4        |1               |32          |
|4200 |7576|tes  |2022-08-10|1st Shift   |Machine 12    |1200   |L11       |2               |32          |


99% of the form building web apps I found were to basic to allow for the specific functionality that we required. Enter GoCanvas. They offered everything we needed: full customizability, pleasant GUI form builder, full integration capabilites, .pdf generation upon form submission; they even accomodated the looping section functionality we were seeking. Only issue: sky high pricing. My manager and I both knew upper management was unlikely to support the investment.

#### Plan B
I decided to build an app myself for the company. Using Streamlit, a web development environment based in python, I developed an app that could be run on the final inspectors' samsung tablets out on the production floor. Each submission routes captured data directly to the company's [data warehouse](https://github.com/Jcohen010/CompanyDW) staging area. 

## Resources

Tools
* Streamlit
* Visual Studio Code
* Postgresql
* Jupyter Notebooks

Languages
* Python
* SQL

## Features
There were a few key features that the Director of Quality and the inspection team were looking:
* Spanish/English Toggle
* Auto-Fill Sample Quantity depending on Case Quantity according to AQL sampling guidelines
* Local Hosting for increased security
* Ensured Accessability for all users


[App Preview](https://user-images.githubusercontent.com/104105293/184428035-28b63ce4-dc52-4d52-aee7-1a61603e2267.webm)


## Walking Through the Logic of the Code

This page walks through the code behind the Final Inspection App. 

We will take it block by block. Blocks will be separated into lines that are logically and functionally related.

Let’s get started!



### Prerequisites

* In order to be able to understand, troubleshoot, and improve the code behind this application a few prerequisites are necessary:

* Proficient in Python

* Experience with Pandas, SQLAlchemy

- Strong understanding of database design and management

* Experience using command line



### Importing our modules

1. Streamlit for building UI and app functionality

2. Pandas for structuring input values in tabular form and dataframe tranformations 

3. PIL for assigning page icon

4. sqlalchemy for connection and communication with postgresql data warehouse

5. toml for parsing .toml config file

```
import streamlit as st

import pandas as pd

from PIL import Image

from sqlalchemy import create_engine

import toml
```


### Fetching Database Credentials

Database URI is held within a toml file in the “Streamlit Final Inspection Form” Folder. Using the toml module, parse the connection string, saving it as the variable “conn_string”. Then pass it into the “create_engine” function from sqlalchemy to create an engine. This engine will be passed in when calling the insert_db() function defined in the next block.

```
credsfile = ".streamlit/secrets.toml"
content  = toml.load(credsfile)
conn_string = content['connection_string']
engine = create_engine(conn_string)
```


### Define Functions

1. insert_db() → Insert submission dataframe into Staging table of CurtisDW

2. Defect_List_Generator() → Using data from data source (.csv or sql table), prepare list of options for “Defect Code” drop down question. Specifically, the function concatenates Defect Code and Defect Desc (ex. P1 - Color Variation ) to improve the user experience for final inspectors (i.e.. not having to memorize the defect codes). 

3. Customer_List_Generator() → Takes dataframe object (from .csv or sql table), renders a customer list for the Customer drop down input.

4. Get_Sample_Qty() → Creates conditional autofill based on what is entered in Case Qty field. 

5. Major(), Minor(), Accept_Reject() → Minor and Major act as helper functions fort Accept_Reject(), which defines the threshold for case rejections based on qty rejected, caseqty, and defect severity.

```
def insert_db(dataframe, engine, table):
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
    Defectcode_desc = dataframe['defectcode'] + "-" + dataframe['defectdesc']
    List = Defectcode_desc.to_list()
    return List

def Customer_List_Generator(dataframe):
    Customer_Dataframe = dataframe.CustomerName + " - " + dataframe.CustomerID
    Customer_List = Customer_Dataframe.to_list()
    return Customer_List
  
# define auto-sample qty based on caseqty
Sample_Qty_dic = {15:2,25:3,90:5,150:8,280:13,500:20,1200:32,3200:50,10000:80,35000:125,150000:200,500000:315}
def Get_Sample_Qty(CaseQty):
    for key in Sample_Qty_dic:
        if CaseQty < key:
            return Sample_Qty_dic.get(key)

# define Accept/Reject function to control acceptance threshold. Dependent on defect severity and defect qty and Caseqty
Major_dict = {500:1, 1200:2, 3200:3, 10000:4, 35000:6}
Minor_dict = {90:1, 280:2, 500: 3, 1200: 4, 3200:6, 10000:8, 35000:11}
Accept ='<p style="font-family:sans-serif; color:Green; font-size: 42px;">Accept</p>'
Reject ='<p style="font-family:sans-serif; color:Red; font-size: 42px;">Reject</p>'
def Major(DefQty, CaseQty):
    for key in Major_dict:
        if CaseQty < key: 
            if DefQty < Major_dict.get(key):
                return "Accept"
            else:
                return "Reject"

def Minor(DefQty, CaseQty):
    for key in Minor_dict:
        if CaseQty < key: 
            if DefQty < Minor_dict.get(key):
                return "Accept"
            else:
                return "Reject"

@st.cache
def Accept_Reject(DefQty, CaseQty, Severity):
    if Severity == "Critical":
        if DefQty < 1:
            return "Accept"
        else: 
            return "Reject"
    elif Severity == "Major":
        return Major(DefQty, CaseQty)
    
    elif Severity == "Minor":
        return Minor(DefQty, CaseQty)
```



### Definition of Drop Down Field Options

Drop down inputs require field options to be either hard coded or called through use of a list object. In this block list objects are defined, either through hard coding or through the use of functions that return a list object. 

```
# create arrays for multiple choice drop down inputs
Gluer_List = ['Gluer #2 Bobst', 'GLUER #4 Omega', 'GLUER #5 6FX', 'GLUER #6 6FX', 'GLUER #7 BOBST', 'GLUER #8 BOBST', 'GLUER #9 OMEGA', 'GLUER #10 OMEGA', 'GLUER#11 International']
Shift_List = ['1st Shift', '2nd Shift', 'Weekend Shift']

# Customer List
Customer_List = []
Customers = pd.read_csv("C:\\Users\\jcohen\\OneDrive - Curtis Packaging Corporation\\Documents\\Justin\\DataTransformations\\CustomerList\\CustomersPreped.csv")
Customer_List = Customer_List_Generator(Customers)

# Defects list
Defect_List = []
defects = pd.read_sql('dim_defect', engine)
Defect_List = Defect_List_Generator(defects)
```


*Once dim_machine and dim_shift tables are created and populated, hard coding will not be required.*



## Building Form UI



### Header Area

Using the streamlit module, this block creates the elements of the App that make up the header.

```
logo = Image.open("Small Curtis Logo.jpg")
st.set_page_config(page_title="Final Inspection Form", page_icon= logo, layout="centered")
st.image(logo, width=100, )
st.title("Final Inspection Form")
st.subheader("Job Information")
st.markdown("---")
```


### Form Body

Static and stylistic components of the form are directly stated, while input components are defined as variables to facilitate data structuring and export. 

```
JobID = st.text_input(label="Job Number", max_chars=6)
ItemID = st.text_input(label="Item Number", max_chars=9, value="CPC")
CustomerID = st.selectbox(label="Customer", options=Customer_List)

if CustomerID == "Parlux Fragrances, Inc. - PARLUX":
    st.info("Customer Requires 25 Samples.")

CaseQty  = st.number_input(label="Case Qty", step=1)
st.subheader("Inspection Information")
st.markdown("---")
InspectorID = st.number_input(label="Inspector Number", step=1, value=0)
InspectStation = st.selectbox(label="Inspection Station", options=Gluer_List)
InspectShift  = st.selectbox(label="Inspection Shift", options=Shift_List)
DateFound = st.date_input("Inspection Date")
st.subheader("Cases")
st.markdown("---")
col1,col2,col3,col4,col5, col6 = st.columns(6)
with col1:
    NumberofCases = st.number_input("Number of Cases", step=1, value=1)
# create blank dictionary for defective cases
Defective_Case = {}

# formatting defective cases input looped section
## Create session state variable for storing number of rows
if 'n_rows' not in st.session_state:
    st.session_state.n_rows = 1
if NumberofCases:
    st.session_state.n_rows = NumberofCases

for i in range(st.session_state.n_rows):
    #add text inputs here
    col1, col2, col3, col4, col5, col6 = st.columns([1,1.5,.95,1,1,.65])

    with col1:
        Case_Number = st.text_input(label=f"Case Number", key=f"case_number{i}")

    with col2:
        Defect_Code = st.selectbox(label="Defect Code", options=Defect_List, key=f"defect_code{i}", help="Select a defect. If no samples are defective, select None")
    
    with col3:
        Defect_Severity = st.selectbox(label="Severity", options=["Minor", "Major", "Critical"], key=f"defect_severity{i}")
    
    with col4:
        Pieces_Defective  = st.number_input(label="Qty Defective", step=1, key=f"pieces_defective{i}")

    with col5:
        Sample_Qty = Get_Sample_Qty(CaseQty)
        Total_Pieces_Sampled = st.number_input(label="Total Samples", value=Sample_Qty, key=f"SampleQty{i}")

    with col6:
        Accept_Reject_Value = Accept_Reject(Pieces_Defective, CaseQty, Defect_Severity)
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

```

### Structuring input data

This block carries out preliminary structuring of the input values by creating a nested dictionary, utilizing the defined variables in the previous block.

```
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
```

### Data Transformation and Export

Upon the click of “Submit”, the nested dictionary created in the previous step is converted into a pandas dataframe. The following transformations take place next:

1. Before unfolding the nested dictionaries in the “defective case” column, four new empty columns are created to hold it’s values.

2. Iterating through the dataframe rows, each nested dictionary is unpacked and it’s values are fed into their respective empty columns.

3. The “defective case” column in postion [7] in the dataframe is deleted. 

4. The “defectcode” column is split on the “-” delimiter to produce two new columns: “defectcode” (this time with the defect code alone), and “defectdesc”.

The prepared dataframe looks something like this:

| | | | | | | | | | | | | |
|-|-|-|-|-|-|-|-|-|-|-|-|-|
|jobid|itemid|customerid|datefound|inspectshift|inspectgluer|caseqty|caseid|defectcode|defectivesamples|totalsamples|caseverdict|defectdesc|
|412620|CPC007909|Titleist|2022-08-24|1st Shift|Gluer #2 Bobst|1200|01865979|ES5|6|50|Reject|Hologram|
|412620|CPC007909|Titleist|2022-08-24|1st Shift|Gluer #2 Bobst|1200|01865957|None|0|50|Accept|None|
|412620|CPC007909|Titleist|2022-08-24|1st Shift|Gluer #2 Bobst|1200|01866038|P6|6|50|Reject|Reticulation|
|412620|CPC007909|Titleist|2022-08-24|1st Shift|Gluer #2 Bobst|1200|01865968|None|0|50|Accept|None|
|412620|CPC007909|Titleist|2022-08-24|1st Shift|Gluer #2 Bobst|1200|01865950|None|0|50|Accept|None|





Finally, the prepared dataframe is first exported to a local folder as a .csv, and then inserted into the “Stage_Defect_Event” table of the Postgresql data warehouse. 

```
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
    df[['customername', 'customerid']] = df['customerid'].str.split(' - ', n=2, expand=True)
    df.to_csv("Q:\Final Inspection Form Raw Exports/TEST_"+f"{str(DateFound)}"+f"_{CustomerID}"+f"_{JobID}.csv", index=False, )  
    df = df.drop(df.columns[[13]], axis=1)
    # st.write(df)
    insert_db(df, engine, "stage_defect_event")
```




There you have it! Hope that was helpful.



Full Python Script:

```
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



########## FUNCTIONS BEGIN ##########

# define database insert function
def insert_db(dataframe, engine, table):
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
    Defectcode_desc = dataframe['defectcode'] + "-" + dataframe['defectdesc']
    List = Defectcode_desc.to_list()
    return List

def Customer_List_Generator(dataframe):
    Customer_Dataframe = dataframe.CustomerName + " - " + dataframe.CustomerID
    Customer_List = Customer_Dataframe.to_list()
    return Customer_List
# define auto-sample qty based on caseqty
Sample_Qty_dic = {15:2,25:3,90:5,150:8,280:13,500:20,1200:32,3200:50,10000:80,35000:125,150000:200,500000:315}
def Get_Sample_Qty(CaseQty):
    for key in Sample_Qty_dic:
        if CaseQty < key:
            return Sample_Qty_dic.get(key)

# define Accept/Reject function to control acceptance threshold. Dependent on defect severity and defect qty and Caseqty
Major_dict = {500:1, 1200:2, 3200:3, 10000:4, 35000:6}
Minor_dict = {90:1, 280:2, 500: 3, 1200: 4, 3200:6, 10000:8, 35000:11}
Accept ='<p style="font-family:sans-serif; color:Green; font-size: 42px;">Accept</p>'
Reject ='<p style="font-family:sans-serif; color:Red; font-size: 42px;">Reject</p>'
def Major(DefQty, CaseQty):
    for key in Major_dict:
        if CaseQty < key: 
            if DefQty < Major_dict.get(key):
                return "Accept"
            else:
                return "Reject"

def Minor(DefQty, CaseQty):
    for key in Minor_dict:
        if CaseQty < key: 
            if DefQty < Minor_dict.get(key):
                return "Accept"
            else:
                return "Reject"

@st.cache
def Accept_Reject(DefQty, CaseQty, Severity):
    if Severity == "Critical":
        if DefQty < 1:
            return "Accept"
        else: 
            return "Reject"
    elif Severity == "Major":
        return Major(DefQty, CaseQty)
    
    elif Severity == "Minor":
        return Minor(DefQty, CaseQty)

########## FUNCTIONS END ##########



########## SUPPORTING LIST OBJECTS BEGIN ###########

# create arrays for multiple choice drop down inputs
Gluer_List = ['Gluer #2 Bobst', 'GLUER #4 Omega', 'GLUER #5 6FX', 'GLUER #6 6FX', 'GLUER #7 BOBST', 'GLUER #8 BOBST', 'GLUER #9 OMEGA', 'GLUER #10 OMEGA', 'GLUER#11 International']
Shift_List = ['1st Shift', '2nd Shift', 'Weekend Shift']

# Customer List
Customer_List = []
Customers = pd.read_csv("C:\\Users\\jcohen\\OneDrive - Curtis Packaging Corporation\\Documents\\Justin\\DataTransformations\\CustomerList\\CustomersPreped.csv")
Customer_List = Customer_List_Generator(Customers)

# Defects list
Defect_List = []
defects = pd.read_sql('dim_defect', engine)
Defect_List = Defect_List_Generator(defects)

########## LISTS END ##########



########## FORM UI BEGINS ###########

# Title Area
logo = Image.open("Small Curtis Logo.jpg")
st.set_page_config(page_title="Final Inspection Form", page_icon= logo, layout="centered")
st.image(logo, width=100, )
st.title("Final Inspection Form")
st.subheader("Job Information")
st.markdown("---")
JobID = st.text_input(label="Job Number", max_chars=6)
ItemID = st.text_input(label="Item Number", max_chars=9, value="CPC")
CustomerID = st.selectbox(label="Customer", options=Customer_List)

if CustomerID == "Parlux Fragrances, Inc. - PARLUX":
    st.info("Customer Requires 25 Samples.")

CaseQty  = st.number_input(label="Case Qty", step=1)
st.subheader("Inspection Information")
st.markdown("---")
InspectorID = st.number_input(label="Inspector Number", step=1, value=0)
InspectStation = st.selectbox(label="Inspection Station", options=Gluer_List)
InspectShift  = st.selectbox(label="Inspection Shift", options=Shift_List)
DateFound = st.date_input("Inspection Date")
st.subheader("Cases")
st.markdown("---")
col1,col2,col3,col4,col5, col6 = st.columns(6)
with col1:
    NumberofCases = st.number_input("Number of Cases", step=1, value=1)
# create blank dictionary for defective cases
Defective_Case = {}

# formatting defective cases input looped section
## Create session state variable for storing number of rows
if 'n_rows' not in st.session_state:
    st.session_state.n_rows = 1
if NumberofCases:
    st.session_state.n_rows = NumberofCases

for i in range(st.session_state.n_rows):
    #add text inputs here
    col1, col2, col3, col4, col5, col6 = st.columns([1,1.5,.95,1,1,.65])

    with col1:
        Case_Number = st.text_input(label=f"Case Number", key=f"case_number{i}")

    with col2:
        Defect_Code = st.selectbox(label="Defect Code", options=Defect_List, key=f"defect_code{i}", help="Select a defect. If no samples are defective, select None")
    
    with col3:
        Defect_Severity = st.selectbox(label="Severity", options=["Minor", "Major", "Critical"], key=f"defect_severity{i}")
    
    with col4:
        Pieces_Defective  = st.number_input(label="Qty Defective", step=1, key=f"pieces_defective{i}")

    with col5:
        Sample_Qty = Get_Sample_Qty(CaseQty)
        Total_Pieces_Sampled = st.number_input(label="Total Samples", value=Sample_Qty, key=f"SampleQty{i}")

    with col6:
        Accept_Reject_Value = Accept_Reject(Pieces_Defective, CaseQty, Defect_Severity)
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

########## FORM UI ENDS ##########



########## DATA STRUCTURING BEGINS ##########

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

########## DATA STRUCTURING ENDS ##########



########## DATA EXTRACTION BEGINS ##########

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
    df[['customername', 'customerid']] = df['customerid'].str.split(' - ', n=2, expand=True)
    df.to_csv("Q:\Final Inspection Form Raw Exports/TEST_"+f"{str(DateFound)}"+f"_{CustomerID}"+f"_{JobID}.csv", index=False, )  
    df = df.drop(df.columns[[13]], axis=1)
    # st.write(df)
    insert_db(df, engine, "stage_defect_event")

########## DATA EXTRACTION ENDS ##########
```
