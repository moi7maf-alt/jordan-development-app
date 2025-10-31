import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="تطبيقي الكامل", page_icon="🚀", layout="wide")

# العنوان الرئيسي
st.title("🚀 تطبيقي الأول على Streamlit")
st.markdown("---")

# قسم المقدمة
st.header("🎯 المقدمة")
st.write("مرحباً بك في تطبيقي الأول! هذا التطبيق يعمل بنجاح!")

# قسم الإدخال
st.header("📝 التفاعل مع المستخدم")
name = st.text_input("ما هو اسمك؟", placeholder="اكتب اسمك هنا...")

if name:
    st.success(f"مرحباً بك {name}! 🎉")
    st.balloons()  # تأثير بالونات

# قسم المعلومات
st.header("ℹ️ معلومات عن التطبيق")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("المستخدمين", "1", "+1")

with col2:
    st.metric("الحالة", "نشط", "100%")

with col3:
    st.metric("الإصدار", "1.0", "مستقر")

# قسم إضافي
st.header("✨ ميزات إضافية")
if st.button("اضغط هنا للحصول على ترحيب خاص!"):
    st.info("🔥 تهانينا! أنت تستخدم Streamlit بنجاح!")

# شريط التقدم
st.header("📊 شريط التقدم")
progress = st.slider("ما هي نسبة إكمالك للتطبيق؟", 0, 100, 50)
st.progress(progress)

# نهاية الصفحة
st.markdown("---")
st.write("⚡ تم تطوير هذا التطبيق باستخدام Streamlit")
