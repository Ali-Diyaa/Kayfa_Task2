# utils/ui.py
import streamlit as st
from pathlib import Path

def inject_css():
    st.markdown("""
<style>
/* ---- Kayfa Command Center ---- */
.stApp { background-color: #ffffff; }
h1, h2, h3 { letter-spacing: -0.02em; }
.block-container { padding-top: 1.5rem; }

/* KPI cards */
.kpi-row { display: flex; gap: 16px; margin: 12px 0 24px 0; flex-wrap: wrap; }
.kpi-card {
  flex: 1; min-width: 200px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-left: 4px solid #1e40af;
  border-radius: 14px;
  padding: 18px 20px;
  box-shadow: 0 2px 12px rgba(30,64,175,0.06);
}
.kpi-label { font-size: 0.82rem; color: #6b7280; margin-bottom: 4px; }
.kpi-value { font-size: 1.9rem; font-weight: 750; color: #1a1a2e; line-height: 1.1; }
.kpi-delta { font-size: 0.8rem; color: #6b7280; margin-top: 4px; }
.kpi-delta.up { color: #15803d; }
.kpi-delta.down { color: #b91c1c; }

/* Insight / CTA box */
.insight-box {
  background: #f5f7ff;
  border: 1px solid #dbeafe;
  border-left: 4px solid #1e40af;
  border-radius: 12px;
  padding: 14px 18px;
  margin: 12px 0 28px 0;
  font-size: 0.95rem;
}
.insight-box b { color: #1e40af; }

/* Tabs / nicer Plotly */
.stTabs [data-baseweb="tab"] { font-weight: 600; }
.js-plotly-plot { border-radius: 12px; }

/* Hide Streamlit footer */
#MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def render_header(title: str, subtitle: str = ""):
    left, right = st.columns([5, 1])
    with left:
        st.markdown(f"### {title}")
        if subtitle:
            st.caption(subtitle)
    with right:
        logo = Path("assets/kayfa_logo.jpg")
        if logo.exists():
            st.image(str(logo), width=110)
    st.markdown("")

def render_kpis(items):
    """items = [{"label": "...", "value": "...", "delta": "...", "trend": "up|down|neutral"}]"""
    html = '<div class="kpi-row">'
    for it in items:
        delta = it.get("delta", "")
        trend = it.get("trend", "neutral")
        delta_html = f'<div class="kpi-delta {trend}">{delta}</div>' if delta else ""
        html += f'''
        <div class="kpi-card">
          <div class="kpi-label">{it["label"]}</div>
          <div class="kpi-value">{it["value"]}</div>
          {delta_html}
        </div>'''
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def insight(text: str):
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)