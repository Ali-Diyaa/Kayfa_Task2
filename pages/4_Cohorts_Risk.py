# pages/4_Cohorts_Risk.py
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
with tc: st.markdown('<div class="page-header"><h1>🎯 Cohorts & Risk</h1><p>Q11 • Q12 • Q13 • Q14</p></div>', unsafe_allow_html=True)
with lc:
    lp = Path("assets/kayfa_logo.jpg")
    if lp.exists(): st.image(str(lp), width=130)

q11 = find_all("q11_segments")
q12 = find_all("q12_group_sizes")
q13 = find_all("q13_merge_recommendation"); q13 = q13[0] if q13 else {}
q14 = find_all("q14_at_risk")

kpi_row([
    ("Segments", "4", "#2563EB", "KMeans"),
    ("At-Risk Flagged", f"{len(q14)}", "#EF4444", "Top 10 outreach"),
    ("Size Issues", "2", "#F59E0B", "G05, G10"),
    ("Merge", "G10→G08", "#22C55E", "S0500→S0397"),
])

# Q11
st.markdown('<div class="section-card"><div class="section-title">Q11 – Student Segmentation</div>', unsafe_allow_html=True)
df = pd.DataFrame(q11)
if not df.empty:
    fig = px.scatter(df, x="attendance_rate", y="avg_grade", size="engagement_events", color="segment",
                     hover_data=["failed_concepts"])
    st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="insight-box"><b>Insight:</b> 4 clusters: High Achievers, Steady, Struggling Attenders, Disengaged At-Risk.</div>', unsafe_allow_html=True)
st.markdown('<div class="rec-box"><b>Action:</b> Route Disengaged At-Risk to advisor queue.</div>', unsafe_allow_html=True)

# Q12/Q13
st.markdown('<div class="section-card"><div class="section-title">Q12/Q13 – Group Size Audit</div>', unsafe_allow_html=True)
df = pd.DataFrame(q12)
if not df.empty:
    fig = px.bar(df, x="group_id", y=["stated_num_students","true_count"], barmode="group")
    st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown(f'<div class="insight-box"><b>Insight:</b> G10 = 1 student S0500. Closest match S0397 in G08.</div>', unsafe_allow_html=True)
st.markdown(f'<div class="rec-box"><b>Action:</b> {q13.get("recommendation","Merge G10 into G08")}</div>', unsafe_allow_html=True)

# Q14
st.markdown('<div class="section-card"><div class="section-title">Q14 – At-Risk Ranking</div>', unsafe_allow_html=True)
df = pd.DataFrame(q14)
if not df.empty:
    fig = px.bar(df, x="at_risk_score", y="full_name", color="group_id", orientation="h")
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="insight-box"><b>Insight:</b> Score = 0.35·attendance + 0.25·eng_decline + 0.15·eng_volume + 0.25·key_fail</div>', unsafe_allow_html=True)
st.markdown('<div class="rec-box"><b>Action:</b> Export Top 10 to outreach CRM – 1:1 check-ins this week.</div>', unsafe_allow_html=True)