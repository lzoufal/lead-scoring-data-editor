import streamlit as st
import pandas as pd
import schedule
import time

from Tables import get_dataframe, write_to_keboola, fetch_all_ids, display_footer, display_logo, init

# Set Streamlit page config and custom CSS
init()
display_logo()

# Create tabs
tab1, tab2 = st.tabs(["Event Scoring","Add Event"])
st.session_state["new_events_added"] = None
#

 #Second tab - Add Event
with tab2:
    st.title("Add event")
    st.subheader("Pick event types, which you wish to add into Event scoring table")

    if 'df_event_add' not in st.session_state:
        st.session_state['df_event_add'] = get_dataframe("in.c-lead-scoring-data-app.events_add")

    df = st.session_state["df_event_add"]

    if "Select" not in df.columns:
        df.insert(0, "Select", False)

    edited_data = st.data_editor(df, num_rows="dynamic", height=500, use_container_width=True,
                                 disabled=("source", "channel", "behaviour", "event_type", "event_subject"),
                                 column_config={"Select": st.column_config.CheckboxColumn(required=True)})

    if st.button("Add to event scoring table", key="add-to-event-table"):
        with st.spinner('Adding...'):
            selected_rows = edited_data[edited_data.Select]
            st.session_state["add_to_scoring"] = selected_rows.drop('Select', axis=1)
            st.session_state["new_events_added"] = True
        st.success('Data Added!', icon="🎉")
    
    st.markdown("After clicking the 'Add to event scoring table' button, the data will be available for adding into scoring table on the second sheet-")
    display_footer()

# Second tab - Event Scoring
with tab1:
    st.title("Event scoring")

    if 'df_event_scoring' not in st.session_state:
        st.session_state['df_event_scoring'] = get_dataframe("in.c-lead-scoring-data-app.lead-scoring")

    if st.session_state["new_events_added"]:
        if "add_to_scoring" in st.session_state:
            if not st.session_state["add_to_scoring"].empty:
                st.write("Add " + str(len(st.session_state["add_to_scoring"])) + " new event(s)!")
                with st.spinner('Saving Data...'):
                    
                    st.session_state["df_event_scoring"] = pd.concat([st.session_state["df_event_scoring"], st.session_state["add_to_scoring"]],
                                                                        ignore_index=True, sort=False)
                    st.session_state["add_to_scoring"] = pd.DataFrame()
                    st.session_state["new_events_added"] = False
                    

    edited_data = st.data_editor(st.session_state["df_event_scoring"], num_rows="dynamic", height=500, use_container_width=True,
                                 disabled=("source", "channel", "behaviour", "event_type", "event_subject"))

    if st.button("Save Data", key="save-data-tables"):
        with st.spinner('Saving Data...'):
            write_to_keboola(edited_data, "in.c-lead-scoring-data-app.lead-scoring", f'updated_data.csv.gz', False)
        st.success('Data Updated!', icon="🎉")

    st.markdown("After clicking the 'Save Data' button, the data will be sent to Keboola Storage using a full load.")
    display_footer()
