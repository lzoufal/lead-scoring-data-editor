
import streamlit as st
import schedule
import time
import pandas as pd

from Tables import cast_bool_columns, get_dataframe, write_to_keboola, write_to_log, fetch_all_ids, display_footer, display_logo, init
# Set Streamlit page config and custom CSS
st.set_page_config(layout="wide")
init()
display_logo()
st.session_state['selected-table'] = "in.c-lead-scoring-data-app.events_add"
st.session_state["data"] = get_dataframe("in.c-lead-scoring-data-app.events_add")

st.title("Add event")
st.subheader("Pick event types, which you wish to add into Event scoring table")  

df = st.session_state["data"]
df.insert(0, "Select", False)
edited_data = st.data_editor(df, num_rows="dynamic", height=500, use_container_width=True,disabled=("source", "channel","behaviour","event_type","event_subject"), column_config={"Select": st.column_config.CheckboxColumn(required=True)})

if st.button("Add to event scoring table", key="add-to-event-table"):
    with st.spinner('Adding...'):
        """kbc_data = cast_bool_columns(get_dataframe(st.session_state["selected-table"]))
        edited_data = cast_bool_columns(edited_data)
        st.session_state["data"] = edited_data
        concatenated_df = pd.concat([kbc_data, edited_data])
        sym_diff_df = concatenated_df.drop_duplicates(keep=False)
        write_to_log(sym_diff_df, st.session_state["selected-table"], True)
        """
        #write_to_keboola(edited_data, st.session_state["selected-table"],f'updated_data.csv.gz', False)
        selected_rows = edited_data[edited_data.Select]
        #st.text(selected_rows)
        st.session_state["add_to_scoring"] = selected_rows.drop('Select', axis=1)
    st.success('Data Added!', icon = "🎉")
st.markdown("After clicking the 'Save Data' button, the data will be sent to Keboola Storage using a full load.")

display_footer()