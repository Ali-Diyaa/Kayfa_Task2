import streamlit as st
from pathlib import Path
from utils.ui import inject_css, filter_bar, get_filters

st.set_page_config(page_title="Kayfa Academic Command Center", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
inject_css()

# ──────────────────────────────────────────────
#  LOGIN GATE
# ──────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # ── hide sidebar on login screen ──
    st.markdown("""
    <style>
    [data-testid="stSidebar"]{visibility:hidden;}
    [data-testid="stSidebar"]>*{visibility:hidden;}
    section[data-testid="stSidebarCollapseButton"]{visibility:hidden;}
    </style>
    """, unsafe_allow_html=True)

    # ── logo ──
    logo_found = False
    for p in ["assets/kayfa_logo.png","assets/kayfa_logo.jpg","kayfa_logo.png","kayfaio_logo.jpg"]:
        if Path(p).exists():
            st.image(p, width=260)
            logo_found = True
            break

    # ── login card ──
    st.markdown("""
    <div style="display:flex;justify-content:center;margin-top:1rem;">
      <div style="background:white;border-radius:18px;padding:2.5rem 2.8rem;
                  box-shadow:0 8px 30px rgba(10,36,99,.12);max-width:400px;width:100%;">
        <h2 style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;
                   color:#0A2463;text-align:center;margin-bottom:.3rem;">Welcome Back</h2>
        <p style="text-align:center;color:#64748B;margin-bottom:1.6rem;font-size:.95rem;">
          Kayfa Academic Command Center
        </p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Sign In", use_container_width=True)

        if submitted:
            if username == "admin" and password == "0000":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")

    # ── footer hint ──
    st.markdown("""
    <div style="text-align:center;margin-top:1.2rem;">
      <span style="color:#94A3B8;font-size:.8rem;">Secured access · Kayfa Platform</span>
    </div>
    """, unsafe_allow_html=True)

    st.stop()   # ← nothing below this runs until logged in

# ──────────────────────────────────────────────
#  AUTHENTICATED — SHOW DASHBOARD
# ──────────────────────────────────────────────
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
    # ── logout button at bottom of sidebar ──
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

pg = st.navigation([
    st.Page("pages/0_Overview.py", title="Overview", icon="🏠", default=True),
    st.Page("pages/1_Attendance_Grades.py", title="Attendance & Grades", icon="📈"),
    st.Page("pages/2_Assessment_Curriculum.py", title="Assessment & Curriculum", icon="📝"),
    st.Page("pages/3_Engagement_Behavior.py", title="Engagement & Behavior", icon="👥"),
    st.Page("pages/4_Cohorts_Risk.py", title="Cohorts & Risk", icon="🎯"),
    st.Page("pages/5_Recommendations.py", title="Recommendations", icon="✅"),
], position="sidebar")
pg.run()