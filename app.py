import streamlit as st
from pathlib import Path
from utils.ui import inject_css, filter_bar, get_filters

st.set_page_config(page_title="Kayfa Academic Command Center", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
inject_css()

with st.sidebar:
    st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
    for p in ["assets/kayfa_logo.png","assets/kayfa_logo.jpg","kayfa_logo.png","kayfaio_logo.jpg"]:
        if Path(p).exists():
            st.image(p, width=220)
            break
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("### Kayfa\nAcademic Performance Command Center")
    st.markdown("---")
    filter_bar()
    f = get_filters()
    if f["groups"] or f["courses"]:
        st.caption(f"Filters active: {', '.join(f['groups'] + f['courses'])}")

pg = st.navigation([
    st.Page("pages/0_Overview.py", title="Overview", icon="🏠", default=True),
    st.Page("pages/1_Attendance_Grades.py", title="Attendance & Grades", icon="📈"),
    st.Page("pages/2_Assessment_Curriculum.py", title="Assessment & Curriculum", icon="📝"),
    st.Page("pages/3_Engagement_Behavior.py", title="Engagement & Behavior", icon="👥"),
    st.Page("pages/4_Cohorts_Risk.py", title="Cohorts & Risk", icon="🎯"),
    st.Page("pages/5_Recommendations.py", title="Recommendations", icon="✅"),
], position="sidebar")
pg.run()