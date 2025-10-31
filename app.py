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
    page_title="المنظومة الوطنية للذكاء التنموي - رؤية 2033",
    page_icon="🏛️",
    layout="wide"
)

# التصميم المخصص للجهات الحكومية
st.markdown("""
<style>
    .main-header {
        font-size: 3.2rem;
        color: #1a5276;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        background: linear-gradient(135deg, #1a5276 0%, #2e86ab 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .executive-dashboard {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        margin: 1.5rem 0;
        border: 2px solid #1a5276;
    }
    .priority-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-left: 6px solid #e74c3c;
        margin: 1rem 0;
    }
    .kpi-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .warning-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        border: 2px solid #c23616;
    }
    .data-source {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-right: 4px solid #2e86ab;
        font-size: 0.9rem;
        color: #555;
    }
</style>
""", unsafe_allow_html=True)

# البيانات الحقيقية المحدثة من المصادر الرسمية
@st.cache_data
def load_official_data():
    """تحميل البيانات الرسمية من المصادر الحكومية"""
    
    # بيانات الكثافة السكانية المحدثة (2024)
    population_data = {
        'المحافظة': ['عمان', 'المفرق', 'إربد', 'الزرقاء', 'البلقاء', 'مأدبا', 'معان', 'الكرك', 'جرش', 'عجلون', 'العقبة', 'الطفيلة'],
        'التعداد_2024': [4920100, 675200, 2173200, 1675700, 603700, 232300, 194500, 388700, 291000, 216200, 245200, 118200],
        'المساحة_كم2': [7579, 26551, 1572, 4761, 1120, 940, 32832, 3495, 410, 420, 6905, 2209],
        'الكثافة_2024': [649.2, 25.4, 1383.2, 352.0, 539.2, 247.3, 5.9, 111.2, 709.8, 514.8, 35.5, 53.5],
        'نمو_سكاني_2024': [2.1, 2.8, 2.3, 2.4, 2.2, 2.5, 1.8, 2.0, 2.6, 2.4, 3.2, 1.9]
    }
    
    # بيانات البطالة الرسمية (2024)
    unemployment_data = {
        'المحافظة': ['عمان', 'المفرق', 'إربد', 'الزرقاء', 'البلقاء', 'مأدبا', 'معان', 'الكرك', 'جرش', 'عجلون', 'العقبة', 'الطفيلة'],
        'البطالة_2024': [20.7, 23.2, 22.2, 22.5, 22.1, 20.5, 23.2, 20.2, 20.9, 21.2, 17.3, 21.9],
        'بطالة_الذكور': [16.0, 23.0, 20.3, 19.3, 20.8, 17.6, 21.3, 16.3, 17.1, 19.0, 15.9, 19.7],
        'بطالة_الإناث': [35.2, 24.1, 30.6, 39.3, 26.2, 29.7, 29.3, 29.4, 36.2, 28.5, 26.7, 28.0],
        'الفجوة_النوعية': [19.2, 1.1, 10.3, 20.0, 5.4, 12.1, 8.0, 13.1, 19.1, 9.5, 10.8, 8.3]
    }
    
    # بيانات المشاركة الاقتصادية (2024)
    economic_participation = {
        'المحافظة': ['عمان', 'المفرق', 'إربد', 'الزرقاء', 'البلقاء', 'مأدبا', 'معان', 'الكرك', 'جرش', 'عجلون', 'العقبة', 'الطفيلة'],
        'المشاركة_الاقتصادية_2024': [34.9, 35.4, 33.4, 31.4, 33.8, 34.2, 34.5, 38.0, 35.7, 33.1, 28.8, 37.4],
        'مشاركة_الذكور': [53.4, 55.5, 54.0, 52.6, 52.3, 51.7, 52.4, 54.0, 56.1, 50.7, 51.1, 56.6],
        'مشاركة_الإناث': [16.9, 14.6, 12.4, 10.2, 15.8, 16.5, 16.2, 22.4, 14.4, 15.4, 7.6, 19.0],
        'فجوة_المشاركة': [36.5, 40.9, 41.6, 42.4, 36.5, 35.2, 36.2, 31.6, 41.7, 35.3, 43.5, 37.6]
    }
    
    # بيانات التعليم (2024)
    education_data = {
        'المحافظة': ['عمان', 'المفرق', 'إربد', 'الزرقاء', 'البلقاء', 'مأدبا', 'معان', 'الكرك', 'جرش', 'عجلون', 'العقبة', 'الطفيلة'],
        'معدل_الأمية_2024': [3.55, 8.15, 3.5, 4.55, 7.35, 6.35, 8.7, 4.8, 4.8, 5.3, 7.25, 7.6]
    }
    
    # بيانات الصحة (2024)
    health_data = {
        'المحافظة': ['عمان', 'المفرق', 'إربد', 'الزرقاء', 'البلقاء', 'مأدبا', 'معان', 'الكرك', 'جرش', 'عجلون', 'العقبة', 'الطفيلة'],
        'وفيات_الرضع_2023': [19, 4, 10, 15, 21, 14, 4, 5, 10, 22, 9, 9],
        'كثافة_الأطباء': [3.2, 1.2, 2.1, 1.8, 1.5, 1.9, 0.8, 1.4, 1.7, 1.8, 2.8, 1.1]
    }
    
    # بيانات التزود المائي (2023)
    water_data = {
        'المحافظة': ['عمان', 'المفرق', 'إربد', 'الزرقاء', 'البلقاء', 'مأدبا', 'معان', 'الكرك', 'جرش', 'عجلون', 'العقبة', 'الطفيلة'],
        'حصة_الفرد_المائية_2023': [125.4, 150.3, 77.6, 103.0, 242.5, 134.5, 222.2, 157.8, 84.3, 85.1, 302.9, 202.8],
        'العجز_المائي_٪': [14.0, 15.6, 23.3, 17.9, 15.8, 18.2, 22.2, 21.4, 25.0, 28.6, 9.5, 25.0]
    }
    
    # بيانات النفايات الصلبة (2022)
    waste_data = {
        'المحافظة': ['عمان', 'المفرق', 'إربد', 'الزرقاء', 'البلقاء', 'مأدبا', 'معان', 'الكرك', 'جرش', 'عجلون', 'العقبة', 'الطفيلة'],
        'النفايات_الصلبة_2022': [1360527.5, 259918.7, 865147.3, 502484.6, 492095.1, 123308.1, 31218.9, 184386, 104342.8, 112801, 23671, 122260.4],
        'معدل_إنتاج_الفرد_2022': [0.8, 1.1, 1.1, 0.9, 2.3, 1.5, 0.5, 1.3, 1.0, 1.5, 0.3, 2.9]
    }
    
    # بيانات الثروة الحيوانية (2023)
    livestock_data = {
        'المحافظة': ['عمان', 'المفرق', 'إربد', 'الزرقاء', 'البلقاء', 'مأدبا', 'معان', 'الكرك', 'جرش', 'عجلون', 'العقبة', 'الطفيلة'],
        'الأغنام_2023': [616666, 995613, 247425, 389140, 152982, 177055, 277168, 395619, 19218, 21502, 63160, 116036],
        'الماعز_2023': [87689, 91451, 68357, 87429, 65506, 47792, 119020, 96523, 39852, 43405, 132505, 28799],
        'الأبقار_2023': [10604, 16026, 15335, 40010, 1494, 1071, 94, 127, 4301, 1132, 0, 102]
    }
    
    # بيانات المحاصيل الزراعية (2023)
    agriculture_data = {
        'المحافظة': ['عمان', 'المفرق', 'إربد', 'الزرقاء', 'البلقاء', 'مأدبا', 'معان', 'الكرك', 'جرش', 'عجلون', 'العقبة', 'الطفيلة'],
        'محاصيل_حقلية_2023': [164749.4, 94490.3, 127058.6, 41331.2, 22619.3, 42368.3, 77704.5, 216403.4, 8057.6, 15126.5, 2766.3, 33496.5],
        'أشجار_مثمرة_2023': [76745.6, 148569.6, 242556.6, 72723.4, 75598.2, 23511.5, 24072.6, 32516.4, 72972.9, 40377.8, 13752.1, 10286.7]
    }
    
    # دمج جميع البيانات
    dfs = [
        pd.DataFrame(population_data),
        pd.DataFrame(unemployment_data),
        pd.DataFrame(economic_participation),
        pd.DataFrame(education_data),
        pd.DataFrame(health_data),
        pd.DataFrame(water_data),
        pd.DataFrame(waste_data),
        pd.DataFrame(livestock_data),
        pd.DataFrame(agriculture_data)
    ]
    
    # الدمج التدريجي
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, on='المحافظة', how='left')
    
    return merged_df

def create_executive_dashboard():
    """لوحة التحكم التنفيذية لرئيس لجنة التخطيط"""
    
    st.markdown('<div class="main-header">🏛️ المنظومة الوطنية للذكاء التنموي - رؤية 2033</div>', unsafe_allow_html=True)
    
    # بطاقة التنفيذي
    st.markdown("""
    <div class="executive-dashboard">
        <h3>📋 لوحة تحكم رئيس لجنة التخطيط التنموي</h3>
        <p>منظومة متكاملة لرصد وتحليل ومتابعة المؤشرات التنموية على مستوى المحافظات</p>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_official_data()
    
    # مؤشرات القيادة السريعة
    st.subheader("🎯 المؤشرات القيادية الفورية")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_population = df['التعداد_2024'].sum()
        st.metric("إجمالي السكان", f"{total_population:,}", "11.7 مليون نسمة")
    
    with col2:
        avg_unemployment = df['البطالة_2024'].mean()
        st.metric("متوسط البطالة", f"{avg_unemployment:.1f}%", "21.4% المعدل الوطني")
    
    with col3:
        avg_female_unemployment = df['بطالة_الإناث'].mean()
        st.metric("بطالة الإناث", f"{avg_female_unemployment:.1f}%", "تحديد تنموي رئيسي")
    
    with col4:
        total_livestock = df['الأغنام_2023'].sum() + df['الماعز_2023'].sum() + df['الأبقار_2023'].sum()
        st.metric("القطيع الحيواني", f"{total_livestock:,}", "رأس ماشية")
    
    st.markdown("---")
    
    # خرائط حرارية للمؤشرات الاستراتيجية
    st.subheader("🗺️ الخرائط الحرارية للمؤشرات الاستراتيجية")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # خريطة البطالة
        fig1 = px.choropleth(
            df,
            locations='المحافظة',
            locationmode='country names',
            color='البطالة_2024',
            color_continuous_scale='RdYlGn_r',
            title='توزيع معدلات البطالة 2024',
            scope='asia'
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # خريطة الكثافة السكانية
        fig2 = px.choropleth(
            df,
            locations='المحافظة',
            locationmode='country names',
            color='الكثافة_2024',
            color_continuous_scale='Blues',
            title='الكثافة السكانية 2024 (فرد/كم²)',
            scope='asia'
        )
        st.plotly_chart(fig2, use_container_width=True)

def early_warning_system():
    """نظام الإنذار المبكر المتقدم"""
    
    st.header("🚨 نظام الإنذار المبكر للمؤشرات الحرجة")
    
    df = load_official_data()
    
    # تحليل المخاطر
    risk_analysis = []
    
    for _, row in df.iterrows():
        risk_score = 0
        warnings = []
        
        # تحليل البطالة
        if row['البطالة_2024'] > 22:
            risk_score += 3
            warnings.append(f"🚨 بطالة مرتفعة ({row['البطالة_2024']}%)")
        
        # تحليل فجوة البطالة النوعية
        if row['الفجوة_النوعية'] > 15:
            risk_score += 2
            warnings.append(f"⚠️ فجوة نوعية كبيرة ({row['الفجوة_النوعية']}%)")
        
        # تحليل المشاركة الاقتصادية للإناث
        if row['مشاركة_الإناث'] < 12:
            risk_score += 2
            warnings.append(f"⚠️ مشاركة إناث منخفضة ({row['مشاركة_الإناث']}%)")
        
        # تحليل الأمية
        if row['معدل_الأمية_2024'] > 7:
            risk_score += 1
            warnings.append(f"📚 أمية مرتفعة ({row['معدل_الأمية_2024']}%)")
        
        # تحليل العجز المائي
        if 'العجز_المائي_٪' in row and row['العجز_المائي_٪'] > 20:
            risk_score += 2
            warnings.append(f"💧 عجز مائي حاد ({row['العجز_المائي_٪']}%)")
        
        risk_analysis.append({
            'المحافظة': row['المحافظة'],
            'مستوى_الخطر': risk_score,
            'الإنذارات': warnings,
            'عدد_الإنذارات': len(warnings)
        })
    
    risk_df = pd.DataFrame(risk_analysis)
    
    # عرض الإنذارات
    st.subheader("🔔 الإنذارات النشطة حسب المحافظة")
    
    high_risk = risk_df[risk_df['عدد_الإنذارات'] > 0].sort_values('مستوى_الخطر', ascending=False)
    
    for _, province in high_risk.iterrows():
        with st.expander(f"🚩 {province['المحافظة']} - مستوى الخطر: {province['مستوى_الخطر']}/10", expanded=True):
            for warning in province['الإنذارات']:
                st.write(f"• {warning}")
            
            # توصيات علاجية مخصصة
            st.info("**التوصيات العلاجية المطلوبة:**")
            
            if "بطالة مرتفعة" in str(province['الإنذارات']):
                st.write("• تطوير برامج تشغيل مستهدفة بالمحافظة")
                st.write("• تحفيز الاستثمار في القطاعات المنتجة للوظائف")
                st.write("• تنمية المشاريع الصغيرة والمتوسطة")
            
            if "فجوة نوعية" in str(province['الإنذارات']):
                st.write("• برامج تمكين اقتصادي للمرأة")
                st.write("• حاضنات أعمال نسائية")
                st.write("• توفير بيئة عمل صديقة للمرأة")
            
            if "عجز مائي" in str(province['الإنذارات']):
                st.write("• ترشيد استهلاك المياه")
                st.write("• تطوير مشاريع جمع مياه الأمطار")
                st.write("• تحسين كفاءة شبكات التوزيع")

def strategic_planning_insights():
    """رؤى التخطيط الاستراتيجي"""
    
    st.header("🎯 رؤى التخطيط الاستراتيجي وأولويات التدخل")
    
    df = load_official_data()
    
    # حساب مؤشرات الأولوية
    priority_indicators = []
    
    for _, row in df.iterrows():
        # مؤشر مركب للاحتياج التنموي
        development_need = (
            row['البطالة_2024'] * 0.3 +
            row['بطالة_الإناث'] * 0.2 +
            (row['معدل_الأمية_2024'] * 2) * 0.15 +
            (100 - row['مشاركة_الإناث']) * 0.2
        )
        
        # إضافة العجز المائي إذا موجود
        if 'العجز_المائي_٪' in row:
            development_need += row['العجز_المائي_٪'] * 0.15
        
        priority_indicators.append({
            'المحافظة': row['المحافظة'],
            'مؤشر_الاحتياج': development_need,
            'البطالة': row['البطالة_2024'],
            'بطالة_الإناث': row['بطالة_الإناث'],
            'المشاركة_الاقتصادية': row['المشاركة_الاقتصادية_2024'],
            'الأمية': row['معدل_الأمية_2024']
        })
    
    priority_df = pd.DataFrame(priority_indicators)
    
    # عرض أولويات التدخل
    st.subheader("📊 أولويات التدخل التنموي حسب المحافظات")
    
    fig = px.bar(
        priority_df.sort_values('مؤشر_الاحتياج', ascending=False),
        x='مؤشر_الاحتياج',
        y='المحافظة',
        orientation='h',
        title='أولويات التدخل التنموي بناءً على مؤشر الاحتياج المركب',
        color='مؤشر_الاحتياج',
        color_continuous_scale='RdYlGn_r'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # تحليل التكتلات التنموية
    st.subheader("🏗️ التكتلات التنموية المقترحة")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**التكتل الشمالي**")
        st.write("• إربد، جرش، عجلون، المفرق")
        st.write("• التركيز: الزراعة، السياحة، الصناعات التحويلية")
        northern_data = df[df['المحافظة'].isin(['إربد', 'جرش', 'عجلون', 'المفرق'])]
        avg_unemployment = northern_data['البطالة_2024'].mean()
        st.metric("متوسط البطالة", f"{avg_unemployment:.1f}%")
    
    with col2:
        st.markdown("**التكتل الأوسط**")
        st.write("• عمان، الزرقاء، البلقاء، مأدبا")
        st.write("• التركيز: الخدمات، التقنية، الصناعات المتقدمة")
        central_data = df[df['المحافظة'].isin(['عمان', 'الزرقاء', 'البلقاء', 'مأدبا'])]
        avg_unemployment = central_data['البطالة_2024'].mean()
        st.metric("متوسط البطالة", f"{avg_unemployment:.1f}%")
    
    with col3:
        st.markdown("**التكتل الجنوبي**")
        st.write("• الكرك، الطفيلة، معان، العقبة")
        st.write("• التركيز: السياحة، التعدين، الطاقة المتجددة")
        southern_data = df[df['المحافظة'].isin(['الكرك', 'الطفيلة', 'معان', 'العقبة'])]
        avg_unemployment = southern_data['البطالة_2024'].mean()
        st.metric("متوسط البطالة", f"{avg_unemployment:.1f}%")

def sectoral_analysis():
    """التحليل القطاعي المتكامل"""
    
    st.header("🏭 التحليل القطاعي المتكامل")
    
    df = load_official_data()
    
    # تحليل القطاع الزراعي
    st.subheader("🌾 القطاع الزراعي والثروة الحيوانية")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # الثروة الحيوانية
        fig1 = px.bar(
            df,
            x='المحافظة',
            y=['الأغنام_2023', 'الماعز_2023', 'الأبقار_2023'],
            title='توزيع الثروة الحيوانية 2023',
            barmode='stack'
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # المحاصيل الزراعية
        fig2 = px.bar(
            df,
            x='المحافظة',
            y=['محاصيل_حقلية_2023', 'أشجار_مثمرة_2023'],
            title='الهيكل الزراعي 2023',
            barmode='group'
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # تحليل القطاع الصحي
    st.subheader("🏥 القطاع الصحي")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # وفيات الرضع
        fig3 = px.bar(
            df.sort_values('وفيات_الرضع_2023'),
            x='المحافظة',
            y='وفيات_الرضع_2023',
            title='معدلات وفيات الرضع 2023',
            color='وفيات_الرضع_2023',
            color_continuous_scale='Viridis_r'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # كثافة الأطباء
        fig4 = px.bar(
            df.sort_values('كثافة_الأطباء', ascending=False),
            x='المحافظة',
            y='كثافة_الأطباء',
            title='كثافة الأطباء (طبيب/1000 نسمة)',
            color='كثافة_الأطباء'
        )
        st.plotly_chart(fig4, use_container_width=True)

def comprehensive_reports():
    """التقارير الشاملة للمحافظات"""
    
    st.header("📋 التقارير التنموية الشاملة للمحافظات")
    
    df = load_official_data()
    
    # اختيار المحافظة
    selected_province = st.selectbox(
        "اختر المحافظة لعرض التقرير التفصيلي:",
        df['المحافظة'].unique()
    )
    
    province_data = df[df['المحافظة'] == selected_province].iloc[0]
    
    st.markdown(f"## 📊 التقرير التنموي الشامل لمحافظة {selected_province}")
    
    # المؤشرات الأساسية
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("التعداد السكاني", f"{province_data['التعداد_2024']:,}")
    
    with col2:
        st.metric("معدل البطالة", f"{province_data['البطالة_2024']}%")
    
    with col3:
        st.metric("المشاركة الاقتصادية", f"{province_data['المشاركة_الاقتصادية_2024']}%")
    
    with col4:
        st.metric("معدل الأمية", f"{province_data['معدل_الأمية_2024']}%")
    
    # تحليل مفصل
    st.subheader("📈 التحليل التفصيلي")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # مؤشرات سوق العمل
        labor_data = {
            'المؤشر': ['البطالة الإجمالية', 'بطالة الذكور', 'بطالة الإناث', 'الفجوة النوعية'],
            'القيمة': [
                province_data['البطالة_2024'],
                province_data['بطالة_الذكور'],
                province_data['بطالة_الإناث'],
                province_data['الفجوة_النوعية']
            ]
        }
        fig1 = px.bar(pd.DataFrame(labor_data), x='المؤشر', y='القيمة', 
                     title='مؤشرات سوق العمل')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # الثروة الحيوانية
        livestock_data = {
            'النوع': ['الأغنام', 'الماعز', 'الأبقار'],
            'العدد': [
                province_data['الأغنام_2023'],
                province_data['الماعز_2023'],
                province_data['الأبقار_2023']
            ]
        }
        fig2 = px.pie(pd.DataFrame(livestock_data), values='العدد', names='النوع',
                     title='توزيع الثروة الحيوانية')
        st.plotly_chart(fig2, use_container_width=True)

def main():
    """الدالة الرئيسية"""
    
    # الشريط الجانبي
    st.sidebar.title("🏛️ قائمة القيادة")
    
    menu_option = st.sidebar.selectbox(
        "اختر لوحة التحكم:",
        [
            "اللوحة التنفيذية",
            "نظام الإنذار المبكر", 
            "التخطيط الاستراتيجي",
            "التحليل القطاعي",
            "التقارير الشاملة",
            "معلومات النظام"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 مصادر البيانات المعتمدة:")
    st.sidebar.markdown("""
    - دائرة الإحصاءات العامة
    - وزارة التخطيط والتعاون الدولي  
    - وزارة العمل
    - وزارة التربية والتعليم
    - وزارة الصحة
    - وزارة المياه والري
    - وزارة الزراعة
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🕒 آخر تحديث:** 30 سبتمبر 2024")
    st.sidebar.markdown("**📈 إصدار البيانات:** الرسمية 2024")
    
    # توجيه حسب الاختيار
    if menu_option == "اللوحة التنفيذية":
        create_executive_dashboard()
    elif menu_option == "نظام الإنذار المبكر":
        early_warning_system()
    elif menu_option == "التخطيط الاستراتيجي":
        strategic_planning_insights()
    elif menu_option == "التحليل القطاعي":
        sectoral_analysis()
    elif menu_option == "التقارير الشاملة":
        comprehensive_reports()
    elif menu_option == "معلومات النظام":
        st.header("ℹ️ معلومات النظام")
        st.info("""
        ### 🏛️ المنظومة الوطنية للذكاء التنموي
        
        **المميزات:**
        - تحليل تنموي متكامل للمحافظات
        - نظام إنذار مبكر للمؤشرات الحرجة
        - تخطيط استراتيجي قائم على البيانات
        - تحليل قطاعي شامل
        - تقارير تفصيلية للمحافظات
        
        **البيانات:**
        - جميع البيانات رسمية ومؤكدة
        - أحدث الإصدارات 2024
        - مصادر حكومية معتمدة
        
        **التقنيات:**
        - Streamlit للواجهة التفاعلية
        - Plotly للرسوم البيانية
        - Pandas لتحليل البيانات
        """)
    
    # تذييل الصفحة
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p><b>المنظومة الوطنية للذكاء التنموي - المملكة الأردنية الهاشمية</b></p>
        <p>© 2024 - تم التطوير بناءً على البيانات الرسمية - جميع الحقوق محفوظة</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
