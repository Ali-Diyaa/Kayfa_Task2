import streamlit as st

st.set_page_config(page_title="Kayfa Academic Command Center", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=DM+Sans:wght@400;500&display=swap');
html, body,.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
  background-color: #FFFFFF!important; color: #1E293B!important;
  font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0A2463 0%, #1447A6 100%)!important; }
[data-testid="stSidebar"] * { color: #FFFFFF!important; }
.main.block-container { padding: 2rem 2.5rem; max-width: 1280px; }
.page-header { background: linear-gradient(135deg, #0A2463 0%, #2563EB 100%); border-radius: 16px; padding: 1.5rem 1.8rem; margin-bottom: 1.2rem; color: white; }
.page-header h1 { font-family:'Plus Jakarta Sans',sans-serif; font-size:1.55rem; font-weight:800; margin:0; color:white; }
.page-header p { opacity:.88; margin:.3rem 0 0 0; color:white; }
.kpi-card { background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:1.1rem 1.3rem; box-shadow:0 1px 6px rgba(0,0,0,.06); }
.kpi-label { font-size:.72rem; font-weight:700; text-transform:uppercase; letter-spacing:.06em; color:#475569; margin-bottom:.35rem; }
.kpi-value { font-family:'Plus Jakarta Sans',sans-serif; font-size:2rem; font-weight:800; color:#1E293B; }
.kpi-delta { font-size:.8rem; color:#64748B; margin-top:.3rem; }
.section-card { background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:1.1rem 1.4rem; box-shadow:0 1px 6px rgba(0,0,0,.05); margin-bottom:1rem; }
.section-title { font-family:'Plus Jakarta Sans',sans-serif; font-size:1.05rem; font-weight:700; color:#0A2463; padding-bottom:.5rem; border-bottom:2px solid #DBEAFE; }
.insight-box { background:#EFF6FF; border-left:4px solid #2563EB; border-radius:0 10px 10px 0; padding:.85rem 1.05rem; margin:.6rem 0 1.2rem 0; font-size:.9rem; color:#1E293B; }
.rec-box { background:#FFFBEB; border-left:4px solid #F59E0B; border-radius:0 10px 10px 0; padding:.85rem 1.05rem; margin:.5rem 0 1.6rem 0; font-size:.9rem; color:#1E293B; }
#MainMenu, footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Kayfa")
    try: st.image("assets/kayfa_logo.jpg", width=160)
    except: pass
    st.caption("Academic Performance Command Center")

pg = st.navigation([
    st.Page("pages/1_Attendance_Grades.py", title="Attendance & Grades", icon="📈"),
    st.Page("pages/2_Assessment_Curriculum.py", title="Assessment & Curriculum", icon="📝"),
    st.Page("pages/3_Engagement_Behavior.py", title="Engagement & Behavior", icon="👥"),
    st.Page("pages/4_Cohorts_Risk.py", title="Cohorts & Risk", icon="🎯"),
], position="sidebar")
pg.run()