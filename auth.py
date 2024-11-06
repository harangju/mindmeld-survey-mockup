import streamlit as st

def auth():
  if "prolific_id" not in st.session_state or st.session_state["prolific_id"] is None:
    st.error("You must enter your Prolific ID to start the survey.")
    login = st.button("Login")
    if login:
      st.session_state["prolific_id"] = None
      st.switch_page("app.py")
    st.stop()
