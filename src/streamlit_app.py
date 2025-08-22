import streamlit as st

st.title("Hello")
name = st.text_input("Enter your name")
if st.button("Submit"):
    st.text(f"Hello {name}")
