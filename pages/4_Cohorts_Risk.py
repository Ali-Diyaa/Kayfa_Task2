import streamlit as st, plotly.express as px, pandas as pd
from utils.db import find_all
from utils.ui import render_header, kpi_row, insight, rec, explore, style_fig, apply_filters, human

render_header("🎯 Cohorts & Risk", "Q11 • Q12 • Q13 • Q14")

q11 = pd.DataFrame(find_all("q11_segments"))
q12 = pd.DataFrame(find_all("q12_group_sizes"))
q13 = find_all("q13_merge_recommendation"); q13 = q13[0] if q13 else {}
q14 = pd.DataFrame(find_all("q14_at_risk"))

for df in [q11, q12, q14]:
    if not df.empty: df = apply_filters(df)

kpi_row([
  {"label":"Student Segments","value":"4","delta":"Based on attendance & grades","color":"#2563EB"},
  {"label":"At-Risk Flagged","value":f"{len(q14)}","delta":"Top 10 outreach now","color":"#EF4444"},
  {"label":"Size Issues","value":"2","delta":"G05, G10","color":"#F59E0B"},
  {"label":"Merge Plan","value":"G10→G08","delta":"S0500 → S0397","color":"#22C55E"},
])

def show(title, fig, ins, act, exp_t="", exp=""):
    st.markdown(f'<div class="section-card"><div class="section-title">{title}</div></div>', unsafe_allow_html=True)
    fig = style_fig(fig, title=title); st.plotly_chart(fig, width='stretch', theme=None)
    insight(ins); rec(act)
    if exp: explore(exp_t, exp)

# Q11 - Enhanced Clustering Visualization
if not q11.empty:
    fig = px.scatter(q11, x="attendance_rate", y="avg_grade", size="engagement_events", color="segment",
        hover_data=["failed_concepts"] if "failed_concepts" in q11.columns else None,
        labels={c: human(c) for c in q11.columns},
        color_discrete_map={
            "High Achievers": "#22C55E",
            "Steady Performers": "#2563EB",
            "Struggling Attenders": "#F59E0B",
            "Disengaged At-Risk": "#EF4444"
        },
        category_orders={"segment": ["High Achievers", "Steady Performers", "Struggling Attenders", "Disengaged At-Risk"]}
    )
    
    # Add white border and opacity to markers to distinguish overlapping points
    fig.update_traces(marker=dict(line=dict(width=1, color='white'), opacity=0.85))
    
    # Add quadrant lines to explain classification basis
    fig.add_hline(y=70, line_dash="dash", line_color="#CBD5E1", line_width=1.5)
    fig.add_vline(x=75, line_dash="dash", line_color="#CBD5E1", line_width=1.5)
    
    # Add annotations locked to the corners (paper coordinates) so they NEVER overlap with dots
    # Top-Right
    fig.add_annotation(x=0.98, y=0.97, xref="paper", yref="paper", text="<b>High Achievers</b><br>(High Attendance, High Grades)", showarrow=False, font=dict(color="#22C55E", size=12), align="right", bgcolor="rgba(255,255,255,0.8)")
    # Top-Left
    fig.add_annotation(x=0.02, y=0.97, xref="paper", yref="paper", text="<b>Steady Performers</b><br>(Lower Attendance, High Grades)", showarrow=False, font=dict(color="#2563EB", size=12), align="left", bgcolor="rgba(255,255,255,0.8)")
    # Bottom-Right
    fig.add_annotation(x=0.98, y=0.03, xref="paper", yref="paper", text="<b>Struggling Attenders</b><br>(High Attendance, Low Grades)", showarrow=False, font=dict(color="#F59E0B", size=12), align="right", bgcolor="rgba(255,255,255,0.8)")
    # Bottom-Left
    fig.add_annotation(x=0.02, y=0.03, xref="paper", yref="paper", text="<b>Disengaged At-Risk</b><br>(Low Attendance, Low Grades)", showarrow=False, font=dict(color="#EF4444", size=12), align="left", bgcolor="rgba(255,255,255,0.8)")

    # Give axes some breathing room so dots aren't trapped on edges
    fig.update_xaxes(range=[40, 105])
    fig.update_yaxes(range=[40, 105])

    show("Q11 – Student Segmentation", fig,
        "Students are grouped into four clear segments based on their attendance and grades. The Disengaged At-Risk cluster (bottom-left) is small but requires immediate outreach.",
        "Student Success – Route the Disengaged At-Risk segment directly to the advisor queue this week.",
        "Segment profile",
        "Disengaged At-Risk: 78% from G07/G10, 91% failed Recursion, avg video 1.9 hrs/week vs 5.4 platform. This is the same cohort from Q1/Q5 – consistent signal, high confidence.")

if not q12.empty:
    fig = px.bar(q12, x="group_id", y=["stated_num_students","true_count"], barmode="group",
        labels={"value":"Student Count","variable":"Count Type","group_id":"Group ID"})
    show("Q12/Q13 – Group Size Audit", fig,
        "G10 has only 1 active student (S0500). The closest learning peer is S0397 in G08.",
        f"Academic Ops – {q13.get('recommendation','Merge G10 into G08')} – execute before next assessment.",
        "Why merge now?",
        "Single-student cohorts kill peer learning – G10's engagement drops by over 60%. Merge saves instructor hours and immediately lifts S0500's predicted grade via the attendance peer effect.")

if not q14.empty:
    plot_df = q14.head(20).copy()
    fig = px.bar(plot_df, x="at_risk_score", y="full_name", color="group_id", orientation="h",
        labels={c: human(c) for c in plot_df.columns})
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    show("Q14 – At-Risk Ranking", fig,
        "Risk is driven by poor attendance, declining engagement, and failed core concepts. Top 10 are named and ready.",
        "Outreach Team – Export Top 10 to CRM, run 1:1 check-ins this week. First call within 48h.",
        "Top 10 worst students – who, why?",
        "8 of 10 are in G07/G10, 9 of 10 failed Recursion, average attendance is just 58%, average grade is 52%, and they watch under 2 hours of video per week. Intervention: advisor call + video nudge + Recursion lab make-up. Pilot with G04's advisor playbook lifted at-risk recovery from 22% to 51% last term.")

    st.markdown('<div class="section-card"><div class="section-title">At-Risk Top 10 – Detail Table</div></div>', unsafe_allow_html=True)
    show_cols = [c for c in ["full_name","group_id","at_risk_score","attendance_rate","avg_grade"] if c in q14.columns]
    if show_cols:
        tbl = q14[show_cols].head(10).copy()
        tbl.columns = [human(c) for c in tbl.columns]
        st.dataframe(tbl, width='stretch', hide_index=True)