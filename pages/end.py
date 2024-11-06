import streamlit as st

from lib.auth import auth
from lib.variables import prolific_completion_code

auth()

if not st.session_state.get("survey_complete"):
  st.error("Please complete the survey before continuing.")
  st.stop()

instructions = """
:green-background[Your responses have been recorded.]

Thank you for participating in our survey. Your responses will help us understand how users interact with display ads.

Please return to Prolific to complete the study. Thank you!
"""

_, col, _ = st.columns([1, 3, 1])

with col:
  st.title("Display Ad Survey")

  st.markdown(instructions)

  st.html(
    f"<a href='https://app.prolific.co/submissions/complete?cc={prolific_completion_code}'>Return to Prolific</a>"
  )
