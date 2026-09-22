import random

import streamlit as st

from randq.selector import rand_draw


st.set_page_config(page_title="Cold-call selector", page_icon="?")
st.title("Cold-call selector")
st.write("Draw a classmate and a question for them to answer.")

def reset_session():
    st.session_state.names_input = ""
    st.session_state.questions_input = ""
    st.session_state.result = None
    st.session_state.used_pairs = set()
    st.session_state.draw_requested = False


names_text = st.text_area(
    "Names",
    placeholder="Enter one name per line",
    height=160,
    key="names_input",
)
questions_text = st.text_area(
    "Questions",
    placeholder="Enter one question per line",
    height=160,
    key="questions_input",
)

if "result" not in st.session_state:
    st.session_state.result = None
if "draw_requested" not in st.session_state:
    st.session_state.draw_requested = False
if "used_pairs" not in st.session_state:
    st.session_state.used_pairs = set()

draw_column, reset_column = st.columns(2)
with draw_column:
    if st.button("Draw", type="primary", use_container_width=True):
        st.session_state.draw_requested = True
with reset_column:
    st.button("Reset", on_click=reset_session, use_container_width=True)

no_repeats = st.checkbox("No repeats", help="Do not draw a previously selected pair during this session.")

if st.session_state.draw_requested:
    st.session_state.draw_requested = False
    names = [name.strip() for name in names_text.splitlines() if name.strip()]
    questions = [
        question.strip()
        for question in questions_text.splitlines()
        if question.strip()
    ]

    if not names:
        st.error("Enter at least one name.")
        st.stop()
    if not questions:
        st.error("Enter at least one question.")
        st.stop()

    try:
        st.session_state.result = rand_draw(
            names,
            questions,
            rng=random,
            excluded_pairs=st.session_state.used_pairs if no_repeats else None,
        )
    except ValueError as error:
        st.error(str(error))
        st.stop()

    if no_repeats:
        st.session_state.used_pairs.add(st.session_state.result)

if st.session_state.result:
    chosen_name, chosen_question = st.session_state.result
    st.success(f"{chosen_name}, please answer:")
    st.subheader(chosen_question)