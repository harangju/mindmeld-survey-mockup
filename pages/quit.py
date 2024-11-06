import streamlit as st

from auth import auth

auth()

instructions = """
You have quit the study.

Please go back to Prolific and return the study. Thank you!
"""

_, col, _ = st.columns([1, 3, 1])

with col:
  st.title("Display Ad Survey")

  st.markdown(instructions)

  st.html(
    "<a href='https://app.prolific.co/submissions/complete?cc=1'>Go back to Prolific</a>"
  )
