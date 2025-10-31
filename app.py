# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(
    page_title="منظومة الذكاء التنموي للمحافظات الأردنية",
    page_icon="🏛️",
    layout="wide"
)

# العنوان الرئيسي المحدث
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🏛️ منظومة الذكاء التنموي للمحافظات الأردنية</div>', unsafe_allow_html=True)

# بيانات المحافظات المحدثة
@st.cache_data
def load_comprehensive_data():
    data = {
        'المحافظة': ['عمان', 'المفرق', 'إربد', 'الزرقاء', 'البلقاء', 'مأدبا', 'معان', 'الكرك', 'جرش', 'عجلون', 'العقبة', 'الطفيلة'],
        'الكثافة_السكانية': [2543, 1383, 1087, 432, 342, 287, 6, 156, 198, 167, 45, 78],
        'معدل_البطالة': [18.5, 22.8, 21.5, 23.1, 19.8, 18.2, 24.3, 20.8, 19.5, 18.9, 17.2, 22.5],
        'مؤشر_التنمية_البشرية': [0.82, 0.72, 0.78, 0.75, 0.73, 0.75, 0.69, 0.74, 0.76, 0.77, 0.76, 0.68],
        'نصيب_الفرد_من_الناتج': [7800, 4500, 5200, 5800, 4800, 5100, 3800, 4200, 4900, 5000, 6200, 3600],
        'معدل_الفقر': [10.2, 18.5, 14.2, 15.8, 15.3, 13.7, 22.3, 16.8, 14.5, 13.9, 12.5, 24.1],
        'الاستثمار_العام': [850, 120, 180, 220, 95, 75, 45, 65, 60, 55, 320, 30],
        'المشاركة_الاقتصادية': [42.5, 38.2, 40.1, 39.8, 37.5, 38.9, 36.2, 37.8, 39.2, 38.5, 41.2, 35.8],
        'مساهمة_الزراعة': [2.1, 15.8, 12.5, 4.2, 8.7, 6.3, 9.8, 11.2, 10.5, 13.2, 3.5, 7.4],
        'اللاجئين_السوريين': [141315, 113298, 80626, 65020, 11934, 9281, 6420, 5771, 5425, 3518, 3015, 954]
    }
    return pd.DataFrame(data)

def show_main_dashboard():
    st.header("📊 اللوحة الرئيسية الشاملة")
    
    df = load_comprehensive_data()
    
    # مؤشرات سريعة
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_unemployment = df['معدل_البطالة'].mean()
        st.metric("متوسط معدل البطالة", f"{avg_unemployment:.1f}%", "هدف 2033: 12%")
    
    with col2:
        avg_hdi = df['مؤشر_التنمية_البشرية'].mean()
        st.metric("متوسط مؤشر التنمية البشرية", f"{avg_hdi:.2f}", "هدف 2033: 0.85")
    
    with col3:
        avg_economic = df['المشاركة_الاقتصادية'].mean()
        st.metric("متوسط المشاركة الاقتصادية", f"{avg_economic:.1f}%", "هدف 2033: 50%")
    
    with col4:
        total_refugees = df['اللاجئين_السوريين'].sum()
        st.metric("إجمالي اللاجئين السوريين", f"{total_refugees:,}")
    
    # رسوم بيانية
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.bar(df, x='المحافظة', y='معدل_البطالة',
                     title='معدلات البطالة في المحافظات',
                     color='معدل_البطالة')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.pie(df, values='اللاجئين_السوريين', names='المحافظة',
                     title='توزيع اللاجئين السوريين')
        st.plotly_chart(fig2, use_container_width=True)

def show_vision_2033():
    st.header("🎯 مواءمة مؤشرات التنمية مع رؤية التحديث الاقتصادي 2033")
    
    st.markdown("""
    ### الأهداف الاستراتيجية للرؤية 2033
    
    **🏗️ النمو الاقتصادي المستدام**
    - خفض معدل البطالة إلى 12%
    - زيادة المشاركة الاقتصادية إلى 50%
    - تنويع القاعدة الاقتصادية
    
    **👥 التنمية البشرية**
    - رفع مؤشر التنمية البشرية إلى 0.85
    - تحسين جودة الخدمات التعليمية والصحية
    - تعزيز العدالة الاجتماعية
    
    **🌱 الاستدامة البيئية**
    - تعزيز الزراعة المستدامة
    - الحفاظ على الموارد الطبيعية
    - تطوير الطاقة المتجددة
    """)
    
    df = load_comprehensive_data()
    
    # مؤشرات التقدم نحو 2033
    st.subheader("📈 مؤشرات التقدم نحو أهداف 2033")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_unemployment = df['معدل_البطالة'].mean()
        progress_2033 = ((22 - current_unemployment) / (22 - 12)) * 100
        st.metric("التقدم في خفض البطالة", f"{progress_2033:.1f}%", f"الحالي: {current_unemployment:.1f}%")
    
    with col2:
        current_hdi = df['مؤشر_التنمية_البشرية'].mean()
        progress_hdi = ((current_hdi - 0.72) / (0.85 - 0.72)) * 100
        st.metric("التقدم في التنمية البشرية", f"{progress_hdi:.1f}%", f"الحالي: {current_hdi:.2f}")
    
    with col3:
        current_economic = df['المشاركة_الاقتصادية'].mean()
        progress_economic = ((current_economic - 35) / (50 - 35)) * 100
        st.metric("التقدم في المشاركة الاقتصادية", f"{progress_economic:.1f}%", f"الحالي: {current_economic:.1f}%")
    
    # خارطة التقدم
    fig = px.scatter(df, x='مؤشر_التنمية_البشرية', y='المشاركة_الاقتصادية',
                    size='نصيب_الفرد_من_الناتج', color='المحافظة',
                    hover_data=['معدل_البطالة', 'مساهمة_الزراعة'],
                    title='خارطة التقدم نحو رؤية 2033')
    st.plotly_chart(fig, use_container_width=True)

def show_women_development():
    st.header("👩‍💼 مؤشرات تنمية المرأة")
    
    # بيانات تنمية المرأة
    women_data = {
        'المحافظة': ['عمان', 'المفرق', 'إربد', 'الزرقاء', 'البلقاء', 'مأدبا', 'معان', 'الكرك', 'جرش', 'عجلون', 'العقبة', 'الطفيلة'],
        'مشاركة_المرأة_الاقتصادية': [28.5, 15.2, 22.1, 18.8, 19.5, 21.3, 12.8, 20.2, 23.5, 24.1, 26.8, 14.5],
        'معدل_البطالة_النسائية': [24.8, 31.5, 28.2, 29.8, 26.3, 25.1, 33.2, 27.8, 25.5, 24.9, 23.2, 30.5],
        'التمثيل_النسائي': [32.5, 18.2, 25.8, 22.1, 20.5, 24.3, 15.8, 21.2, 26.5, 28.1, 30.2, 16.8]
    }
    
    df_women = pd.DataFrame(women_data)
    
    # مؤشرات سريعة
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_women_part = df_women['مشاركة_المرأة_الاقتصادية'].mean()
        st.metric("متوسط مشاركة المرأة الاقتصادية", f"{avg_women_part:.1f}%")
    
    with col2:
        avg_women_unemp = df_women['معدل_البطالة_النسائية'].mean()
        st.metric("متوسط بطالة النساء", f"{avg_women_unemp:.1f}%")
    
    with col3:
        avg_representation = df_women['التمثيل_النسائي'].mean()
        st.metric("متوسط التمثيل النسائي", f"{avg_representation:.1f}%")
    
    # رسوم بيانية
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.bar(df_women, x='المحافظة', y=['مشاركة_المرأة_الاقتصادية', 'معدل_البطالة_النسائية'],
                     title='مشاركة المرأة الاقتصادية والبطالة النسائية',
                     barmode='group')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.scatter(df_women, x='التمثيل_النسائي', y='مشاركة_المرأة_الاقتصادية',
                         size='معدل_البطالة_النسائية', color='المحافظة',
                         title='العلاقة بين التمثيل والمشاركة الاقتصادية')
        st.plotly_chart(fig2, use_container_width=True)

def show_interactive_map():
    st.header("🗺️ الخريطة التفاعلية لمحافظات الأردن")
    
    # خريطة مبسطة
    st.map(pd.DataFrame({
        'lat': [31.95, 32.34, 32.55, 32.06, 32.04, 31.72, 30.20, 31.18, 32.28, 32.33, 29.53, 30.83],
        'lon': [35.91, 36.20, 35.85, 36.09, 35.73, 35.79, 35.73, 35.70, 35.90, 35.75, 35.01, 35.60],
        'المحافظة': ['عمان', 'المفرق', 'إربد', 'الزرقاء', 'البلقاء', 'مأدبا', 'معان', 'الكرك', 'جرش', 'عجلون', 'العقبة', 'الطفيلة']
    }))
    
    st.info("""
    **دليل الخريطة:**
    - 🔵 النقاط الزرقاء: مراكز المحافظات
    - 📍 انقر على أي نقطة لرؤية اسم المحافظة
    - 🎯 استخدم زر التكبير/التصغير للتحكم في الخريطة
    """)

def main():
    # الشريط الجانبي
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50/2E86AB/FFFFFF?text=الأردن", width=150)
        st.title("القائمة الرئيسية")
        
        option = st.selectbox(
            "اختر القسم:",
            ["اللوحة الرئيسية", "رؤية 2033", "تنمية المرأة", "الخريطة التفاعلية", "التقارير التفصيلية"]
        )
        
        st.markdown("---")
        st.info("""
        **مصادر البيانات:**
        - دائرة الإحصاءات العامة
        - وزارة التخطيط
        - البنك الدولي
        - تقارير الأمم المتحدة
        """)
    
    if option == "اللوحة الرئيسية":
        show_main_dashboard()
    elif option == "رؤية 2033":
        show_vision_2033()
    elif option == "تنمية المرأة":
        show_women_development()
    elif option == "الخريطة التفاعلية":
        show_interactive_map()
    elif option == "التقارير التفصيلية":
        st.header("📋 التقارير التفصيلية للمحافظات")
        st.info("هذا القسم قيد التطوير...")
    
    # تذييل الصفحة
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p><b>منظومة الذكاء التنموي للمحافظات الأردنية - تم التطوير بالاعتماد على البيانات الرسمية</b></p>
        <p>© 2025 - المملكة الأردنية الهاشمية - جميع الحقوق محفوظة</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
