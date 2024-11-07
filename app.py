import os
import streamlit as st
from lib.env import load_secrets

environment = os.getenv("ENVIRONMENT", "local")
project_id = "mindmeld-hj"
secret_id = "streamlit-secrets"

if environment == "production":
  load_secrets(project_id, secret_id)

if "prolific_id" in st.session_state and st.session_state["prolific_id"]:
  st.switch_page("pages/start.py")
  st.stop()

_, col, _ = st.columns([1, 3, 1])

with col:
  st.title("Display Ad Survey")

  prolific_id = st.text_input("Enter your Prolific ID: ")
  start_clicked = st.button("Start Survey", disabled=not prolific_id)

  if prolific_id:
    st.session_state["prolific_id"] = prolific_id

  if prolific_id and start_clicked:
    st.switch_page("pages/start.py")
