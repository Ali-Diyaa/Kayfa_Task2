# pages/1_Attendance_Grades.py
import streamlit as st
import plotly.express as px
import pandas as pd
from pathlib import Path
from utils.db import find_all

def kpi_row(items):
    cols = st.columns(len(items))
    for col, (label, val, color, delta) in zip(cols, items):
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="border-top:4px solid {color}">
              <div class="kpi-label">{label}</div>
              <div class="kpi-value" style="color:{color}">{val}</div>
              <div class="kpi-delta">{delta}</div>
            </div>""", unsafe_allow_html=True)

# --- header with logo top-right ---
tc, lc = st.columns([5,1])
with tc: st.markdown('<div class="page-header"><h1>📈 Attendance & Grades</h1><p>Q1 • Q4 • Q15 – Cohort health and trajectory</p></div>', unsafe_allow_html=True)
with lc:
    lp = Path("assets/kayfa_logo.jpg")
    if lp.exists(): st.image(str(lp), width=130)

# --- load ---
q1 = find_all("q1_attendance")
q1_meta = find_all("q1_meta")
platform_avg = q1_meta[0].get("platform_avg", 75.8) if q1_meta else 75.8
q4 = find_all("q4_attendance_grade")
q4 = q4[0] if q4 else {"r":0.468, "points":[]}
q15_trends = find_all("q15_group_trends")
q15_assess = find_all("q15_group_assess")

df_q1 = pd.DataFrame(q1)
df_q15 = pd.DataFrame(q15_assess)
pts = pd.DataFrame(q4.get("points", []))
avg_grade = pts["avg_grade"].mean() if not pts.empty and "avg_grade" in pts else 71.2
up_groups = sum(1 for t in q15_trends if t.get("slope",0) > 0)

kpi_row([
    ("Platform Attendance", f"{platform_avg:.1f}%", "#2563EB", "Target 80%"),
    ("Avg Grade", f"{avg_grade:.1f}%", "#22C55E", f"r = {q4.get('r',0.468):.3f}"),
    ("Active Groups", f"{len(df_q1)}", "#6366F1", "10 cohorts"),
    ("Trending Up", f"{up_groups}", "#F59E0B", "G04, G08"),
])

# Q1
st.markdown('<div class="section-card"><div class="section-title">Q1 – Attendance by Group</div>', unsafe_allow_html=True)
if not df_q1.empty:
    fig = px.bar(df_q1, x="group_id", y="attendance_rate", color="status_label",
        color_discrete_map={"Below average":"#EF4444","Above average":"#2563EB"})
    fig.update_layout(height=320, margin=dict(t=10,b=10), yaxis_title="Attendance %")
    st.plotly_chart(fig, width='stretch')
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="insight-box"><b>Insight:</b> Platform 75.8%. G07 60.2% and G10 65.4% below average.</div>', unsafe_allow_html=True)
st.markdown('<div class="rec-box"><b>Action:</b> Trigger check-in workflow for G07/G10 instructors this week.</div>', unsafe_allow_html=True)

# Q4
st.markdown('<div class="section-card"><div class="section-title">Q4 – Attendance → Grade</div>', unsafe_allow_html=True)
if not pts.empty:
    fig = px.scatter(pts, x="attendance_rate", y="avg_grade", trendline="ols")
    fig.update_layout(height=300, xaxis_title="Attendance %", yaxis_title="Grade %")
    st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown(f'<div class="insight-box"><b>Insight:</b> r = {q4.get("r",0.468):.3f}. +10pp attendance ≈ +3.3pp grade.</div>', unsafe_allow_html=True)
st.markdown('<div class="rec-box"><b>Action:</b> Auto-nudge students &lt;70% attendance.</div>', unsafe_allow_html=True)

# Q15
st.markdown('<div class="section-card"><div class="section-title">Q15 – Group Score Trends</div>', unsafe_allow_html=True)
if not df_q15.empty:
    fig = px.line(df_q15, x="assessment_seq", y="avg_score", color="group_id", markers=True)
    fig.update_layout(height=340, xaxis_title="Assessment Seq", yaxis_title="Avg Score")
    st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="insight-box"><b>Insight:</b> Up: G04, G08. Down: G10, G06.</div>', unsafe_allow_html=True)
st.markdown('<div class="rec-box"><b>Action:</b> Peer-review G04 materials, audit G10/G06 pacing.</div>', unsafe_allow_html=True)