import streamlit as st
import pandas as pd
import random
import csv
import os
import time
from kbcstorage.client import Client
from streamlit_option_menu import option_menu


st.set_page_config(

    layout="wide",

)


token = st.secrets["kbc_storage_token"]

client_upload = Client('https://connection.north-europe.azure.keboola.com', token)

@st.cache_data(ttl=7200,show_spinner=False)
def get_dataframe(table_name):
    client = Client('https://connection.north-europe.azure.keboola.com', token)
    client.tables.export_to_file(table_id=table_name, path_name='.')
    with open('./sf_contact', mode='rt', encoding='utf-8') as in_file:
        lazy_lines = (line.replace('\0', '') for line in in_file)
        reader = csv.reader(lazy_lines, lineterminator='\n')

    os.rename('sf_contact', 'data.csv')
    df = pd.read_csv('data.csv')
    return df


data = get_dataframe('in.c-sales-force.sf_contact')

#city_options = ['All'] + list(data['city'].unique())
title_options = ['All'] + list(data['Title'].unique())
department_options = ['All'] + list(data['Department'].unique())
segment_options = ['All'] + list(data['Segment__c'].unique())

def main():
    st.title("Audience builder")

    # Load dataset


    # Filter parameters
    # user_id_filter = st.text_input("Filter by user_id", value="user_id")
    title_filter = st.selectbox("Filter by title", title_options, index = 0)
    department_filter = st.selectbox("Filter by department", department_options, index=0)
    segment_filter =st.selectbox("Filter by segment", segment_options, index = 0)
    #city_filter = st.selectbox("Filter by city", city_options, index=0)

    # Filter data
    filtered_df = data
    
    #if user_id_filter != 'All':
    #    filtered_df = filtered_df[filtered_df['user_id'] == user_id_filter]
    if title_filter != 'All':
        filtered_df = filtered_df[filtered_df['Title'] == title_filter]
    if department_filter != 'All':
        filtered_df = filtered_df[filtered_df['Department'] == department_filter]
    if segment_filter != 'All':
        filtered_df = filtered_df[filtered_df['Segment__c'] == segment_filter]
    # if city_filter != 'All':
    #    filtered_df = filtered_df[filtered_df['city'] == city_filter]
    
    # Show filtered data
    st.write("Total filtered rows: ", filtered_df.shape[0])

    # Select Columns to download
    columns_to_download = st.multiselect("Select columns to download", filtered_df.columns)

    # Export to CSV
    if st.button("Export CSV"):
        file_name = st.text_input("Enter file name", "filtered_data")
        if file_name:
            file_path = f"{file_name}.csv.gz"
            filtered_df[columns_to_download].to_csv(file_path, index=False,compression='gzip')
            #st.write("Data exported as:")
            #st.markdown(f"[{file_name}.csv.gz]({file_path}?download=true)")
    if st.button("Sent to Keboola"):
        timestamp = int(time.time())
        file_name = 'data_' + str(timestamp) + 'Xtitle_' + str(title_filter) + 'Xdepartment_' + str(department_filter) + 'Xsegment_' + str(segment_filter)
        client_upload.tables.create(name=file_name, bucket_id='out.c-segments', file_path='./filtered_data.csv.gz')

    # Create a DataFrame with user counts grouped by age
    age_counts = filtered_df.groupby('Title')['Id'].count().reset_index()
    age_counts.columns = ['Title', 'user_count']
    st.dataframe(filtered_df.sample(10))

    # Create a bar chart using Streamlit
    st.bar_chart(age_counts.set_index('Title'))


if __name__ == '__main__':
    main()
