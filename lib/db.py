import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

connection_url = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DATABASE']}?sslmode=require"
engine = create_engine(connection_url)

def get_survey_participant_index(prolific_id):
    """
    Get the next survey participant index and insert the new participant atomically
    """
    connection = engine.connect()
    transaction = connection.begin()
    try:
        # Get the largest index
        result = connection.execute('SELECT MAX("index") FROM "SurveyParticipant";')
        max_index = result.scalar()
        next_index = (max_index or 0) + 1

        # Insert the new participant
        connection.execute(
            'INSERT INTO "SurveyParticipant" ("prolificId", "index") VALUES (%s, %s);',
            (prolific_id, next_index)
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
    connection = engine.connect()
    transaction = connection.begin()
    try:
        # Insert the new mockup data
        connection.execute(
            'INSERT INTO "SurveyMockup" ("prolificId", "data") VALUES (%s, %s);',
            (prolific_id, data)
        )
        
        # Commit the transaction
        transaction.commit()
    except SQLAlchemyError as e:
        transaction.rollback()
        raise e
    finally:
        connection.close()
