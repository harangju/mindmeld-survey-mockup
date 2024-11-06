import json
import streamlit as st
import streamlit_survey as ss

likert_scale = ["Select option", "Strongly Agree", "Agree", "Somewhat Agree", "Neutral", "Somewhat Disagree", "Disagree", "Strongly Disagree"]
questions = [
  {
    "question": "Is the copy clear and easy to read?",
    "options": likert_scale,
    "answer": None,
  },
  {
    "question": "Is the ad visually appealing?",
    "options": likert_scale,
    "answer": None,
  },
  {
    "question": "How likely are you to click on this ad?",
    "options": likert_scale,
    "answer": None,
  },
]
ad_ids = [
  "cm2b3p8cg00ik7yauzkra3bo2",
]

survey = ss.StreamlitSurvey("Display Ad Survey")

def submit():
  st.success("Your responses have been recorded. Thank you!")
  questions_json = json.dumps(questions, indent=2)
  print(questions_json)

num_pages = len(questions) * len(ad_ids)
pages = survey.pages(
  num_pages,
  progress_bar=True,
  on_submit=submit,
)

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
