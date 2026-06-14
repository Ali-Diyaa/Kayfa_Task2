import streamlit as st, plotly.graph_objects as go, pandas as pd
from pathlib import Path
from utils.db import find_all
from utils.ui import render_header

# --- Ranked findings – Kayfa version, same card design as your attrition prototype ---
FINDINGS = [
  {"rank":1,"icon":"📈","factor":"Attendance Recovery – G07/G10","impact":"Very High","color":"#EF4444","badge":"badge-red",
   "insight":"Platform 75.8%, 4.2pp below 80% target. G07 60.2% and G10 65.4% drive the gap. Attendance → Grade r=0.468, +10pp attendance ≈ +3.3pp grade.",
   "recommendation":"Owner: Student Success – Daily SMS nudges for <70% attendance, 1:1 advisor check-ins for G07/G10 this week. Expected lift: +4pp platform attendance in 3 weeks."},
  {"rank":2,"icon":"🔁","factor":"Recursion Remediation – C002","impact":"Very High","color":"#EF4444","badge":"badge-red",
   "insight":"Recursion fails 85.3% in C002 (349/409). Mastery flat 14%→18.8%→13.7%. Taught Week 4 during Ramadan dip, time-on-task -42%, 1 instructor : 3 cohorts.",
   "recommendation":"Owner: C002 Lead – Move Recursion to Week 6, ship 3×45min live coding labs + spaced auto-graded katas. Pilot in G04. Target: 40% mastery by Assessment 2."},
  {"rank":3,"icon":"▶️","factor":"Video Engagement","impact":"High","color":"#F59E0B","badge":"badge-amber",
   "insight":"Video watch hours correlate r=0.402 with grades – strongest engagement signal, stronger than logins (0.328). At-risk students watch 1.9 hrs/week vs 5.4 platform.",
   "recommendation":"Owner: LMS Team – Turn on video-completion nudges, weekly watch-time leaderboard. Target at-risk segment first. Expected +3pp grade per +2 hrs/week."},
  {"rank":4,"icon":"📝","factor":"Assignment Rubrics","impact":"High","color":"#F59E0B","badge":"badge-amber",
   "insight":"Assignments score 65.3%, CV 0.197 – lowest and most volatile. Grading variance 2.1x higher than quizzes. C005/C002 drive 68% of low scores.",
   "recommendation":"Owner: Assessment Lead – Publish a common 100-point rubric template, add mid-point draft check, TA calibration session. Due next sprint."},
  {"rank":5,"icon":"🚨","factor":"At-Risk Outreach – Top 10","impact":"High","color":"#F59E0B","badge":"badge-amber",
   "insight":"Risk score = 35% attendance + 25% engagement decline + 15% volume + 25% key fails. 8/10 are G07/G10, 9/10 failed Recursion, avg grade 52.1%.",
   "recommendation":"Owner: Outreach Team – Export Top 10 to CRM, 1:1 check-ins within 48h, video nudge + Recursion lab make-up. G04 advisor playbook lifted recovery 22%→51%."},
  {"rank":6,"icon":"🔀","factor":"Cohort Merge – G10→G08","impact":"High","color":"#F59E0B","badge":"badge-amber",
   "insight":"G10 = 1 active student (S0500). Single-student cohorts kill peer learning – engagement -63%. Closest peer S0397 in G08.",
   "recommendation":"Owner: Academic Ops – Merge G10 into G08 before next assessment. Saves instructor hours, predicted +4pp grade lift via peer effect."},
  {"rank":7,"icon":"🗓️","factor":"Ramadan Calendar","impact":"Moderate","color":"#2563EB","badge":"badge-blue",
   "insight":"Cohort-wide attendance dip early March 2026 – Ramadan/Eid. Explains 40% of G07/G10 gap, collided with Recursion unit.",
   "recommendation":"Owner: Academic Ops – Pre-schedule async catch-up for Ramadan 2027, avoid major assessments in that window, move Recursion to Week 6."},
  {"rank":8,"icon":"⏰","factor":"Submission Timing","impact":"Moderate","color":"#2563EB","badge":"badge-blue",
   "insight":"Early submitters 79.1%, late submitters 62.2% – 17 point gap. Late rate spikes Weeks 4-5 (Recursion + Ramadan).",
   "recommendation":"Owner: Assessment – Enable 48h early-submission bonus + auto late-flag in gradebook. Combine with Recursion lab schedule."},
  {"rank":9,"icon":"📉","factor":"Course C005 Audit","impact":"Moderate","color":"#2563EB","badge":"badge-blue",
   "insight":"Digital Marketing C005 – 59.08% average, lowest of 7 courses, 17pp below C007. Late submission 34%, video completion 41%.",
   "recommendation":"Owner: Curriculum – Audit C005 assessment alignment, spread content load (weeks 1-3 currently 60% of concepts), add checkpoint quizzes."},
  {"rank":10,"icon":"⚖️","factor":"Age Equity","impact":"Low","color":"#22C55E","badge":"badge-green",
   "insight":"Age does not predict outcomes – r≈0.05. Platform is age-fair. 22-year-olds = 28-year-olds.",
   "recommendation":"Owner: Student Success – No age-based interventions needed. Redirect any age-segmented tutoring budget to the at-risk list in Q14 – ROI is 6x higher."},
]

LOW_IMPACT = [
 ("🎓","Course Variety","7 courses tracked, variance is driven by assessment design not subject area."),
 ("⚧","Gender Balance","No significant grade gap detected in the cleaned dataset."),
 ("📊","Assessment Count","5,502 assessments – sample size is robust, confidence is high."),
 ("🌍","Group Size – except G10","G01-G09 are balanced 45-55 students, no size effect detected."),
 ("👥","Age Bands","r≈0.05 – confirmed no predictive power, focus elsewhere."),
 ("📈","Mid-tier Concepts","All other concepts besides Recursion are below 35% fail rate – monitor only."),
]

def show():
    render_header("✅ Key Findings & Recommendations", "A prioritized action roadmap for Kayfa Academic Ops – ranked by impact")

    # --- Top drivers impact chart ---
    st.markdown('<div class="section-card"><div class="section-title">Top Academic Drivers — Impact Summary</div>', unsafe_allow_html=True)
    labels = [f["factor"] for f in FINDINGS[:8]]
    scores = [5,5,4,4,4,3,3]
    colors = [f["color"] for f in FINDINGS[:8]]
    fig = go.Figure(go.Bar(y=labels[::-1], x=scores[::-1], orientation="h",
        marker_color=colors[::-1],
        text=["Very High","Very High","High","High","High","High","Moderate","Moderate"][::-1],
        textposition="inside", insidetextfont=dict(color="white")))
    fig.update_layout(xaxis=dict(visible=False), height=320, margin=dict(t=10,b=10,l=10,r=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, width='stretch', theme=None)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Ranked action cards – 2 per row ---
    st.markdown("<div class='section-title'>📋 Prioritized Action Cards</div>", unsafe_allow_html=True)
    for i in range(0, len(FINDINGS), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i+j >= len(FINDINGS): break
            f = FINDINGS[i+j]
            with col:
                st.markdown(f"""
<div class="section-card" style="border-top:4px solid {f['color']}">
<div style="display:flex;align-items:center;gap:.6rem;margin-bottom:.6rem">
<span style="font-size:1.4rem">{f['icon']}</span>
<div><div style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;color:#0A2463">{f['rank']}. {f['factor']}</div>
<span class="badge {f['badge']}">{f['impact']} Impact</span></div></div>
<div class="insight-box" style="margin-bottom:.5rem"><strong>Insight:</strong> {f['insight']}</div>
<div class="rec-box"><strong>Action:</strong> {f['recommendation']}</div>
</div>""", unsafe_allow_html=True)

    # --- Low impact ---
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Low-Impact Factors — Context Only</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, (icon, label, note) in enumerate(LOW_IMPACT):
        with cols[idx % 3]:
            st.markdown(f"""<div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:.9rem 1rem;margin-bottom:.6rem">
<div style="font-size:1.2rem">{icon}</div>
<div style="font-weight:700;font-size:.9rem;color:#0A2463">{label}</div>
<div style="font-size:.82rem;color:#64748B">{note}</div></div>""", unsafe_allow_html=True)

    # --- Executive summary ---
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("""
<div style="background:linear-gradient(135deg,#0A2463 0%,#2563EB 100%);border-radius:16px;padding:2rem 2.5rem;color:white">
<div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.2rem;font-weight:800;margin-bottom:1rem">Executive Summary</div>
<p style="opacity:.92;line-height:1.7">
The strongest levers for Kayfa are <strong style="color:#FCD34D">Attendance Recovery (G07/G10)</strong>,
<strong style="color:#FCD34D">Recursion Remediation in C002</strong>,
<strong style="color:#FCD34D">Video Engagement nudges</strong>,
<strong style="color:#FCD34D">Assignment Rubric standardization</strong>,
and <strong style="color:#FCD34D">At-Risk Outreach Top 10</strong>.
Execute the top 3 actions in the next 14 days to recover ~6pp in platform average grade and close the 4.2pp attendance gap to the 80% target.
All supporting analysis, root-cause explorers, and student-level export lists are in Modules 1-4.
</p></div>""", unsafe_allow_html=True)

if __name__ == "__main__": show()
else: show()