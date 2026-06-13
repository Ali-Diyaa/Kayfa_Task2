# app.py
import streamlit as st

st.set_page_config(
    page_title="Kayfa Academic Command Center",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS – Attrition dashboard style ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
:root {
    --blue-900: #0A2463; --blue-700: #1447A6; --blue-500: #2563EB;
    --blue-400: #3B82F6; --blue-100: #DBEAFE; --blue-50: #EFF6FF;
    --accent: #F59E0B; --white: #FFFFFF; --gray-50: #F8FAFC;
    --gray-100: #F1F5F9; --gray-200: #E2E8F0; --gray-600: #475569;
    --red-500: #EF4444; --green-500:#22C55E;
}
html, body,.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: var(--white)!important; color: #1E293B;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] { background: linear-gradient(180deg, var(--blue-900) 0%, var(--blue-700) 100%)!important; }
[data-testid="stSidebar"] * { color: var(--white)!important; }
.main.block-container { padding: 2rem 2.5rem 3rem; max-width: 1300px; }
.page-header { background: linear-gradient(135deg, var(--blue-900) 0%, var(--blue-500) 100%);
  border-radius: 16px; padding: 1.8rem 2.2rem; margin-bottom: 1.5rem; color: white; position: relative; overflow: hidden; }
.page-header::after { content:''; position:absolute; top:-60px; right:-60px; width:220px; height:220px; background:rgba(255,255,255,.06); border-radius:50%; }
.page-header h1 { font-family:'Plus Jakarta Sans',sans-serif; font-size:1.7rem; font-weight:800; margin:0; }
.page-header p { opacity:.85; margin:.3rem 0 0 0; font-size:.92rem; }
.kpi-card { background: var(--white); border: 1px solid var(--gray-200); border-radius: 14px;
  padding: 1.2rem 1.4rem; box-shadow: 0 1px 6px rgba(0,0,0,.06); transition: transform.2s, box-shadow.2s; }
.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,.1); }
.kpi-label { font-size:.78rem; font-weight:600; text-transform:uppercase; letter-spacing:.06em; color:var(--gray-600); margin-bottom:.4rem; }
.kpi-value { font-family:'Plus Jakarta Sans',sans-serif; font-size:2.0rem; font-weight:800; line-height:1; }
.kpi-delta { font-size:.8rem; color:#64748B; margin-top:.3rem; }
.section-card { background: var(--white); border: 1px solid var(--gray-200); border-radius: 14px;
  padding: 1.4rem 1.6rem; box-shadow: 0 1px 6px rgba(0,0,0,.05); margin-bottom: 1.2rem; }
.section-title { font-family:'Plus Jakarta Sans',sans-serif; font-size:1.05rem; font-weight:700;
  color:var(--blue-900); margin-bottom:.8rem; padding-bottom:.5rem; border-bottom:2px solid var(--blue-100); }
.insight-box { background: var(--blue-50); border-left: 4px solid var(--blue-500);
  border-radius: 0 10px 10px 0; padding:.9rem 1.1rem; margin:.6rem 0 1.2rem 0; font-size:.9rem; line-height:1.55; }
.rec-box { background: #FFFBEB; border-left: 4px solid var(--accent);
  border-radius: 0 10px 10px 0; padding:.9rem 1.1rem; margin:.6rem 0 1.2rem 0; font-size:.9rem; }
#MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Sidebar branding
with st.sidebar:
    st.markdown("### Kayfa")
    try: st.image("assets/kayfa_logo.jpg", use_container_width=True)
    except: st.markdown("🏢 Kayfa")
    st.caption("Academic Performance Command Center")

# Pages – uses the files in /pages
pg = st.navigation([
    st.Page("pages/1_Attendance_Grades.py", title="Attendance & Grades", icon="📈"),
    st.Page("pages/2_Assessment_Curriculum.py", title="Assessment & Curriculum", icon="📝"),
    st.Page("pages/3_Engagement_Behavior.py", title="Engagement & Behavior", icon="👥"),
    st.Page("pages/4_Cohorts_Risk.py", title="Cohorts & Risk", icon="🎯"),
], position="sidebar")
pg.run()