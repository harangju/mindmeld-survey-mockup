import os
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
ads = [
  {
    "id": "cm2b3p8cg00ik7yauzkra3bo2",
  },
]

survey = ss.StreamlitSurvey("Display Ad Survey")

def submit():
  st.success("Your responses have been recorded. Thank you!")
  questions_json = json.dumps(questions, indent=2)
  print(questions_json)

num_pages = len(questions) * len(ads)
pages = survey.pages(
  num_pages,
  progress_bar=True,
  on_submit=submit,
)

with pages:

  index_question = pages.current // len(ads)
  question = questions[index_question]['question']

  index_ad = pages.current % len(ads)
  ad_id = ads[index_ad]["id"]
  image_url = f"https://mit-mindmeld.s3.us-east-2.amazonaws.com/ad mocks/ad_{ad_id}.png"

  item_id = f"{ad_id}_{index_question}"

  st.title("Display Ad Survey")

  st.markdown(
    "We are conducting a survey to understand how users interact with display ads. Please answer the following questions."
  )

  st.markdown(f"### Ad {index_ad+1}/{len(ads)}")

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
