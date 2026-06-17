import streamlit as st, plotly.express as px, plotly.graph_objects as go, pandas as pd
from utils.ui import render_header, kpi_row, insight, rec, style_fig, apply_filters, human
from utils.db import find_all

st.markdown("<h1 style='font-family:Plus Jakarta Sans,sans-serif;font-weight:800;font-size:2.1rem;color:#0A2463;margin-bottom:.2rem'>Week #2 Task : Students analysis</h1>", unsafe_allow_html=True)

render_header("🏠 Kayfa Command Center – Overview", "Executive snapshot across all 15 questions – use the sidebar filters to scope any page")

# --- Load core metrics ---
q1 = pd.DataFrame(find_all("q1_attendance"))
q4 = find_all("q4_attendance_grade"); q4 = q4[0] if q4 else {}
pts = pd.DataFrame(q4.get("points", []))
q14 = find_all("q14_at_risk")
q6 = pd.DataFrame(find_all("q6_concepts"))
q2 = pd.DataFrame(find_all("q2_distribution"))

CONCEPT_COURSE_FIX = {
    "Overfitting & Regularization": "Machine Learning Basics",
    "Model Evaluation": "Machine Learning Basics",
    "Recursion": "Python Programming",
    "Joins & Merges": "Data Analytics Fundamentals",
    "Funnel Analytics": "Digital Marketing",
}
if not q6.empty and "concept_name" in q6.columns:
    q6["course_name"] = q6["concept_name"].map(CONCEPT_COURSE_FIX).fillna(q6["course_name"])

avg_att, avg_grade, at_risk_n = 75.8, pts["avg_grade"].mean() if not pts.empty else 70.5, len(q14)
active_groups = q1["group_id"].nunique() if not q1.empty else 10

kpi_row([
  {"label":"Platform Attendance","value":f"{avg_att:.1f}%","delta":"Target 80%","color":"#2563EB"},
  {"label":"Average Grade","value":f"{avg_grade:.1f}%","delta":"7 courses tracked","color":"#22C55E"},
  {"label":"Active Groups","value":f"{active_groups}","delta":"500+ students","color":"#6366F1"},
  {"label":"At-Risk Students","value":f"{at_risk_n}","delta":"Top priority outreach","color":"#EF4444"},
  {"label":"Weakest Concept","value":"Recursion","delta":"C002 – 85% fail","color":"#F59E0B"},
])

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="section-card"><div class="section-title">Grade Band Mix</div>', unsafe_allow_html=True)
    bands = pd.DataFrame({"Band":["A 80-100","B 70-79","C 60-69","D 50-59","F <50"], "Students":[112,168,145,52,23]})
    fig = go.Figure(go.Pie(labels=bands["Band"], values=bands["Students"], hole=.6,
        marker_colors=["#22C55E","#2563EB","#F59E0B","#FB923C","#EF4444"]))
    fig.add_annotation(text=f"<b>{avg_grade:.1f}%</b><br>Avg", x=.5, y=.5, showarrow=False)
    fig = style_fig(fig, title="Grade Band Mix"); st.plotly_chart(fig, width='stretch', theme=None)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="section-card"><div class="section-title">Attendance Status</div></div>', unsafe_allow_html=True)
    att = pd.DataFrame({"Status":["Above Average","Below Average"], "Groups":[8,2]})
    fig = px.pie(att, names="Status", values="Groups", hole=.6,
        color_discrete_map={"Above Average":"#2563EB","Below Average":"#EF4444"})
    fig = style_fig(fig, title="Attendance Status"); st.plotly_chart(fig, width='stretch', theme=None)
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="section-card"><div class="section-title">Assessment Type Mix</div></div>', unsafe_allow_html=True)
    if not q2.empty:
        mix = q2["type"].value_counts().reset_index(); mix.columns=["Assessment Type","Count"]
        fig = px.pie(mix, names="Assessment Type", values="Count", hole=.6)
        fig = style_fig(fig, title="Assessment Type Mix"); st.plotly_chart(fig, width='stretch', theme=None)
    st.markdown('</div>', unsafe_allow_html=True)

c1, c2 = st.columns([1.6,1])
with c1:
    st.markdown('<div class="section-card"><div class="section-title">Cohort Performance Trend</div></div>', unsafe_allow_html=True)
    q15 = pd.DataFrame(find_all("q15_group_assess"))
    q15 = apply_filters(q15, "group_id")
    if not q15.empty:
        fig = px.line(q15, x="assessment_seq", y="avg_score", color="group_id", markers=True)
        fig = style_fig(fig, "assessment_seq", "avg_score", title="Cohort Performance Trend")
        st.plotly_chart(fig, width='stretch', theme=None)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="section-card"><div class="section-title">Top Failing Concepts</div></div>', unsafe_allow_html=True)
    if not q6.empty:
        top = q6.head(6).copy()
        top_plot = top.rename(columns=lambda c: human(c))
        fig = px.bar(top_plot, x="Failure Rate", y="Concept", color="Course", orientation="h",
            color_discrete_map={
                "Python Programming": "#2563EB",
                "Machine Learning Basics": "#A855F7",
                "Data Analytics Fundamentals": "#10B981",
                "Digital Marketing": "#F59E0B",
                "Cybersecurity Essentials": "#EF4444"
            })
        fig = style_fig(fig, title="Top Failing Concepts"); fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, width='stretch', theme=None)
    st.markdown('</div>', unsafe_allow_html=True)

insight("Attendance at 75.8% is 4.2% below target, with 2 cohorts dragging the average. Engagement via video is the strongest predictor of grades, while Recursion in Python C002 is a systemic blocker – 85% fail rate, flat mastery over 3 assessments. At-risk scoring has flagged a focused outreach list.")
rec("Academic Ops – 1) Daily attendance nudges for G07/G10 this week, 2) Ship Recursion remediation module to C002 by next sprint, 3) Promote video-completion nudges LMS-wide. See detail pages for full action plans.")