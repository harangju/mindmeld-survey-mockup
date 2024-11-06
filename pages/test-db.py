import streamlit as st

from sqlalchemy import create_engine, text
from lib.db import get_survey_participant_index

# index = get_survey_participant_index('hi')
# st.write(f"Participant index: {index}")

conn = st.connection("postgresql", type="sql")
df = conn.query('SELECT * FROM "SurveyMockup";')
st.markdown("## SurveyMockup")
st.write(df)

df = conn.query('SELECT * FROM "SurveyParticipant";')
st.markdown("## SurveyParticipant")
st.write(df)
