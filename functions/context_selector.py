import streamlit as st
import pandas as pd
from functions.prompt_templates import templates

def set_industry():
    # Callback function to save the role selection to Session State
    st.session_state.industry = st.session_state._industry
  

def set_keywords():
    # Callback function to save the role selection to Session State
    st.session_state.keywords = st.session_state._keywords
    

def set_target_role():
    # Callback function to save the role selection to Session State
    st.session_state.target = st.session_state._target

def set_template():
    st.session_state.template_text = templates.loc[templates['type'] == st.session_state._template, 'template'].values[0]

# Function to filter stories based on user input
def filter_stories(df, target_industry, keywords):

    # Filter by industry
    filtered_df = df[df['target_industry'] == target_industry]
    if filtered_df.empty:
        return
    # Function to calculate keyword match score
    def keyword_match_score(row_keywords, selected_keywords):
        return sum(kw.strip() in row_keywords for kw in selected_keywords)

    # Calculate match score for keywords
    filtered_df['match_score'] = filtered_df['keywords_clean'].apply(lambda k: keyword_match_score(k, keywords))

    # Sort by match score in descending order
    filtered_df = filtered_df.sort_values(by='match_score', ascending=False)
    return filtered_df.iloc[0]['content']


def split_data(df):
    
    # Create a list of unique values for 'target_industry' column
    unique_industries = df['target_industry'].unique().tolist()

    # Split the keywords in the 'keywords' column and create a list of unique keywords
    # First, split each keyword string into a list of keywords
    df['keywords'] = df['keywords_clean'].str.split(',')

    # Then, flatten the list of lists and create a unique set of keywords
    unique_keywords = set([keyword.strip() for sublist in df['keywords'].dropna() for keyword in sublist])
    unique_keywords = list(unique_keywords)
    return unique_industries, unique_keywords

def show_context(df):

    industry, keywords, target_role = st.columns(3)
    unique_industries, unique_keywords = split_data(df)
    with industry:
        st.selectbox(
            "Select target industry:",
            unique_industries,
            index = None,
            key="_industry",
            on_change=set_industry
        )
    with keywords:
        st.multiselect(
            "Select keywords",
            unique_keywords,
            default = None,
            key="_keywords",
            on_change=set_keywords
        )
    with target_role:
        st.text_input(
            "Select job title",
            value = None,
            key="_target",
            on_change=set_target_role
        )

    
