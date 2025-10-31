import streamlit as st

st.title("🚀 تطبيقي الأول على Streamlit")
st.write("هذا التطبيق يعمل بنجاح! ✅")

name = st.text_input("ما هو اسمك؟")
if name:
    st.success(f"مرحباً بك {name}! 🎉")

st.write("---")
st.write("تم تطوير هذا التطبيق باستخدام Streamlit")
