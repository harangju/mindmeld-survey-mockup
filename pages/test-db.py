import streamlit as st

from lib.db import get_survey_participant_index, upload_data

st.write("# Display Ad Survey")

index = get_survey_participant_index('hi')

st.write(f"Participant index: {index}")
