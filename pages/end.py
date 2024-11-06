import streamlit as st

if "prolific_id" not in st.session_state:
  st.error("You must enter your Prolific ID to start the survey.")
  login = st.button("Login")
  if login:
    st.session_state["prolific_id"] = None
    st.switch_page("app.py")
  st.stop()

instructions = """
Thank you for participating in our survey. Your responses will help us understand how users interact with display ads.

Please return to Prolific to complete the study. Thank you!
"""

_, col, _ = st.columns([1, 3, 1])

with col:
  st.title("Display Ad Survey")

  st.markdown(instructions)

  st.html(
    "<a href='https://app.prolific.co/submissions/complete?cc=1'>Return to Prolific</a>"
  )
