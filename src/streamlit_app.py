import streamlit as st

st.title("Hello")
name = st.text_input("Your name:")
if st.button("Submit"):
    st.text(f"Hello {name}, nice to meet you!")
