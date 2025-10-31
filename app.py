# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# تكوين الصفحة
st.set_page_config(
    page_title="المنظومة الوطنية للتحليل التنموي - الأردن",
    page_icon="🇯🇴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f3a93;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<div class="main-header">🌍 المنظومة الوطنية للتحليل التنموي - المملكة الأردنية الهاشمية</div>', unsafe_allow_html=True)
    
    # الشريط الجانبي
    st.sidebar.title("🔄 قائمة التقارير")
    report_type = st.sidebar.selectbox(
        "اختر نوع التقرير",
        [
            "اللوحة الرئيسية",
            "رؤية التحديث الاقتصادي 2033", 
            "التحديات التنموية",
            "تأثير اللاجئين",
            "تقارير المحافظات",
            "المقارنات التنموية"
        ]
    )
    
    if report_type == "اللوحة الرئيسية":
        show_main_dashboard()
    elif report_type == "رؤية التحديث الاقتصادي 2033":
        show_economic_vision_dashboard()
    elif report_type == "التحديات التنموية":
        show_developmental_challenges_dashboard()
    elif report_type == "تأثير اللاجئين":
        show_refugee_impact_dashboard()
    elif report_type == "تقارير المحافظات":
        show_governorate_reports()
    elif report_type == "المقارنات التنموية":
        show_comparative_analysis()

def show_main_dashboard():
    st.header("📊 اللوحة الرئيسية - المؤشرات التنموية الوطنية")
    
    # بيانات المحافظات الأساسية
    governorates_data = {
        "العاصمة": {"population": 4920100, "unemployment": 20.7, "illiteracy": 3.55, "development_index": 0.78},
        "إربد": {"population": 2173200, "unemployment": 22.2, "illiteracy": 3.5, "development_index": 0.72},
        "الزرقاء": {"population": 1675700, "unemployment": 22.5, "illiteracy": 4.55, "development_index": 0.68},
        "المفرق": {"population": 675200, "unemployment": 23.2, "illiteracy": 8.15, "development_index": 0.55},
        "البلقاء": {"population": 603700, "unemployment": 22.1, "illiteracy": 7.35, "development_index": 0.65},
        "مأدبا": {"population": 232300, "unemployment": 20.5, "illiteracy": 6.35, "development_index": 0.70},
        "الكرك": {"population": 388700, "unemployment": 20.2, "illiteracy": 4.8, "development_index": 0.73},
        "معان": {"population": 194500, "unemployment": 23.2, "illiteracy": 8.7, "development_index": 0.58},
        "العقبة": {"population": 245200, "unemployment": 17.3, "illiteracy": 7.25, "development_index": 0.75},
        "جرش": {"population": 291000, "unemployment": 20.9, "illiteracy": 4.8, "development_index": 0.71},
        "عجلون": {"population": 216200, "unemployment": 21.2, "illiteracy": 5.3, "development_index": 0.69},
        "الطفيلة": {"population": 118200, "unemployment": 21.9, "illiteracy": 7.6, "development_index": 0.62}
    }
    
    # مؤشرات رئيسية
    col1, col2, col3, col4 = st.columns(4)
    
    total_population = sum(gov["population"] for gov in governorates_data.values())
    avg_unemployment = np.mean([gov["unemployment"] for gov in governorates_data.values()])
    avg_illiteracy = np.mean([gov["illiteracy"] for gov in governorates_data.values()])
    avg_development = np.mean([gov["development_index"] for gov in governorates_data.values()])
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("إجمالي السكان", f"{total_population:,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("متوسط البطالة", f"{avg_unemployment:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("متوسط الأمية", f"{avg_illiteracy:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("مؤشر التنمية", f"{avg_development:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # رسوم بيانية
    col1, col2 = st.columns(2)
    
    with col1:
        gov_names = list(governorates_data.keys())
        unemployment_rates = [gov["unemployment"] for gov in governorates_data.values()]
        fig = px.bar(x=gov_names, y=unemployment_rates, title="معدلات البطالة بالمحافظات")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        development_indices = [gov["development_index"] for gov in governorates_data.values()]
        fig = px.bar(x=gov_names, y=development_indices, title="مؤشرات التنمية المركبة")
        st.plotly_chart(fig, use_container_width=True)

def show_economic_vision_dashboard():
    st.header("🎯 رؤية التحديث الاقتصادي 2033")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; color: white; text-align: center;'>
        <h2>رؤية التحديث الاقتصادي 2033</h2>
        <h3>تحويل الأردن إلى مركز إقليمي للاستثمار والابتكار</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # مؤشرات الأداء
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("معدل النمو الاقتصادي", "2.7%", "5.5%")
    with col2:
        st.metric("معدل البطالة", "21.4%", "12%")
    with col3:
        st.metric("معدل الأمية", "5.1%", "3%")
    
    st.markdown("---")
    
    st.subheader("المحاور الاستراتيجية")
    
    pillars = {
        "تحفيز النمو الاقتصادي": [
            "رفع معدل النمو الاقتصادي إلى 5.5%",
            "خفض معدل البطالة إلى 12%",
            "جذب استثمارات أجنبية مباشرة بقيمة 10 مليارات دولار"
        ],
        "تعزيز رأس المال البشري": [
            "خفض معدل الأمية إلى 3%",
            "رفع نسبة الملتحقين بالتعليم المهني إلى 25%",
            "تحسين مخرجات التعليم لمواءمة سوق العمل"
        ]
    }
    
    for pillar, goals in pillars.items():
        with st.expander(f"**{pillar}**"):
            for goal in goals:
                st.write(f"• {goal}")

def show_developmental_challenges_dashboard():
    st.header("🚧 التحديات التنموية في المحافظات")
    
    # بيانات التحديات
    challenges_data = {
        "المفرق": {"التحديات": 8, "العاجلة": 3, "التصنيف": "أولوية قصوى"},
        "معان": {"التحديات": 6, "العاجلة": 2, "التصنيف": "أولوية عالية"},
        "الطفيلة": {"التحديات": 5, "العاجلة": 2, "التصنيف": "أولوية متوسطة-عالية"},
        "إربد": {"التحديات": 5, "العاجلة": 2, "التصنيف": "أولوية عالية"}
    }
    
    # نظرة عامة
    col1, col2, col3 = st.columns(3)
    
    total_challenges = sum(gov["التحديات"] for gov in challenges_data.values())
    urgent_challenges = sum(gov["العاجلة"] for gov in challenges_data.values())
    
    with col1:
        st.metric("إجمالي التحديات المسجلة", total_challenges)
    with col2:
        st.metric("التحديات العاجلة", urgent_challenges)
    with col3:
        st.metric("أكثر المحافظات تحدياً", "المفرق", "8 تحديات")
    
    st.markdown("---")
    
    # تفاصيل التحديات
    for governorate, data in challenges_data.items():
        with st.expander(f"**{governorate}** - {data['التصنيف']}"):
            st.write(f"**إجمالي التحديات:** {data['التحديات']}")
            st.write(f"**التحديات العاجلة:** {data['العاجلة']}")
            
            if governorate == "المفرق":
                st.write("**أهم التحديات:**")
                st.write("• الضغط السكاني بسبب اللاجئين السوريين")
                st.write("• ارتفاع معدلات البطالة والأمية")
                st.write("• ضعف البنية التحتية الخدمية")

def show_refugee_impact_dashboard():
    st.header("📊 تأثير اللاجئين السوريين")
    
    refugee_data = {
        "المفرق": {"refugees": 142358, "percentage": 21.1},
        "العاصمة": {"refugees": 121845, "percentage": 2.5},
        "إربد": {"refugees": 78432, "percentage": 3.6},
        "الزرقاء": {"refugees": 65218, "percentage": 3.9}
    }
    
    total_refugees = sum(gov["refugees"] for gov in refugee_data.values())
    highest_refugee_gov = max(refugee_data.items(), key=lambda x: x[1]["percentage"])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("إجمالي اللاجئين المسجلين", f"{total_refugees:,}")
    with col2:
        st.metric("أعلى نسبة لاجئين", f"{highest_refugee_gov[1]['percentage']}%", highest_refugee_gov[0])
    with col3:
        st.metric("لاجئين في المجتمعات الحضرية", "83%")
    
    st.markdown("---")
    
    # رسم بياني
    gov_names = list(refugee_data.keys())
    refugee_percentages = [gov["percentage"] for gov in refugee_data.values()]
    
    fig = px.bar(x=gov_names, y=refugee_percentages, title="نسبة اللاجئين إلى السكان المحليين (%)")
    st.plotly_chart(fig, use_container_width=True)

def show_governorate_reports():
    st.header("📋 تقارير المحافظات التفصيلية")
    
    governorates_data = {
        "العاصمة": {"population": 4920100, "unemployment": 20.7, "illiteracy": 3.55, "development_index": 0.78},
        "المفرق": {"population": 675200, "unemployment": 23.2, "illiteracy": 8.15, "development_index": 0.55},
        "إربد": {"population": 2173200, "unemployment": 22.2, "illiteracy": 3.5, "development_index": 0.72}
    }
    
    selected_gov = st.selectbox("اختر المحافظة", list(governorates_data.keys()))
    
    if selected_gov:
        gov_data = governorates_data[selected_gov]
        
        st.subheader(f"تقرير تنموي شامل - محافظة {selected_gov}")
        
        # المؤشرات الرئيسية
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("عدد السكان", f"{gov_data['population']:,}")
            st.metric("مؤشر التنمية", f"{gov_data['development_index']}")
        
        with col2:
            st.metric("معدل البطالة", f"{gov_data['unemployment']}%")
        
        with col3:
            st.metric("معدل الأمية", f"{gov_data['illiteracy']}%")
        
        st.markdown("---")
        
        # توصيات
        st.subheader("🎯 التوصيات التنموية")
        
        if selected_gov == "المفرق":
            recommendations = [
                "توسعة البنية التحتية التعليمية والصحية لاستيعاب اللاجئين",
                "برامج تشغيل مستهدفة للشباب والخريجين",
                "حملات محو أمية مكثفة في المناطق الأكثر احتياجاً",
                "تحسين خدمات البنية التحتية في المناطق الحضرية المكتظة"
            ]
        else:
            recommendations = [
                "تحسين جودة الخدمات التعليمية والصحية",
                "برامج تنمية اقتصادية محلية",
                "تعزيز المشاركة الاقتصادية للشباب",
                "تحسين البنية التحتية الخدمية"
            ]
        
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")

def show_comparative_analysis():
    st.header("📈 المقارنات التنموية بين المحافظات")
    
    governorates_data = {
        "العاصمة": {"population": 4920100, "unemployment": 20.7, "illiteracy": 3.55, "development_index": 0.78},
        "إربد": {"population": 2173200, "unemployment": 22.2, "illiteracy": 3.5, "development_index": 0.72},
        "الزرقاء": {"population": 1675700, "unemployment": 22.5, "illiteracy": 4.55, "development_index": 0.68},
        "المفرق": {"population": 675200, "unemployment": 23.2, "illiteracy": 8.15, "development_index": 0.55}
    }
    
    selected_indicators = st.multiselect(
        "اختر المؤشرات للمقارنة",
        ["البطالة", "الأمية", "مؤشر التنمية"],
        default=["البطالة", "الأمية"]
    )
    
    if selected_indicators:
        comparison_data = []
        for gov_name, gov_data in governorates_data.items():
            row = {"المحافظة": gov_name}
            if "البطالة" in selected_indicators:
                row["البطالة"] = gov_data["unemployment"]
            if "الأمية" in selected_indicators:
                row["الأمية"] = gov_data["illiteracy"]
            if "مؤشر التنمية" in selected_indicators:
                row["مؤشر التنمية"] = gov_data["development_index"]
            comparison_data.append(row)
        
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
