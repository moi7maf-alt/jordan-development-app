import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from datetime import datetime
import json

# تنسيق الصفحة
st.set_page_config(
    page_title="التطبيق التنموي التنبؤي - الأردن",
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
    .section-header {
        font-size: 1.8rem;
        color: #2c3e50;
        border-right: 5px solid #3498db;
        padding-right: 15px;
        margin: 2rem 0 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
    .prediction-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .gov-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-right: 4px solid #3498db;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# بيانات المحافظات الإحداثيات
governorates_coords = {
    "العاصمة": {"lat": 31.9539, "lon": 35.9106, "population": 4920100},
    "البلقاء": {"lat": 32.0367, "lon": 35.7272, "population": 603700},
    "الزرقاء": {"lat": 32.0608, "lon": 36.0942, "population": 1675700},
    "مأدبا": {"lat": 31.7167, "lon": 35.7933, "population": 232300},
    "إربد": {"lat": 32.5556, "lon": 35.85, "population": 2173200},
    "المفرق": {"lat": 32.3417, "lon": 36.2022, "population": 675200},
    "جرش": {"lat": 32.2808, "lon": 35.8993, "population": 291000},
    "عجلون": {"lat": 32.3333, "lon": 35.7528, "population": 216200},
    "الكرك": {"lat": 31.1833, "lon": 35.7, "population": 388700},
    "الطفيلة": {"lat": 30.8333, "lon": 35.6, "population": 118200},
    "معان": {"lat": 30.1967, "lon": 35.7344, "population": 194500},
    "العقبة": {"lat": 29.5267, "lon": 35.0078, "population": 245200}
}

# العنوان الرئيسي
st.markdown('<div class="main-header">🌍 التطبيق التنموي التنبؤي - المملكة الأردنية الهاشمية</div>', unsafe_allow_html=True)

# باقي الكود سيأتي هنا...