import pandas as pd


templates = pd.DataFrame({
    "type" : ["E-mail", "LinkedInm"],
    "template": ["""Create e-mail communication to promote Keboola, 
                 that is targetting position:[[job_role]], 
                 who is working in industry:[[industry]], 
                 inspire communication by: [[user_story]]"""
        
                 ,"""Create LinkedIn post to promote Keboola, 
                 that is targetting position:[[job_role]], 
                 who is working in industry:[[industry]], 
                 inspire communication by: [[user_story]]"""]
})