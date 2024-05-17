
import streamlit as st
import schedule
import time
import pandas as pd

from Tables import  get_dataframe, write_to_keboola, fetch_all_ids, display_footer, display_logo, init
# Set Streamlit page config and custom CSS

init()
display_logo()
#st.session_state['selected-table'] = "in.c-lead-scoring-data-app.lead-scoring"
#st.session_state["data"] = get_dataframe("in.c-lead-scoring-data-app.lead-scoring")

st.title("Event scoring")  


if 'df_event_scoring' not in st.session_state:
    st.session_state['df_event_scoring'] = get_dataframe("in.c-lead-scoring-data-app.lead-scoring")

if "add_to_scoring" in st.session_state:
    if not st.session_state["add_to_scoring"].empty:
        if st.button("Add " + str(len(st.session_state["add_to_scoring"])) + " new event(s) " , key="add-new-events"):
            with st.spinner('Saving Data...'):
                st.session_state["df_event_scoring"] = pd.concat([st.session_state["df_event_scoring"],st.session_state["add_to_scoring"]],ignore_index=True, sort=False)
                


edited_data = st.data_editor(st.session_state["df_event_scoring"], num_rows="dynamic", height=500, use_container_width=True,disabled=("source", "channel","behaviour","event_type","event_subject"))

if st.button("Save Data", key="save-data-tables"):
    with st.spinner('Saving Data...'):
        write_to_keboola(edited_data, "in.c-lead-scoring-data-app.lead-scoring",f'updated_data.csv.gz', False)
    st.success('Data Updated!', icon = "🎉")
st.markdown("After clicking the 'Save Data' button, the data will be sent to Keboola Storage using a full load.")

display_footer()