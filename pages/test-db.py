import streamlit as st

from sqlalchemy import create_engine, text
from lib.db import get_survey_participant_index

# index = get_survey_participant_index('hi')
# st.write(f"Participant index: {index}")

endpoint_id = st.secrets['POSTGRES_HOST'].split('.')[0]
connection_url = f"postgresql://{st.secrets['POSTGRES_USER']}:{st.secrets['POSTGRES_PASSWORD']}@{st.secrets['POSTGRES_HOST']}:{st.secrets['POSTGRES_PORT']}/{st.secrets['POSTGRES_DATABASE']}?sslmode=require&options=endpoint%3D{endpoint_id}"
engine = create_engine(connection_url)

with engine.connect() as connection:
  query = text('SELECT * FROM "SurveyMockup";')
  result = connection.execute(query)
  surveys = result.fetchall()
  st.write(surveys[0])

  if surveys:
    survey = surveys[2]
    st.write(f"ID: {survey[0]}")
    st.write(f"Timestamp: {survey[1]}")
    st.write(f"Category: {survey[2]}")
    
    # Parse the JSON field
    survey_data = survey[3]
    st.write("Survey Data:")
    st.json(survey_data)