import streamlit as st
import pandas as pd
import openai
import base64
import os


from functions.show_data_info import show_data_info
from functions.improve_prompt import improve_prompt
from functions.run_prompts_app import run_prompts_app
from functions.context_selector import show_context
from functions.context_selector import filter_stories

from src.st_aggrid.st_aggrid import interactive_table

from Tables import display_logo,get_dataframe

image_path = os.path.dirname(os.path.abspath(__file__))

#st.set_page_config(page_title="Prompt playgorund"
#                   )
display_logo()
#logo_image = image_path+"/static/keboola.png"
#logo_html = f'<div style="display: flex; justify-content: flex-end;"><img src="data:image/png;base64,{base64.b64encode(open(logo_image, "rb").read()).decode()}" style="width: 150px; margin-left: -10px;"></div>'
#st.markdown(f"{logo_html}", unsafe_allow_html=True)

st.title('Prompt playground')


OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

openai.api_key = OPENAI_API_KEY

def get_uploaded_file():
    if 'df_user_stories' not in st.session_state:
        st.session_state['df_user_stories'] = get_dataframe("out.c-user_strories_pairing.USER_STORIES")
    return st.session_state['df_user_stories']

def display_main_content(openai_api_key):
    #if uploaded_file:
    df = get_uploaded_file()
    #show_data_info(df)
    show_context(df)

    if st.session_state['df_user_stories'] is not None:
        interactive_table()
    
    if len(openai_api_key) < 14:
        st.warning("To continue, please enter your OpenAI API Key.")
    
    #improve_prompt()
    if st.session_state.industry and st.session_state.keywords:
        selected_df = pd.DataFrame({
            "industry": [st.session_state.industry],
            #"keywords": [','.join(st.session_state.keywords) if isinstance(st.session_state.keywords, list) else st.session_state.keywords],
            "job_role": [st.session_state.target],
            "user_story":[filter_stories(df,st.session_state.industry,st.session_state.keywords)]
        })
    run_prompts_app(selected_df)

    st.text(" ")
    #st.markdown(f"{logo_html}", unsafe_allow_html=True)
    
def main():
    tab1, tab2 = st.tabs(["App", "Guide"])
    with tab1:
        display_main_content(OPENAI_API_KEY)
    
    with tab2:
        st.markdown("""
                    
        🔄 __Connect__ – Start by connecting to the Keboola storage, you'll need your API token to do this. Go to _Settings_ and find the _API Tokens_ tab. Once connected, you'll be able to select the bucket and table you want to work with. 
        
        📊 __Explore__ – Here you'll see the uploaded table to make sure you are working with the correct data.
                    
        🛠️ __Improve__ – If you have ideas but are unsure about the wording of your prompts, use this section. Simply enter your idea and hit the _Improve_ button. The app will return an improved version of your prompt that follows prompt engineering best practices.
                   
        🤹‍♂️ __Test__ – This is where you can experiment and fine-tune your prompts. You can input 1-3 prompts to run with your data. Each prompt comes with its own settings, allowing you to tweak parameters or compare results across different models. Additionally, you can specify the portion of your dataset you want to work with.
        
        💌 __Feedback__ – If you have any questions, encounter issues, or have suggestions for improving the PromptLab, don't hesitate to reach out! andrea.novakova@keboola.com
        
        🔗 __Useful Links__
        - Keboola's [API Tokens](https://help.keboola.com/management/project/tokens/)
        - Get your OpenAI API key [here](https://platform.openai.com/account/api-keys)
        - Read the prompt engineering [best practices](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api)
        - PromptLab [GitHub repo](https://github.com/keboola/kai-promptlab/tree/main)

                    """)
    
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if __name__ == "__main__":
    main()