import streamlit as st, plotly.express as px, pandas as pd
from pathlib import Path
from utils.db import find_all

st.set_page_config(page_title="Engagement & Behavior", layout="wide")

def header(title, sub):
    l, r = st.columns([6,1])
    with l: st.markdown(f'<div class="page-header"><h1>{title}</h1><p>{sub}</p></div>', unsafe_allow_html=True)
    with r:
        p = Path("assets/kayfa_logo.jpg")
        if p.exists(): st.image(str(p), width=100)

def kpis(items):
    cols = st.columns(len(items))
    for c, (label, val, color, delta) in zip(cols, items):
        with c: st.markdown(f'<div class="kpi-card" style="border-top:4px solid {color}"><div class="kpi-label">{label}</div><div class="kpi-value" style="color:{color}">{val}</div><div class="kpi-delta">{delta}</div></div>', unsafe_allow_html=True)

def show(title, fig, insight, rec):
    st.markdown(f'<div class="section-card"><div class="section-title">{title}</div></div>', unsafe_allow_html=True)
    fig.update_layout(template="plotly_white", paper_bgcolor="white", plot_bgcolor="white", font=dict(color="#1E293B"))
    st.plotly_chart(fig, width='stretch', theme=None)
    st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="rec-box">{rec}</div>', unsafe_allow_html=True)

header("👥 Engagement & Behavior", "Q5 • Q8 • Q9 • Q10")

q5 = find_all("q5_engagement"); q5 = q5[0] if q5 else {}
q8 = find_all("q8_submission_timing")
q9 = find_all("q9_term_trends")
q10 = find_all("q10_age_bands")

kpis([
    ("Video → Grade r", "0.402", "#2563EB", "Strongest signal"),
    ("Late Penalty", "-5.0pp", "#EF4444", "67.1% → 62.1%"),
    ("Term Dip", "Mar 2026", "#F59E0B", "Ramadan / Eid"),
    ("Age Effect", "r≈0.05", "#6366F1", "No predictive power"),
])

pts = pd.DataFrame(q5.get("points", []))
if not pts.empty and "video_watch_hours" in pts:
    fig = px.scatter(pts, x="video_watch_hours", y="avg_grade")
    show("Q5 – Engagement vs Performance", fig,
        "<b>Insight:</b> video r=0.402, logins r=0.328",
        "<b>Action:</b> Promote video completion nudges in LMS.")

df = pd.DataFrame(q8)
if not df.empty:
    fig = px.bar(df, x="buffer_bin", y="grade_pct")
    show("Q8 – Submission Timing", fig,
        "<b>Insight:</b> 3d+ early 79.1%, late 62.2%",
        "<b>Action:</b> 48h early-bonus + late flag in gradebook.")

df = pd.DataFrame(q9)
if not df.empty:
    fig = px.line(df, x="session_datetime", y="attendance_rate", markers=True)
    show("Q9 – Term Trend Dip", fig,
        "<b>Insight:</b> Cohort-wide dip early March 2026 – Ramadan/Eid.",
        "<b>Action:</b> Pre-schedule async catch-up for Ramadan 2027.")

df = pd.DataFrame(q10)
if not df.empty:
    fig = px.bar(df, x="age_band", y="avg_grade")
    show("Q10 – Age Bands", fig,
        "<b>Insight:</b> Age does not predict outcomes.",
        "<b>Action:</b> Focus on attendance/engagement, not age.")