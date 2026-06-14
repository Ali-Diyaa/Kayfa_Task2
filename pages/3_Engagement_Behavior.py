# pages/3_Engagement_Behavior.py
import streamlit as st, plotly.express as px, pandas as pd
from pathlib import Path
from utils.db import find_all
from utils.ui import inject_css, render_header, kpi_row, insight, rec, plotly_template, get_theme
inject_css()


def kpi_row(items):
    cols = st.columns(len(items))
    for col, (label, val, color, delta) in zip(cols, items):
        with col: st.markdown(f"""<div class="kpi-card" style="border-top:4px solid {color}">
          <div class="kpi-label">{label}</div><div class="kpi-value" style="color:{color}">{val}</div>
          <div class="kpi-delta">{delta}</div></div>""", unsafe_allow_html=True)

tc, lc = st.columns([5,1])
with tc: st.markdown('<div class="page-header"><h1>👥 Engagement & Behavior</h1><p>Q5 • Q8 • Q9 • Q10</p></div>', unsafe_allow_html=True)
with lc:
    lp = Path("assets/kayfa_logo.jpg")
    if lp.exists(): st.image(str(lp), width=130)

q5 = find_all("q5_engagement"); q5 = q5[0] if q5 else {}
q8 = find_all("q8_submission_timing")
q9 = find_all("q9_term_trends")
q10 = find_all("q10_age_bands")

kpi_row([
    ("Video → Grade r", "0.402", "#2563EB", "Strongest signal"),
    ("Late Penalty", "-5.0pp", "#EF4444", "67.1% → 62.1%"),
    ("Term Dip", "Mar 2026", "#F59E0B", "Ramadan / Eid"),
    ("Age Effect", "r≈0.05", "#6366F1", "No predictive power"),
])

# Q5
st.markdown('<div class="section-card"><div class="section-title">Q5 – Engagement vs Performance</div>', unsafe_allow_html=True)
pts = pd.DataFrame(q5.get("points", []))
if not pts.empty and "video_watch_hours" in pts:
    fig = px.scatter(pts, x="video_watch_hours", y="avg_grade", trendline="ols")
    fig.update_layout(template="plotly_white", paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, width='stretch')
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="insight-box"><b>Insight:</b> video r=0.402, logins r=0.328</div>', unsafe_allow_html=True)
st.markdown('<div class="rec-box"><b>Action:</b> Promote video completion nudges in LMS.</div>', unsafe_allow_html=True)

# Q8
st.markdown('<div class="section-card"><div class="section-title">Q8 – Submission Timing</div>', unsafe_allow_html=True)
df = pd.DataFrame(q8)
if not df.empty: st.plotly_chart(px.bar(df, x="buffer_bin", y="grade_pct"), width='stretch')
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="insight-box"><b>Insight:</b> 3d+ early 79.1%, late 62.2%</div>', unsafe_allow_html=True)
st.markdown('<div class="rec-box"><b>Action:</b> 48h early-bonus + late flag in gradebook.</div>', unsafe_allow_html=True)

# Q9
st.markdown('<div class="section-card"><div class="section-title">Q9 – Term Trend Dip</div>', unsafe_allow_html=True)
df = pd.DataFrame(q9)
if not df.empty: st.plotly_chart(px.line(df, x="session_datetime", y="attendance_rate", markers=True), width='stretch')
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="insight-box"><b>Insight:</b> Cohort-wide dip early March 2026 – Ramadan/Eid.</div>', unsafe_allow_html=True)
st.markdown('<div class="rec-box"><b>Action:</b> Pre-schedule async catch-up for Ramadan 2027.</div>', unsafe_allow_html=True)

# Q10
st.markdown('<div class="section-card"><div class="section-title">Q10 – Age Bands</div>', unsafe_allow_html=True)
df = pd.DataFrame(q10)
if not df.empty: st.plotly_chart(px.bar(df, x="age_band", y="avg_grade"), width='stretch')
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="insight-box"><b>Insight:</b> Age does not predict outcomes.</div>', unsafe_allow_html=True)
st.markdown('<div class="rec-box"><b>Action:</b> No age-based interventions – focus on attendance/engagement.</div>', unsafe_allow_html=True)