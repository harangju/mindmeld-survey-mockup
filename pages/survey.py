import streamlit as st
import streamlit_survey as ss

from lib.auth import auth
from lib.data import get_samples
from lib.variables import questions
from lib.db import get_survey_participant_index

auth()

participant_index = get_survey_participant_index(st.session_state["prolific_id"])
ad_ids = get_samples(participant_index)

def submit():
  st.success("Your responses have been recorded. Thank you!")
  json = survey.to_json()
  prolific_id = st.session_state["prolific_id"]
  package = {
    "prolific_id": prolific_id,
    "survey": json,
  }
  # TODO: Send the responses to the server
  # and Prolific IDs
  st.switch_page("pages/end.py")

def question_answered(index):
  index_question = index % len(questions)
  index_ad = int(index / len(questions))
  ad_id = ad_ids[index_ad]
  question_id = f"{ad_id}_{index_question}"
  return (
    question_id in survey.data and "Select option" not in survey.data[question_id]["value"]
  )

survey = ss.StreamlitSurvey("Display Ad Survey")
num_pages = len(questions) * len(ad_ids)
pages = survey.pages(
  num_pages,
  progress_bar=True,
  on_submit=submit,
)

next_button = lambda pages: st.button(
  "Next",
  use_container_width=True,
  on_click=pages.next,
  disabled=(pages.current == pages.n_pages-1) or not question_answered(pages.current),
  key=f"{pages.current_page_key}_btn_next_custom",
)
pages.next_button = next_button

submit_button = lambda pages: st.button(
  "Submit",
  use_container_width=True,
  type="primary",
  disabled=not question_answered(pages.current),
  key=f"{pages.current_page_key}_btn_next_custom",
)
pages.submit_button = submit_button

with pages:

  index_question = pages.current % len(questions)
  question = questions[index_question]['question']
  options = questions[index_question]['options']

  index_ad = int(pages.current / len(questions))
  ad_id = ad_ids[index_ad]
  image_url = f"https://mit-mindmeld.s3.us-east-2.amazonaws.com/ad mocks/ad_{ad_id}.png"

  item_id = f"{ad_id}_{index_question}"

  st.markdown(f"### Display Ad Survey")
  st.markdown("Please rate the following questions based on the ad below:")

  _, col, _ = st.columns([1, 2, 1])
  with col:
    st.markdown(f"##### Ad :gray-background[{index_ad+1}/{len(ad_ids)}]")
    st.image(image_url)
    st.markdown(f"##### :gray-background[Q{index_question+1}] {question}")
    response = survey.radio(
      item_id,
      options=options,
      index=0,
      label_visibility="collapsed",
    )
    questions[index_question]["answer"] = response
    st.divider()

json = survey.to_json()
st.write(f"Prolific ID: {st.session_state['prolific_id']}")
st.json(json)