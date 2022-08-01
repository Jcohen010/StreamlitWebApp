import streamlit as st

# if 'n_rows' not in st.session_state:
#     st.session_state.n_rows = 1

# add = st.button(label="add")

# if add:
#     st.session_state.n_rows += 1
#     st.experimental_rerun()

# inputs = {}
# for i in range(st.session_state.n_rows):
#     #add text inputs here
#     input = st.text_input(label="Column Name", key=i)
#     inputs[i] = {i:input}
    
# st.write(st.session_state.n_rows)

# st.write(inputs)
Defective_Case = {}
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
                            "Total Pieces Sampled" : Total_Pieces_Sampled
                        }
                    
                

st.write(Defective_Case)