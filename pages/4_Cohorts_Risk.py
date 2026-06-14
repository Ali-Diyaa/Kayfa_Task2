import streamlit as st, plotly.express as px, pandas as pd
from pathlib import Path
from utils.db import find_all

st.set_page_config(page_title="Cohorts & Risk", layout="wide")
l, r = st.columns([5,1])
with l: st.markdown('<div class="page-header"><h1>🎯 Cohorts & Risk</h1><p>Q11 • Q12 • Q13 • Q14</p></div>', unsafe_allow_html=True)
with r:
    p = Path("assets/kayfa_logo.jpg")
    if p.exists(): st.image(str(p), width=120)

def kpis(items):
    cols = st.columns(len(items))
    for c, (label, val, color, delta) in zip(cols, items):
        with c: st.markdown(f'<div class="kpi-card" style="border-top:4px solid {color}"><div class="kpi-label">{label}</div><div class="kpi-value" style="color:{color}">{val}</div><div class="kpi-delta">{delta}</div></div>', unsafe_allow_html=True)

def show_card(title, fig, insight, rec):
    st.markdown(f'<div class="section-card"><div class="section-title">{title}</div>', unsafe_allow_html=True)
    fig.update_layout(template="plotly_white", paper_bgcolor="white", plot_bgcolor="white", font_color="#1E293B")
    st.plotly_chart(fig, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="rec-box">{rec}</div>', unsafe_allow_html=True)

q11 = find_all("q11_segments")
q12 = find_all("q12_group_sizes")
q13 = find_all("q13_merge_recommendation"); q13 = q13[0] if q13 else {}
q14 = find_all("q14_at_risk")

kpis([
    ("Segments", "4", "#2563EB", "KMeans"),
    ("At-Risk Flagged", f"{len(q14)}", "#EF4444", "Top 10 outreach"),
    ("Size Issues", "2", "#F59E0B", "G05, G10"),
    ("Merge", "G10→G08", "#22C55E", "S0500→S0397"),
])

df = pd.DataFrame(q11)
if not df.empty:
    fig = px.scatter(df, x="attendance_rate", y="avg_grade", size="engagement_events", color="segment", hover_data=["failed_concepts"])
    show_card("Q11 – Student Segmentation", fig,
        "<b>Insight:</b> 4 clusters: High Achievers, Steady, Struggling Attenders, Disengaged At-Risk.",
        "<b>Action:</b> Route Disengaged At-Risk to advisor queue.")

df = pd.DataFrame(q12)
if not df.empty:
    fig = px.bar(df, x="group_id", y=["stated_num_students","true_count"], barmode="group")
    show_card("Q12/Q13 – Group Size Audit", fig,
        "<b>Insight:</b> G10 = 1 student S0500. Closest match S0397 in G08.",
        f"<b>Action:</b> {q13.get('recommendation','Merge G10 into G08')}")

df = pd.DataFrame(q14)
if not df.empty:
    fig = px.bar(df, x="at_risk_score", y="full_name", color="group_id", orientation="h")
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    show_card("Q14 – At-Risk Ranking", fig,
        "<b>Insight:</b> Score = 0.35·attendance + 0.25·eng_decline + 0.15·eng_volume + 0.25·key_fail",
        "<b>Action:</b> Export Top 10 to outreach CRM – 1:1 check-ins.")