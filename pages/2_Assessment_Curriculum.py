import streamlit as st, plotly.express as px, pandas as pd
from pathlib import Path
from utils.db import find_all

st.set_page_config(page_title="Assessment & Curriculum", layout="wide")
l, r = st.columns([5,1])
with l: st.markdown('<div class="page-header"><h1>📝 Assessment & Curriculum</h1><p>Q2 • Q3 • Q6 • Q7</p></div>', unsafe_allow_html=True)
with r:
    p = Path("assets/kayfa_logo.jpg")
    if p.exists(): st.image(str(p), width=120)

def kpis(items):
    cols = st.columns(len(items))
    for c, (label, val, color, delta) in zip(cols, items):
        with c: st.markdown(f'<div class="kpi-card" style="border-top:4px solid {color}"><div class="kpi-label">{label}</div><div class="kpi-value" style="color:{color}">{val}</div><div class="kpi-delta">{delta}</div></div>', unsafe_allow_html=True)

def chart_card(title, fig, insight, rec):
    st.markdown(f'<div class="section-card"><div class="section-title">{title}</div>', unsafe_allow_html=True)
    fig.update_layout(template="plotly_white", paper_bgcolor="white", plot_bgcolor="white", font_color="#1E293B")
    st.plotly_chart(fig, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="rec-box">{rec}</div>', unsafe_allow_html=True)

q2_dist = find_all("q2_distribution")
q3_dist = find_all("q3_distribution")
q6 = find_all("q6_concepts")
q7 = find_all("q7_recursion_mastery")

kpis([
    ("Avg Course Grade", "70.1%", "#2563EB", "7 courses"),
    ("Highest Course", "C007", "#22C55E", "Cybersecurity 76.15%"),
    ("Weakest Concept", "Recursion", "#EF4444", "C002 – 85.3% fail"),
    ("Assessments", "5,502", "#6366F1", "All types"),
])

df = pd.DataFrame(q2_dist)
if not df.empty:
    fig = px.box(df, x="type", y="score_pct", color="type")
    chart_card("Q2 – Score by Assessment Type", fig,
        "<b>Insight:</b> Assignments 65.3%, most volatile.",
        "<b>Action:</b> Standardize rubrics, add checkpoint drafts.")

df = pd.DataFrame(q3_dist)
if not df.empty:
    fig = px.box(df, x="course_name", y="score_pct")
    fig.update_xaxes(tickangle=-30)
    chart_card("Q3 – Course Grade Distribution", fig,
        "<b>Insight:</b> C007 76.15% high, C005 59.08% low.",
        "<b>Action:</b> Audit C005 assessment alignment.")

df = pd.DataFrame(q6)
if not df.empty:
    fig = px.bar(df.head(12), x="fail_rate", y="concept_name", color="course_name", orientation="h")
    chart_card("Q6 – Concept Failure Hotspots", fig,
        "<b>Insight:</b> Recursion – C002: 85.33% fail.",
        "<b>Action:</b> Add 2-week Recursion remediation to C002.")

df = pd.DataFrame(q7)
if not df.empty:
    fig = px.line(df, x="assessment_id", y="mastery_rate", markers=True)
    chart_card("Q7 – Recursion Mastery Over Time", fig,
        "<b>Insight:</b> Mastery flat 14% → 18.8% → 13.7%.",
        "<b>Action:</b> Spaced practice + live coding labs.")