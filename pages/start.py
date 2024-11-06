import streamlit as st

from auth import auth

auth()

instructions = """
We are conducting a survey to understand how users interact with display ads.

If you would like to participate, please click "Start Survey".

If you would like to quit, please click "Quit Study".
"""

_, col, _ = st.columns([1, 3, 1])

with col:
  st.title("Display Ad Survey")

  st.markdown(instructions)

  left, _, right = st.columns(3)
  with left:
    quit_button = st.button(
      "Quit Study",
      help="If you quit, you are returning the study.",
    )
  with right:
    start_button = st.button("Start Study")

  if start_button:
    st.switch_page("pages/instructions.py")

  if quit_button:
    st.switch_page("pages/quit.py")
