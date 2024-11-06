import streamlit_survey as ss

survey = ss.StreamlitSurvey()

survey.select_slider(
    "Likert scale:", options=["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"], id="Q2"
)