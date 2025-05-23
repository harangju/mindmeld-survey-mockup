import streamlit as st
import uuid
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

conn = st.connection("postgresql", type="sql")

def get_survey_participant_index(prolific_id):
  """
  Get the next survey participant index and insert the new participant atomically
  """
  connection = conn.engine.connect()
  transaction = connection.begin()
  try:
    # Check if the participant already exists
    result = connection.execute(
      text('SELECT "index" FROM "SurveyParticipant" WHERE "prolificId" = :prolific_id;'),
      {'prolific_id': prolific_id}
    )
    existing_index = result.scalar()
    
    if existing_index is not None:
      return existing_index

    # Get the largest index
    result = connection.execute(text('SELECT MAX("index") FROM "SurveyParticipant";'))
    max_index = result.scalar()
    next_index = (max_index or 0) + 1

    # Generate a unique ID for the new participant
    new_id = str(uuid.uuid4())

    # Insert the new participant
    connection.execute(
      text('INSERT INTO "SurveyParticipant" ("id", "prolificId", "index") VALUES (:id, :prolific_id, :index);'),
      {'id': new_id, 'prolific_id': prolific_id, 'index': next_index}
    )
    
    # Commit the transaction
    transaction.commit()
    
    return next_index
  except SQLAlchemyError as e:
    transaction.rollback()
    raise e
  finally:
    connection.close()

def upload_data(prolific_id, data):
  """
  Upload a row to SurveyMockup with the given prolific_id and data JSON
  """
  connection = conn.engine.connect()
  transaction = connection.begin()
  try:
    # Generate a unique ID for the new mockup
    new_id = str(uuid.uuid4())

    # Insert the new mockup data
    connection.execute(
      text('INSERT INTO "SurveyMockup" ("id", "prolificId", "data") VALUES (:id, :prolific_id, :data);'),
      {'id': new_id, 'prolific_id': prolific_id, 'data': data}
    )
    
    # Commit the transaction
    transaction.commit()
    return True
  except SQLAlchemyError as e:
    transaction.rollback()
    raise e
  finally:
    connection.close()
