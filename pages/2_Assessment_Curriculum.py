# pages/2_Assessment_Curriculum.py
import streamlit as st, plotly.express as px, pandas as pd
from pathlib import Path
from utils.db import find_all

def kpi_row(items):
    cols = st.columns(len(items))
    for col, (label, val, color, delta) in zip(cols, items):
        with col: st.markdown(f"""<div class="kpi-card" style="border-top:4px solid {color}">
          <div class="kpi-label">{label}</div><div class="kpi-value" style="color:{color}">{val}</div>
          <div class="kpi-delta">{delta}</div></div>""", unsafe_allow_html=True)

tc, lc = st.columns([5,1])
with tc: st.markdown('<div class="page-header"><h1>📝 Assessment & Curriculum</h1><p>Q2 • Q3 • Q6 • Q7</p></div>', unsafe_allow_html=True)
with lc:
    lp = Path("assets/kayfa_logo.jpg")
    if lp.exists(): st.image(str(lp), width=130)

q2_dist = find_all("q2_distribution")
q3_dist = find_all("q3_distribution")
q6 = find_all("q6_concepts")
q7 = find_all("q7_recursion_mastery")

kpi_row([
    ("Avg Course Grade", "70.1%", "#2563EB", "7 courses"),
    ("Highest Course", "C007", "#22C55E", "Cybersecurity 76.15%"),
    ("Weakest Concept", "Recursion", "#EF4444", "C002 – 85.3% fail"),
    ("Assessments", "5,502", "#6366F1", "All types"),
])

# Q2
st.markdown('<div class="section-card"><div class="section-title">Q2 – Score by Assessment Type</div>', unsafe_allow_html=True)
df = pd.DataFrame(q2_dist)
if not df.empty:
    fig = px.box(df, x="type", y="score_pct", color="type")
    st.plotly_chart(fig, width='stretch')
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="insight-box"><b>Insight:</b> Assignments 65.3%, CV 0.197 – lowest and most volatile.</div>', unsafe_allow_html=True)
st.markdown('<div class="rec-box"><b>Action:</b> Standardize assignment rubrics, add checkpoint drafts.</div>', unsafe_allow_html=True)

# Q3
st.markdown('<div class="section-card"><div class="section-title">Q3 – Course Grade Distribution</div>', unsafe_allow_html=True)
df = pd.DataFrame(q3_dist)
if not df.empty:
    fig = px.box(df, x="course_name", y="score_pct")
    fig.update_xaxes(tickangle=-30)
    st.plotly_chart(fig, width='stretch')
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="insight-box"><b>Insight:</b> C007 76.15% high, C005 59.08% low.</div>', unsafe_allow_html=True)
st.markdown('<div class="rec-box"><b>Action:</b> Audit C005 assessment alignment.</div>', unsafe_allow_html=True)

# Q6
st.markdown('<div class="section-card"><div class="section-title">Q6 – Concept Failure Hotspots</div>', unsafe_allow_html=True)
df = pd.DataFrame(q6)
if not df.empty:
    fig = px.bar(df.head(12), x="fail_rate", y="concept_name", color="course_name", orientation="h")
    st.plotly_chart(fig, width='stretch')
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="insight-box"><b>Insight:</b> Recursion – C002: 85.33% fail.</div>', unsafe_allow_html=True)
st.markdown('<div class="rec-box"><b>Action:</b> Add 2-week Recursion remediation to C002.</div>', unsafe_allow_html=True)

# Q7
st.markdown('<div class="section-card"><div class="section-title">Q7 – Recursion Mastery Over Time</div>', unsafe_allow_html=True)
df = pd.DataFrame(q7)
if not df.empty:
    fig = px.line(df, x="assessment_id", y="mastery_rate", markers=True)
    st.plotly_chart(fig, width='stretch')
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="insight-box"><b>Insight:</b> Mastery flat 14% → 18.8% → 13.7%.</div>', unsafe_allow_html=True)
st.markdown('<div class="rec-box"><b>Action:</b> Replace unit with spaced practice + live coding labs.</div>', unsafe_allow_html=True)