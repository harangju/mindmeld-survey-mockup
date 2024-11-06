import json
import streamlit as st
import streamlit_survey as ss

from auth import auth
from variables import likert_scale, questions, ad_ids

auth()

def submit():
  st.success("Your responses have been recorded. Thank you!")
  questions_json = json.dumps(questions, indent=2)
  # TODO: Send the responses to the server
  st.switch_page("pages/end.py")

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
  disabled=(pages.current == pages.n_pages-1) or (questions[pages.current]["answer"] == "Select option"),
  key=f"{pages.current_page_key}_btn_next_custom",
)
pages.next_button = next_button

submit_button = lambda pages: st.button(
  "Submit",
  use_container_width=True,
  type="primary",
  disabled=questions[pages.current]["answer"] == "Select option",
  key=f"{pages.current_page_key}_btn_next_custom",
)
pages.submit_button = submit_button

with pages:

  index_question = pages.current // len(ad_ids)
  question = questions[index_question]['question']

  index_ad = pages.current % len(ad_ids)
  ad_id = ad_ids[index_ad]
  image_url = f"https://mit-mindmeld.s3.us-east-2.amazonaws.com/ad mocks/ad_{ad_id}.png"

  item_id = f"{ad_id}_{index_question}"

  st.markdown(f"### Ad #{index_ad+1}")
  st.markdown("Please rate the following questions based on the ad below:")

  _, col, _ = st.columns([1, 3, 1])
  with col:
    st.image(image_url)
    st.markdown(f"**{question}**")
    response = survey.radio(
      item_id,
      options=likert_scale,
      index=0,
      label_visibility="collapsed",
    )

    questions[index_question]["answer"] = response
