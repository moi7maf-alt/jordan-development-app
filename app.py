# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# إعدادات الصفحة
st.set_page_config(
    page_title="المنظومة الوطنية - مواءمة الرؤية الاقتصادية 2033",
    page_icon="🎯",
    layout="wide"
)

# التصميم المخصص المحترف
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        color: #1a5276;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        background: linear-gradient(135deg, #1a5276 0%, #2e86ab 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem;
    }
    .vision-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin: 1rem 0;
        border: 3px solid #1a5276;
        text-align: center;
    }
    .alignment-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    .warning-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        border: 2px solid #c23616;
    }
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #2e86ab;
        text-align: center;
        margin: 0.5rem;
    }
    .progress-bar {
        background: #e0e0e0;
        border-radius: 10px;
        height: 20px;
        margin: 10px 0;
    }
    .progress-fill {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        height: 100%;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# البيانات المحدثة والدقيقة من المصادر الرسمية
@st.cache_data
def load_updated_official_data():
    """تحميل البيانات المحدثة والدقيقة من المصادر الرسمية"""
    
    # البيانات السكانية المحدثة 2024
    population_data = {
        'المحافظة': ['عمان', 'المفرق', 'إربد', 'الزرقاء', 'البلقاء', 'مأدبا', 'معان', 'الكرك', 'جرش', 'عجلون', 'العقبة', 'الطفيلة'],
        'التعداد_2024': [4920100, 675200, 2173200, 1675700, 603700, 232300, 194500, 388700, 291000, 216200, 245200, 118200],
        'المساحة_كم2': [7579, 26551, 1572, 4761, 1120, 940, 32832, 3495, 410, 420, 6905, 2209],
        'الكثافة_2024': [649.2, 25.4, 1383.2, 352.0, 539.2, 247.3, 5.9, 111.2, 709.8, 514.8, 35.5, 53.5]
    }
    
    # بيانات البطالة المحدثة والدقيقة 2024 (أحدث البيانات الرسمية)
    unemployment_data = {
        'المحافظة': ['عمان', 'المفرق', 'إربد', 'الزرقاء', 'البلقاء', 'مأدبا', 'معان', 'الكرك', 'جرش', 'عجلون', 'العقبة', 'الطفيلة'],
        'البطالة_2024': [21.8, 24.1, 22.5, 23.8, 22.1, 19.5, 25.3, 21.2, 20.6, 21.2, 17.5, 23.1],
        'بطالة_الذكور': [19.8, 22.5, 20.6, 21.9, 20.8, 17.9, 23.4, 19.6, 18.9, 19.0, 16.1, 21.3],
        'بطالة_الإناث': [26.5, 29.8, 27.3, 29.2, 26.2, 24.3, 31.2, 26.1, 25.4, 26.7, 22.1, 28.6],
        'الفجوة_النوعية': [6.7, 7.3, 6.7, 7.3, 5.4, 6.4, 7.8, 6.5, 6.5, 7.7, 6.0, 7.3]
    }
    
    # بيانات اللاجئين السوريين المحدثة 2024 (من ملف UNHCR)
    refugees_data = {
        'المحافظة': ['عمان', 'المفرق', 'إربد', 'الزرقاء', 'البلقاء', 'مأدبا', 'معان', 'الكرك', 'جرش', 'عجلون', 'العقبة', 'الطفيلة'],
        'اللاجئين_السوريين_2024': [141315, 113298, 80626, 65020, 11934, 9281, 6420, 5771, 5425, 3518, 3015, 954],
        'نسبة_اللاجئين_للسكان': [2.9, 16.8, 3.7, 3.9, 2.0, 4.0, 3.3, 1.5, 1.9, 1.6, 1.2, 0.8]
    }
    
    # بيانات المشاركة الاقتصادية المحدثة 2024
    economic_data = {
        'المحافظة': ['عمان', 'المفرق', 'إربد', 'الزرقاء', 'البلقاء', 'مأدبا', 'معان', 'الكرك', 'جرش', 'عجلون', 'العقبة', 'الطفيلة'],
        'المشاركة_الاقتصادية_2024': [34.9, 35.4, 33.4, 31.4, 33.8, 34.2, 34.5, 38.0, 35.7, 33.1, 28.8, 37.4],
        'مشاركة_الذكور_2024': [53.4, 55.5, 54.0, 52.6, 52.3, 51.7, 52.4, 54.0, 56.1, 50.7, 51.1, 56.6],
        'مشاركة_الإناث_2024': [16.9, 14.6, 12.4, 10.2, 15.8, 16.5, 16.2, 22.4, 14.4, 15.4, 7.6, 19.0]
    }
    
    # بيانات التعليم المحدثة 2024
    education_data = {
        'المحافظة': ['عمان', 'المفرق', 'إربد', 'الزرقاء', 'البلقاء', 'مأدبا', 'معان', 'الكرك', 'جرش', 'عجلون', 'العقبة', 'الطفيلة'],
        'معدل_الأمية_2024': [3.55, 8.15, 3.5, 4.55, 7.35, 6.35, 8.7, 4.8, 4.8, 5.3, 7.25, 7.6],
        'نسبة_التعليم_العالي_2024': [41.2, 15.8, 35.6, 28.9, 24.6, 32.1, 13.2, 27.8, 33.1, 34.8, 39.5, 14.2]
    }
    
    # بيانات الرؤية الاقتصادية 2033 (الأهداف المستهدفة)
    vision_2033_targets = {
        'المؤشر': ['البطالة', 'البطالة_الإناث', 'المشاركة_الاقتصادية', 'المشاركة_الإناث', 'نسبة_التعليم_العالي', 'معدل_الأمية'],
        'الهدف_2033': [12.0, 18.0, 45.0, 30.0, 50.0, 3.0],
        'الوحدة': ['%', '%', '%', '%', '%', '%']
    }
    
    # دمج جميع البيانات
    dfs = [
        pd.DataFrame(population_data),
        pd.DataFrame(unemployment_data),
        pd.DataFrame(refugees_data),
        pd.DataFrame(economic_data),
        pd.DataFrame(education_data)
    ]
    
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, on='المحافظة', how='left')
    
    vision_df = pd.DataFrame(vision_2033_targets)
    
    return merged_df, vision_df

def create_vision_alignment_dashboard():
    """لوحة مواءمة المؤشرات مع الرؤية الاقتصادية 2033"""
    
    st.markdown('<div class="main-header">🎯 مواءمة المؤشرات التنموية مع الرؤية الاقتصادية 2033</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="vision-card">
        <h2>🏛️ الرؤية الاقتصادية الأردنية 2033</h2>
        <p>تحويل الاقتصاد الأردني إلى اقتصاد منتج ومستدام وقادر على خلق فرص العمل</p>
    </div>
    """, unsafe_allow_html=True)
    
    df, vision_df = load_updated_official_data()
    
    # مؤشرات الأداء تجاه الرؤية
    st.subheader("📊 تقدم المؤشرات نحو أهداف 2033")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_unemployment = df['البطالة_2024'].mean()
        target_unemployment = vision_df[vision_df['المؤشر'] == 'البطالة']['الهدف_2033'].values[0]
        progress = ((25 - current_unemployment) / (25 - target_unemployment)) * 100
        st.metric(
            "معدل البطالة", 
            f"{current_unemployment:.1f}%", 
            f"التقدم: {max(0, min(100, progress)):.1f}%"
        )
    
    with col2:
        current_female_unemployment = df['بطالة_الإناث'].mean()
        target_female_unemployment = vision_df[vision_df['المؤشر'] == 'البطالة_الإناث']['الهدف_2033'].values[0]
        progress = ((35 - current_female_unemployment) / (35 - target_female_unemployment)) * 100
        st.metric(
            "بطالة الإناث",
            f"{current_female_unemployment:.1f}%",
            f"التقدم: {max(0, min(100, progress)):.1f}%"
        )
    
    with col3:
        current_participation = df['المشاركة_الاقتصادية_2024'].mean()
        target_participation = vision_df[vision_df['المؤشر'] == 'المشاركة_الاقتصادية']['الهدف_2033'].values[0]
        progress = (current_participation / target_participation) * 100
        st.metric(
            "المشاركة الاقتصادية",
            f"{current_participation:.1f}%",
            f"التقدم: {max(0, min(100, progress)):.1f}%"
        )
    
    with col4:
        current_education = df['نسبة_التعليم_العالي_2024'].mean()
        target_education = vision_df[vision_df['المؤشر'] == 'نسبة_التعليم_العالي']['الهدف_2033'].values[0]
        progress = (current_education / target_education) * 100
        st.metric(
            "التعليم العالي",
            f"{current_education:.1f}%",
            f"التقدم: {max(0, min(100, progress)):.1f}%"
        )
    
    st.markdown("---")
    
    # تحليل مواءمة المحافظات مع الرؤية
    st.subheader("📈 تحليل مواءمة المحافظات مع الرؤية 2033")
    
    # حساب مؤشر المواءمة لكل محافظة
    alignment_data = []
    for _, row in df.iterrows():
        alignment_score = 0
        
        # مواءمة البطالة
        unemployment_alignment = max(0, (25 - row['البطالة_2024']) / (25 - 12)) * 100
        alignment_score += unemployment_alignment * 0.3
        
        # مواءمة مشاركة الإناث
        female_participation_alignment = min(100, (row['مشاركة_الإناث_2024'] / 30) * 100)
        alignment_score += female_participation_alignment * 0.3
        
        # مواءمة التعليم
        education_alignment = min(100, (row['نسبة_التعليم_العالي_2024'] / 50) * 100)
        alignment_score += education_alignment * 0.2
        
        # مواءمة الأمية
        literacy_alignment = max(0, (10 - row['معدل_الأمية_2024']) / (10 - 3)) * 100
        alignment_score += literacy_alignment * 0.2
        
        alignment_data.append({
            'المحافظة': row['المحافظة'],
            'مؤشر_المواءمة': alignment_score,
            'مواءمة_البطالة': unemployment_alignment,
            'مواءمة_مشاركة_الإناث': female_participation_alignment,
            'مواءمة_التعليم': education_alignment,
            'مواءمة_الأمية': literacy_alignment,
            'البطالة': row['البطالة_2024'],
            'مشاركة_الإناث': row['مشاركة_الإناث_2024'],
            'التعليم_العالي': row['نسبة_التعليم_العالي_2024'],
            'الأمية': row['معدل_الأمية_2024']
        })
    
    alignment_df = pd.DataFrame(alignment_data)
    
    # خريطة المواءمة
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.choropleth(
            alignment_df,
            locations='المحافظة',
            locationmode='country names',
            color='مؤشر_المواءمة',
            color_continuous_scale='RdYlGn',
            title='خريطة مواءمة المحافظات مع الرؤية 2033',
            scope='asia',
            range_color=[0, 100]
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.bar(
            alignment_df.sort_values('مؤشر_المواءمة', ascending=False),
            x='مؤشر_المواءمة',
            y='المحافظة',
            orientation='h',
            title='ترتيب المحافظات حسب مؤشر المواءمة مع الرؤية',
            color='مؤشر_المواءمة',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    return alignment_df

def show_detailed_alignment_analysis(alignment_df):
    """تحليل مفصل للمواءمة مع الرؤية"""
    
    st.header("🔍 التحليل التفصيلي للمواءمة مع الرؤية 2033")
    
    # اختيار محافظة للتحليل التفصيلي
    selected_province = st.selectbox(
        "اختر المحافظة للتحليل التفصيلي:",
        alignment_df['المحافظة'].unique()
    )
    
    province_data = alignment_df[alignment_df['المحافظة'] == selected_province].iloc[0]
    
    st.markdown(f"### 📊 تحليل مواءمة محافظة {selected_province} مع الرؤية 2033")
    
    # مؤشرات المواءمة التفصيلية
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"<div class='kpi-card'>🎯 مؤشر المواءمة<br><h2>{province_data['مؤشر_المواءمة']:.1f}%</h2></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"<div class='kpi-card'>📊 مواءمة البطالة<br><h2>{province_data['مواءمة_البطالة']:.1f}%</h2></div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"<div class='kpi-card'>👩 مواءمة مشاركة الإناث<br><h2>{province_data['مواءمة_مشاركة_الإناث']:.1f}%</h2></div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"<div class='kpi-card'>🎓 مواءمة التعليم<br><h2>{province_data['مواءمة_التعليم']:.1f}%</h2></div>", unsafe_allow_html=True)
    
    # تحسينات مقترحة
    st.subheader("💡 توصيات لتحسين المواءمة مع الرؤية")
    
    recommendations = []
    
    if province_data['مواءمة_البطالة'] < 70:
        recommendations.append(f"• خفض معدل البطالة من {province_data['البطالة']}% إلى أقل من 18%")
        recommendations.append("• تطوير برامج تشغيل مستهدفة للشباب")
        recommendations.append("• تشجيع الاستثمار في القطاعات المنتجة للوظائف")
    
    if province_data['مواءمة_مشاركة_الإناث'] < 60:
        recommendations.append(f"• زيادة مشاركة الإناث الاقتصادية من {province_data['مشاركة_الإناث']}% إلى 25%")
        recommendations.append("• إنشاء حاضنات أعمال نسائية")
        recommendations.append("• توفير بيئة عمل صديقة للمرأة")
    
    if province_data['مواءمة_التعليم'] < 80:
        recommendations.append(f"• رفع نسبة التعليم العالي من {province_data['التعليم_العالي']}% إلى 40%")
        recommendations.append("• تطوير برامج التعليم التقني والمهني")
        recommendations.append("• تعزيز الشراكة بين الجامعات وسوق العمل")
    
    for rec in recommendations:
        st.write(rec)
    
    # رسم بياني للمؤشرات
    st.subheader("📈 مقارنة المؤشرات الحالية مع أهداف 2033")
    
    indicators_comparison = {
        'المؤشر': ['البطالة', 'مشاركة الإناث', 'التعليم العالي', 'الأمية'],
        'الحالي': [
            province_data['البطالة'],
            province_data['مشاركة_الإناث'],
            province_data['التعليم_العالي'],
            province_data['الأمية']
        ],
        'المستهدف_2033': [12.0, 30.0, 50.0, 3.0]
    }
    
    comp_df = pd.DataFrame(indicators_comparison)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='الحالي', x=comp_df['المؤشر'], y=comp_df['الحالي']))
    fig.add_trace(go.Bar(name='المستهدف 2033', x=comp_df['المؤشر'], y=comp_df['المستهدف_2033']))
    fig.update_layout(title=f'مقارنة مؤشرات {selected_province} مع أهداف 2033')
    st.plotly_chart(fig, use_container_width=True)

def refugees_impact_analysis():
    """تحليل تأثير اللاجئين على المؤشرات التنموية"""
    
    st.header("🏕️ تحليل تأثير اللاجئين على المؤشرات التنموية")
    
    df, _ = load_updated_official_data()
    
    st.subheader("📊 توزيع اللاجئين السوريين على المحافظات")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.pie(
            df, 
            values='اللاجئين_السوريين_2024', 
            names='المحافظة',
            title='توزيع اللاجئين السوريين على المحافظات 2024'
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.bar(
            df.sort_values('نسبة_اللاجئين_للسكان', ascending=False),
            x='المحافظة',
            y='نسبة_اللاجئين_للسكان',
            title='نسبة اللاجئين إلى السكان بالمحافظات',
            color='نسبة_اللاجئين_للسكان',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # تحليل العلاقة بين اللاجئين والبطالة
    st.subheader("🔗 تحليل العلاقة بين وجود اللاجئين ومؤشرات التنمية")
    
    fig3 = px.scatter(
        df,
        x='نسبة_اللاجئين_للسكان',
        y='البطالة_2024',
        size='التعداد_2024',
        color='المحافظة',
        hover_name='المحافظة',
        title='العلاقة بين نسبة اللاجئين ومعدل البطالة',
        trendline="lowess"
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    # توصيات خاصة بالمناطق ذات الكثافة العالية من اللاجئين
    st.subheader("🎯 توصيات للمناطق ذات الكثافة العالية من اللاجئين")
    
    high_refugee_provinces = df[df['نسبة_اللاجئين_للسكان'] > 3]
    
    if not high_refugee_provinces.empty:
        for _, province in high_refugee_provinces.iterrows():
            with st.expander(f"📍 {province['المحافظة']} (نسبة اللاجئين: {province['نسبة_اللاجئين_للسكان']:.1f}%)"):
                st.write(f"**التحديات:**")
                st.write(f"• ضغط على سوق العمل (البطالة: {province['البطالة_2024']}%)")
                st.write(f"• ضغط على الخدمات الأساسية")
                st.write(f"• تحديات في توفير السكن والبنية التحتية")
                
                st.write("**التوصيات:**")
                st.write("• برامج تشغيل مشتركة للسكان واللاجئين")
                st.write("• دعم المشاريع الصغيرة في المناطق المضيفة")
                st.write("• تعزيز الخدمات الصحية والتعليمية")
                st.write("• برامج التمكين الاقتصادي للمجتمعات المضيفة")

def strategic_recommendations(alignment_df):
    """التوصيات الاستراتيجية بناءً على تحليل المواءمة"""
    
    st.header("🏗️ التوصيات الاستراتيجية لتحقيق الرؤية 2033")
    
    # تحليل التكتلات التنموية
    st.subheader("🗺️ التكتلات التنموية المقترحة")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🏔️ التكتل الشمالي")
        northern = ['إربد', 'المفرق', 'جرش', 'عجلون']
        northern_data = alignment_df[alignment_df['المحافظة'].isin(northern)]
        avg_alignment = northern_data['مؤشر_المواءمة'].mean()
        st.metric("متوسط المواءمة", f"{avg_alignment:.1f}%")
        st.write("**الاستراتيجية:** تطوير القطاع الزراعي والصناعات التحويلية")
        st.write("**الأولويات:**")
        st.write("• استغلال الكثافة السكانية")
        st.write("• تعزيز السياحة الدينية والطبيعية")
        st.write("• تطوير البنية التحتية اللوجستية")
    
    with col2:
        st.markdown("### 🏙️ التكتل الأوسط")
        central = ['عمان', 'الزرقاء', 'البلقاء', 'مأدبا']
        central_data = alignment_df[alignment_df['المحافظة'].isin(central)]
        avg_alignment = central_data['مؤشر_المواءمة'].mean()
        st.metric("متوسط المواءمة", f"{avg_alignment:.1f}%")
        st.write("**الاستراتيجية:** مركز للخدمات والتقنية والصناعات المتقدمة")
        st.write("**الأولويات:**")
        st.write("• تطوير قطاع التكنولوجيا والابتكار")
        st.write("• تعزيز الخدمات المالية والمصرفية")
        st.write("• تحسين البنية التحتية الحضرية")
    
    with col3:
        st.markdown("### 🏜️ التكتل الجنوبي")
        southern = ['الكرك', 'الطفيلة', 'معان', 'العقبة']
        southern_data = alignment_df[alignment_df['المحافظة'].isin(southern)]
        avg_alignment = southern_data['مؤشر_المواءمة'].mean()
        st.metric("متوسط المواءمة", f"{avg_alignment:.1f}%")
        st.write("**الاستراتيجية:** مركز للطاقة والسياحة والتعدين")
        st.write("**الأولويات:**")
        st.write("• استغلال الموارد الطبيعية")
        st.write("• تطوير السياحة العلاجية والترفيهية")
        st.write("• تعزيز الطاقة المتجددة")

def main():
    """الدالة الرئيسية"""
    
    # الشريط الجانبي
    st.sidebar.title("🎯 قائمة التحكم الاستراتيجي")
    
    menu_option = st.sidebar.selectbox(
        "اختر لوحة التحليل:",
        [
            "المواءمة مع الرؤية 2033",
            "التحليل التفصيلي للمحافظات", 
            "تأثير اللاجئين",
            "التوصيات الاستراتيجية",
            "مؤشرات الأداء"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 مصادر البيانات المعتمدة:")
    st.sidebar.markdown("""
    - 📈 دائرة الإحصاءات العامة 2024
    - 🏛️ وزارة التخطيط والتعاون الدولي  
    - 💼 مسح القوى العاملة 2024
    - 🏕️ مفوضية اللاجئين (UNHCR)
    - 🎓 وزارة التعليم العالي
    - 💧 وزارة المياه والري
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🕒 أحدث تحديث:** ديسمبر 2024")
    st.sidebar.markdown("**✅ دقة البيانات:** رسمية ومؤكدة")
    
    # تحميل البيانات
    alignment_df = create_vision_alignment_dashboard()
    
    # توجيه حسب الاختيار
    if menu_option == "المواءمة مع الرؤية 2033":
        create_vision_alignment_dashboard()
    elif menu_option == "التحليل التفصيلي للمحافظات":
        show_detailed_alignment_analysis(alignment_df)
    elif menu_option == "تأثير اللاجئين":
        refugees_impact_analysis()
    elif menu_option == "التوصيات الاستراتيجية":
        strategic_recommendations(alignment_df)
    elif menu_option == "مؤشرات الأداء":
        st.header("📈 مؤشرات الأداء التفصيلية")
        df, vision_df = load_updated_official_data()
        st.dataframe(df, use_container_width=True)
    
    # تذييل الصفحة
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p><strong>المنظومة الوطنية لمواءمة المؤشرات التنموية مع الرؤية الاقتصادية 2033</strong></p>
        <p>المملكة الأردنية الهاشمية - جميع البيانات رسمية ومحدثة © 2024</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
