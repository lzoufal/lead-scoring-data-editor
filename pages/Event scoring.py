
import streamlit as st
import schedule
import time
import pandas as pd

from Tables import cast_bool_columns, get_dataframe, write_to_keboola, write_to_log, fetch_all_ids, display_footer, display_logo, init
# Set Streamlit page config and custom CSS

init()
display_logo()
st.session_state['selected-table'] = "in.c-lead-scoring-data-app.lead-scoring"
st.session_state["data"] = get_dataframe("in.c-lead-scoring-data-app.lead-scoring")

st.title("Event scoring")  

if "add_to_scoring" in st.session_state:
    if len(st.session_state["add_to_scoring"]) != 0:
        st.button("Add " + str(len(st.session_state["add_to_scoring"])) + " new event(s) " , key="add-new-events")
        with st.spinner('Saving Data...'):
            st.session_state["data"] = pd.concat([st.session_state["data"],st.session_state["add_to_scoring"]],ignore_index=True, sort=False)

edited_data = st.data_editor(st.session_state["data"], num_rows="dynamic", height=500, use_container_width=True,disabled=("source", "channel","behaviour","event_type","event_subject"))

if st.button("Save Data", key="save-data-tables"):
    with st.spinner('Saving Data...'):
        """kbc_data = cast_bool_columns(get_dataframe(st.session_state["selected-table"]))
        edited_data = cast_bool_columns(edited_data)
        st.session_state["data"] = edited_data
        concatenated_df = pd.concat([kbc_data, edited_data])
        sym_diff_df = concatenated_df.drop_duplicates(keep=False)
        write_to_log(sym_diff_df, st.session_state["selected-table"], True)
        """
        write_to_keboola(edited_data, st.session_state["selected-table"],f'updated_data.csv.gz', False)
    st.success('Data Updated!', icon = "🎉")
st.markdown("After clicking the 'Save Data' button, the data will be sent to Keboola Storage using a full load.")

display_footer()