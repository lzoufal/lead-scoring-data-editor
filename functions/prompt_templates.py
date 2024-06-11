import pandas as pd


templates = pd.DataFrame({
    "type" : ["E-mail", "LinkedIn"],
    "template": ["""create a personalized email communication to promote Keboola. The email should target individuals holding the position of [[job_role]] within the [[industry]] industry. The communication should be inspired by the following user story: [[user_story]].
                The email should include the following elements:
                Subject Line: An engaging and relevant subject line to capture the recipient's attention.
                Introduction: A brief introduction addressing the recipient and introducing Keboola.
                Value Proposition: A clear explanation of how Keboola can benefit their specific role and industry.
                User Story: An inspiring user story that highlights the success and benefits experienced by a similar professional or organization.
                Call to Action: A clear call to action inviting the recipient to learn more or schedule a meeting.
                Closing: A professional closing statement with contact information."""
        
                 ,"""Create LinkedIn post to promote Keboola, 
                 that is targetting position:[[job_role]], 
                 who is working in industry:[[industry]], 
                 inspire communication by: [[user_story]]"""]
})