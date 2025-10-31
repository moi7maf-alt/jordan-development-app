import streamlit as st

st.title("My First Streamlit App")
st.write("This app is working successfully!")

name = st.text_input("What is your name?")
if name:
    st.success(f"Hello {name}!")
