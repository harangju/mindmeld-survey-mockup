import streamlit as st
import streamlit_survey as ss

from lib.auth import auth
from lib.data import get_samples
from lib.variables import questions
from lib.db import get_survey_participant_index, upload_data

max_post_survey_attempts = 10

auth()

participant_index = get_survey_participant_index(st.session_state["prolific_id"])
ad_ids = get_samples(participant_index)

def submit():
  data = survey.to_json()
  prolific_id = st.session_state["prolific_id"]
  submitted = False
  tries = 0
  while not submitted and tries < max_post_survey_attempts:
    try:
      submitted = upload_data(prolific_id, data)
      tries += 1
    except Exception as e:
      st.error(f"Error: {e}")
  # st.switch_page("pages/end.py")

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
  st.markdown("The ad is for an annual report by a research organization that studies the impact of digital technologies on society, business, and the economy. Please rate the following questions based on the ad below:")

  left, right = st.columns(2)
  with left:
    st.markdown(f"##### Ad :gray-background[{index_ad+1}/{len(ad_ids)}]")
    st.image(image_url)
  with right:
    header = "##### "
    for i, q in enumerate(questions):
      if i == index_question:
        header += f":red-background[Q{i+1}] "
      else:
        header += f":gray-background[Q{i+1}] "
      if i < len(questions) - 1:
        header += " — "
    st.markdown(header)
    st.markdown(f'**{question}**')
    response = survey.radio(
      item_id,
      options=options,
      index=0,
      label_visibility="collapsed",
    )
    questions[index_question]["answer"] = response
