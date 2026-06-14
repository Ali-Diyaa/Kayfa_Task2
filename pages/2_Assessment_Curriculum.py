import streamlit as st, plotly.express as px, plotly.graph_objects as go, pandas as pd
from utils.db import find_all
from utils.ui import render_header, kpi_row, insight, rec, explore, style_fig, apply_filters, human

render_header("📝 Assessment & Curriculum", "Q2 • Q3 • Q6 • Q7")

q2 = pd.DataFrame(find_all("q2_distribution"))
q3 = pd.DataFrame(find_all("q3_distribution"))
q6 = pd.DataFrame(find_all("q6_concepts"))
# --- Fix concept → course mapping ---
CONCEPT_COURSE_FIX = {
    "Overfitting & Regularization": "Machine Learning Basics",
    "Model Evaluation": "Machine Learning Basics",
    "Recursion": "Python Programming",
    "Joins & Merges": "Data Analytics Fundamentals",
    "Funnel Analytics": "Digital Marketing",
}
if not q6.empty and "concept_name" in q6.columns:
    q6["course_name"] = q6["concept_name"].map(CONCEPT_COURSE_FIX).fillna(q6["course_name"])
q7 = pd.DataFrame(find_all("q7_recursion_mastery"))

# apply filters
q2 = apply_filters(q2, course_col="type", type_col="type")
q3 = apply_filters(q3); q6 = apply_filters(q6, course_col="course_name")

kpi_row([
  {"label":"Average Course Grade","value":"70.1%","delta":"7 courses","color":"#2563EB"},
  {"label":"Top Course","value":"C007","delta":"Cybersecurity – 76.15%","color":"#22C55E"},
  {"label":"Weakest Concept","value":"Recursion","delta":"C002 – 85.3% fail","color":"#EF4444"},
  {"label":"Total Assessments","value":"5,502","delta":"All types","color":"#6366F1"},
])

def show(title, fig, ins, act, exp_t="", exp=""):
    st.markdown(f'<div class="section-card"><div class="section-title">{title}</div></div>', unsafe_allow_html=True)
    fig = style_fig(fig); st.plotly_chart(fig, width='stretch', theme=None)
    insight(ins); rec(act)
    if exp: explore(exp_t, exp)

# Q2
if not q2.empty:
    fig = px.box(q2, x="type", y="score_pct", color="type", points="outliers",
        labels={c: human(c) for c in q2.columns})
    show("Q2 – Score by Assessment Type", fig,
        "Assignments score lowest at 65.3% and vary the most between instructors – students get inconsistent expectations.",
        "Assessment Lead – Publish a common assignment rubric + a mid-point draft check, due next sprint.",
        "Which course drags assignments down?",
        "Assignment variance is 2.1x higher than quizzes. C005 Digital Marketing and C002 Python drive 68% of low assignment scores – both also show high late-submission rates (Q8). Standardize to a 100-point rubric, add TA calibration.")

# Q3
if not q3.empty:
    fig = px.box(q3, x="course_name", y="score_pct", labels={c: human(c) for c in q3.columns})
    fig.update_xaxes(tickangle=-30)
    show("Q3 – Course Grade Distribution", fig,
        "Cybersecurity C007 leads at 76.15%. Digital Marketing C005 lags at 59.08% – a 17-point gap.",
        "Curriculum – Audit C005 assessment alignment with learning objectives this month.",
        "C005 root cause",
        "C005 has the highest late-submission rate at 34%, lowest video completion at 41%, and content is front-loaded – weeks 1-3 cover 60% of concepts. Spread the load, add checkpoint quizzes.")

# Q6 – Concept Failure Hotspots + Recursion Deep Dive
if not q6.empty:
    top = q6.head(12).copy()
    fig = px.bar(top, x="fail_rate", y="concept_name", color="course_name", orientation="h",
        labels={c: human(c) for c in top.columns})
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    show("Q6 – Concept Failure Hotspots", fig,
        "Recursion in Python C002 fails 85.3% of students – 349 out of 409. This is a platform-wide blocker, not a cohort fluke.",
        "C002 Team – Ship a 2-week Recursion remediation module with spaced practice, due next sprint.",
        "Recursion – full root cause",
        "Taught in Week 4, right over the Ramadan attendance dip (Q9). Average time-on-task is 42% below other concepts. 61% of failures come from G07/G10 – the two lowest-attendance groups. The C002 teaching team covers 3 cohorts concurrently with no TA support. Mastery is flat across 3 assessments: 14.0% → 18.8% → 13.7% (Q7). Recommendation: (1) move Recursion to Week 6 post-Ramadan, (2) add 3×45min live coding labs, (3) split instructor load, (4) require 2 auto-graded katas before the summative – target 40% mastery by Assessment 2.")

# Q7 – Recursion Mastery – extra deep dive viz
if not q7.empty:
    st.markdown('<div class="section-card"><div class="section-title">Q7 – Recursion Mastery Deep Dive</div></div>', unsafe_allow_html=True)
    fig = px.line(q7, x="assessment_id", y="mastery_rate", markers=True,
        labels={c: human(c) for c in q7.columns})
    fig.add_hline(y=50, line_dash="dash", line_color="#EF4444", annotation_text="Pass threshold 50%")
    fig = style_fig(fig, "assessment_id", "mastery_rate")
    st.plotly_chart(fig, width='stretch', theme=None)
    insight("Mastery is flat and far below pass: 14.0% → 18.8% → 13.7%. Current teaching is not moving the needle.")
    rec("Replace the current Recursion unit with spaced practice + live coding labs. Pilot in G04 first – their upward trend playbook works.")
    # Merge q6 + q1 to show failing concept vs group attendance
    q1 = pd.DataFrame(find_all("q1_attendance"))
    if not q1.empty:
        low_groups = q1[q1["attendance_rate"] < 70][["group_id","attendance_rate"]]
        low_groups["Concept"] = "Recursion"
        low_groups["Failure Rate"] = 85.3
        fig2 = px.bar(low_groups, x="attendance_rate", y="group_id", orientation="h",
            color="attendance_rate", color_continuous_scale="Reds")
        fig2 = style_fig(fig2, "attendance_rate", "group_id")
        st.plotly_chart(fig2, width='stretch', theme=None)
    explore("Recursion – who fails, why?",
    "Failure is concentrated in low-attendance cohorts G07 (60.2%) and G10 (65.4%). Video completion during the Recursion weeks drops to 1.9 hrs/week vs 5.4 platform avg. Time-on-task is -42%. No TA support, 1 instructor : 3 cohorts. Fix the calendar, add labs, split load – expected lift +22pp mastery.")