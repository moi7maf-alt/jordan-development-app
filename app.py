# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(
    page_title="المنظومة التحليلية للتحديات التنموية",
    page_icon="📊",
    layout="wide"
)

# بيانات المؤشرات التنموية الشاملة
@st.cache_data
def load_comprehensive_data():
    data = {
        'المحافظة': ['المفرق', 'إربد', 'الزرقاء', 'معان', 'الطفيلة', 'العقبة', 'الكرك', 'عمان', 'البلقاء', 'مأدبا', 'جرش', 'عجلون'],
        'الكثافة_السكانية': [1383, 1087, 432, 6, 78, 45, 156, 2543, 342, 287, 198, 167],
        'معدل_البطالة': [23.2, 22.2, 22.5, 23.2, 21.9, 18.5, 20.2, 17.8, 19.5, 18.9, 20.1, 19.8],
        'مؤشر_التنمية_البشرية': [0.72, 0.78, 0.75, 0.69, 0.68, 0.76, 0.74, 0.82, 0.73, 0.75, 0.76, 0.77],
        'نصيب_الفرد_من_الناتج': [4500, 5200, 5800, 3800, 3600, 6200, 4200, 7800, 4800, 5100, 4900, 5000],
        'معدل_الفقر': [18.5, 14.2, 15.8, 22.3, 24.1, 12.5, 16.8, 10.2, 15.3, 13.7, 14.5, 13.9],
        'الاستثمار_العام': [120, 180, 220, 45, 30, 320, 65, 850, 95, 75, 60, 55],
        'اللاجئين_السوريين': [142358, 78432, 45218, 12543, 8567, 9234, 15678, 125432, 23456, 18765, 13456, 11543]
    }
    return pd.DataFrame(data)

# بيانات التحديات التنموية (نفس البيانات التي قدمتها)
developmental_challenges = {
    "المفرق": {
        "التحديات_الرئيسية": [
            {
                "التحدي": "الضغط السكاني بسبب اللاجئين السوريين",
                "التأثير": "عالية جداً",
                "المؤشرات": ["زيادة السكان بنسبة 21%", "اكتظاظ المدارس بنسبة 45%", "ضغط على الخدمات الصحية بنسبة 60%"],
                "الأسباب": ["تواجد 142,358 لاجئ سوري", "تركيز اللاجئين في المجتمعات الحضرية", "نقص التمويل للبنية التحتية"]
            }
        ],
        "التصنيف_العام": "أولوية قصوى",
        "مجموع_التحديات": 8,
        "التحديات_العاجلة": 3
    },
    "معان": {
        "التحديات_الرئيسية": [
            {
                "التحدي": "التباعد الجغرافي والعزلة النسبية", 
                "التأثير": "عالية",
                "المؤشرات": ["كثافة سكانية 6 نسمة/كم²", "صعوبة الوصول للخدمات", "ارتفاع تكلفة تقديم الخدمات"],
                "الأسباب": ["مساحة شاسعة (32,832 كم²)", "تشتت التجمعات السكانية", "ضعف شبكة الطرق"]
            }
        ],
        "التصنيف_العام": "أولوية عالية", 
        "مجموع_التحديات": 6,
        "التحديات_العاجلة": 2
    }
}

def show_main_dashboard():
    st.title("🌍 المنظومة التحليلية للتحديات التنموية")
    st.markdown("**تحليل شامل للتحديات التنموية وارتباطها برؤية التحديث الاقتصادي**")
    
    df = load_comprehensive_data()
    
    # مؤشرات سريعة
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("إجمالي المحافظات", len(df), "12 محافظة")
    
    with col2:
        avg_unemployment = df['معدل_البطالة'].mean()
        st.metric("متوسط البطالة", f"{avg_unemployment:.1f}%")
    
    with col3:
        total_refugees = df['اللاجئين_السوريين'].sum()
        st.metric("إجمالي اللاجئين السوريين", f"{total_refugees:,}")
    
    with col4:
        max_poverty = df['معدل_الفقر'].max()
        st.metric("أعلى معدل فقر", f"{max_poverty:.1f}%", "الطفيلة")
    
    st.markdown("---")
    
    # التحليلات الرئيسية
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 توزيع معدلات البطالة")
        fig1 = px.bar(df, x='المحافظة', y='معدل_البطالة', 
                     color='معدل_البطالة', color_continuous_scale='reds')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("🎯 العلاقة بين التنمية البشرية والفقر")
        fig2 = px.scatter(df, x='مؤشر_التنمية_البشرية', y='معدل_الفقر',
                         size='الكثافة_السكانية', color='المحافظة',
                         hover_name='المحافظة', size_max=60)
        st.plotly_chart(fig2, use_container_width=True)
    
    # خريطة حرارية لل correlations
    st.subheader("🔗 مصفوفة الارتباط بين المؤشرات التنموية")
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()
    
    fig3 = px.imshow(corr_matrix, aspect="auto", color_continuous_scale='RdBu_r')
    st.plotly_chart(fig3, use_container_width=True)

def show_developmental_challenges_dashboard():
    st.header("🚧 التحليل التفصيلي للتحديات التنموية")
    
    # نظرة عامة
    col1, col2, col3 = st.columns(3)
    
    total_challenges = sum(gov["مجموع_التحديات"] for gov in developmental_challenges.values())
    urgent_challenges = sum(gov["التحديات_العاجلة"] for gov in developmental_challenges.values())
    
    with col1:
        st.metric("إجمالي التحديات المسجلة", total_challenges)
    
    with col2:
        st.metric("التحديات العاجلة", urgent_challenges, "تتطلب تدخلاً فورياً")
    
    with col3:
        high_priority = len([g for g in developmental_challenges.values() 
                           if "قصوى" in g["التصنيف_العام"] or "عالية" in g["التصنيف_العام"]])
        st.metric("المحافظات ذات الأولوية العالية", high_priority)
    
    # تحليل التحديات
    for governorate, data in developmental_challenges.items():
        with st.expander(f"**{governorate}** - {data['التصنيف_العام']}"):
            st.write(f"**إجمالي التحديات:** {data['مجموع_التحديات']} | **التحديات العاجلة:** {data['التحديات_العاجلة']}")
            
            for challenge in data["التحديات_الرئيسية"]:
                st.write(f"##### {challenge['التحدي']} (تأثير: {challenge['التأثير']})")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**المؤشرات:**")
                    for indicator in challenge["المؤشرات"]:
                        st.write(f"• {indicator}")
                
                with col2:
                    st.write("**الأسباب الجذرية:**")
                    for cause in challenge["الأسباب"]:
                        st.write(f"• {cause}")

def show_economic_vision_dashboard():
    st.header("🎯 رؤية التحديث الاقتصادي 2033")
    st.markdown("تحليل مؤشرات الأداء وارتباطها بالأهداف الاستراتيجية")
    
    # مؤشرات رؤية 2033
    vision_indicators = {
        'المحافظة': ['عمان', 'إربد', 'الزرقاء', 'المفرق', 'العقبة', 'معان'],
        'النمو_المستهدف': [6.5, 5.8, 6.2, 4.5, 7.2, 4.2],
        'الاستثمار_المستهدف': [1200, 650, 580, 320, 850, 280],
        'الوظائف_المستهدفة': [85000, 45000, 38000, 25000, 35000, 18000],
        'التنويع_الاقتصادي': [0.75, 0.68, 0.72, 0.58, 0.82, 0.52]
    }
    
    df_vision = pd.DataFrame(vision_indicators)
    
    # مؤشرات الأداء
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_investment = df_vision['الاستثمار_المستهدف'].sum()
        st.metric("إجمالي الاستثمار المستهدف", f"{total_investment:,} مليون دينار")
    
    with col2:
        total_jobs = df_vision['الوظائف_المستهدفة'].sum()
        st.metric("الوظائف المستهدفة", f"{total_jobs:,}")
    
    with col3:
        avg_growth = df_vision['النمو_المستهدف'].mean()
        st.metric("متوسط النمو المستهدف", f"{avg_growth:.1f}%")
    
    # تحليل تحقيق الأهداف
    st.subheader("📊 تحليل الفجوات بين الواقع والمستهدف")
    
    current_vs_target = {
        'المحافظة': ['عمان', 'إربد', 'الزرقاء', 'المفرق'],
        'البطالة_الحالية': [17.8, 22.2, 22.5, 23.2],
        'البطالة_المستهدفة': [12.0, 15.0, 16.0, 18.0],
        'النمو_الحالي': [4.2, 3.1, 3.5, 2.8],
        'النمو_المستهدف': [6.5, 5.8, 6.2, 4.5]
    }
    
    df_gap = pd.DataFrame(current_vs_target)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='البطالة الحالية', x=df_gap['المحافظة'], y=df_gap['البطالة_الحالية']))
    fig.add_trace(go.Bar(name='البطالة المستهدفة', x=df_gap['المحافظة'], y=df_gap['البطالة_المستهدفة']))
    fig.update_layout(title="فجوة البطالة بين الواقع والمستهدف")
    st.plotly_chart(fig, use_container_width=True)

def show_comparative_analysis():
    st.header("📈 التحليلات المقارنة بين المحافظات")
    
    df = load_comprehensive_data()
    
    # مقارنة متعددة الأبعاد
    st.subheader("مقارنة شاملة للمؤشرات التنموية")
    
    selected_governorates = st.multiselect(
        "اختر المحافظات للمقارنة:",
        df['المحافظة'].unique(),
        default=['المفرق', 'عمان', 'العقبة']
    )
    
    if selected_governorates:
        comparison_df = df[df['المحافظة'].isin(selected_governorates)]
        
        # رسم بياني راداري للمقارنة
        categories = ['معدل_البطالة', 'مؤشر_التنمية_البشرية', 'نصيب_الفرد_من_الناتج', 'معدل_الفقر']
        
        fig = go.Figure()
        
        for gov in selected_governorates:
            gov_data = comparison_df[comparison_df['المحافظة'] == gov]
            values = [gov_data[c].values[0] for c in categories]
            
            # تسوية البيانات للمقارنة
            normalized_values = []
            for i, val in enumerate(values):
                if categories[i] in ['معدل_البطالة', 'معدل_الفقر']:
                    normalized_values.append(1 - (val / 100))
                else:
                    normalized_values.append(val / max(comparison_df[categories[i]]))
            
            fig.add_trace(go.Scatterpolar(
                r=normalized_values,
                theta=categories,
                fill='toself',
                name=gov
            ))
        
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                         showlegend=True,
                         title="المقارنة النسبية الشاملة")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # جدول المقارنة التفصيلي
        st.subheader("جدول المقارنة التفصيلي")
        st.dataframe(comparison_df.set_index('المحافظة'), use_container_width=True)

def main():
    st.sidebar.title("📋 التقارير التحليلية")
    
    report_type = st.sidebar.selectbox(
        "اختر نوع التقرير:",
        [
            "اللوحة الرئيسية",
            "رؤية التحديث الاقتصادي", 
            "التحديات التنموية",
            "التحليلات المقارنة",
            "التقارير التفصيلية"
        ]
    )
    
    if report_type == "اللوحة الرئيسية":
        show_main_dashboard()
    elif report_type == "رؤية التحديث الاقتصادي":
        show_economic_vision_dashboard()
    elif report_type == "التحديات التنموية":
        show_developmental_challenges_dashboard()
    elif report_type == "التحليلات المقارنة":
        show_comparative_analysis()
    elif report_type == "التقارير التفصيلية":
        st.info("سيتم إضافة التقارير التفصيلية في التحديثات القادمة")
    
    # تذييل الصفحة
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **المصادر:**
    - وزارة التخطيط والتعاون الدولي
    - دائرة الإحصاءات العامة
    - تقارير البنك الدولي
    - رؤية التحديث الاقتصادي 2033
    """)

if __name__ == "__main__":
    main()
