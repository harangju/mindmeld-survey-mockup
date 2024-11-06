import streamlit as st

from lib.auth import auth

auth()

instructions = """
In this survey, you will be shown a series of display ads and asked to rate them based on a set of questions.

#### Definitions

A **display ad** is a type of online advertisement that is displayed on a webpage. It can be in the form of a banner, image, or video.

What is a **copy**? It is the text that appears on the ad. For example, "Get 50% off today!" is a copy.

#### What is the ad for?

The ad is for an annual report by a research organization that studies the impact of digital technologies on society, business, and the economy.

#### How many ads will I see?
You will see 40 ads in total. For each ad, there are 3 questions to answer.
"""

_, col, _ = st.columns([1, 3, 1])

with col:
  st.title("Display Ad Survey")

  st.markdown(instructions)

  _, center, _ = st.columns(3)
  with center:
    start_button = st.button("Start Survey")

  if start_button:
    st.switch_page("pages/survey.py")
