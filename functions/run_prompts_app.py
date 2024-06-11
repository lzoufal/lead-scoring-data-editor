# run_prompts_app.py

import streamlit as st
import re 
import math
import json 

from sentence_transformers import SentenceTransformer, util
from functions.prompt_output import get_prompts, get_response
from functions.context_selector import set_template
from functions.prompt_templates import templates

def init_session_states():
        default_params = {
            "response_params_1": {},
            "response_params_2": {},
            "response_params_3": {},
            'response_content': None,
            'rating_content': None
        }

        for key, value in default_params.items():
            if key not in st.session_state:
                st.session_state[key] = value

def check_missing_cols(df, prompts_list):
    placeholder_columns = re.findall(r'\[\[(.*?)\]\]', ''.join(prompts_list.values()))
    missing_cols = [col for col in placeholder_columns if col not in df.columns]
    
    if missing_cols:
        st.warning(f"The following columns are missing from the table: {', '.join(missing_cols)}")

# Get similarity score
def compute_similarity_product(row, num_prompts, model):
    scores = []
    sentences = [f'prompt_{i + 1}' for i in range(num_prompts)]

    for i in range(len(sentences)):
        for j in range(i + 1, len(sentences)):
            if row[sentences[i]] == "" or row[sentences[j]] == "":
                scores.append(0)
                continue

            emb1 = model.encode(row[sentences[i]], convert_to_tensor=True)
            emb2 = model.encode(row[sentences[j]], convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(emb1, emb2)
            scores.append(similarity.item())
    
            #similarity_sum = sum(scores)
            #similarity_mean = similarity_sum / len(scores)
    
    similarity_product = math.prod(scores)        
    return math.pow(similarity_product, 1.0/len(scores))

def run_prompts_app(df):
    # Initialize session states
    init_session_states()
    
    # Run prompts UI
    st.markdown(f'<h3 style="border-bottom: 2px solid #338dff; ">{"Test"}</h3>', unsafe_allow_html=True)    
    st.text(" ")

    test_info = """
    🤹 This is your playground. Try up to 3 different prompts, or the same prompt with different settings, it\'s up to you! However, there are some important things to keep in mind:
    
    
    - Make sure the prompts contain relevant column names in double square brackets.

    """
    
    html_code = f"""
    <div style="background-color: rgba(244,249,254,255); olor:#283338; font-size: 16px; border-radius: 10px; padding: 15px 15px 1px 15px;">
        {test_info}
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)
    st.text(" ")

    st.selectbox(
            "Select prompt template:",
            templates["type"].unique(),
            index = None,
            key="_template",
            on_change=set_template
        )

    col1, _, _ =st.columns(3)
    num_prompts = col1.number_input("Select number of prompts:", min_value=1, value=1, max_value=3, )

    prompts_dict = get_prompts(num_prompts)
    check_missing_cols(df, prompts_dict)
    
    #col1, _, _ =st.columns(3)
    #rows_to_use = col1.number_input("Select how many rows of the table you want to use:", min_value=1, value=1, max_value=df.shape[0])
    df_subset = df.head(1)
    
    # Get responses
    if st.button('OKaaaAAAaaAYYYy LETS GO 🎢'):
        prompt_output = get_response(df_subset, prompts_dict)
        st.session_state["response_content"] = prompt_output
        
    # Show responses
    if st.session_state["response_content"] is not None:

        st.markdown(f'<h3 style="border-bottom: 2px solid #3ca0ff; ">{"Responses"}</h3>', unsafe_allow_html=True)
        st.text(" ")

        resp_info = "⬇️⬇️⬇️ Check out the responses and see which prompt fits your data best."
        st.markdown(f'<p style="background-color:rgba(244,249,254,255);color:#283338;font-size:16px;border-radius:10px;padding:15px;">{resp_info}</p>', unsafe_allow_html=True)

        st.text_area(label="Prompt result", value=st.session_state["response_content"]["prompt_1"].values[0],height=300)

    # Rate, download, reset
    #    st.markdown("What's next? 👀 Check the response similarity score to pinpoint areas where prompts might seem contradictory, it's a great way to refine your prompts and understand potential model challenges. Download the prompts with their settings, or start from scratch with a different table!")
        