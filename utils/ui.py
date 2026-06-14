# utils/ui.py
import streamlit as st
from pathlib import Path

def theme_selector():
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    choice = st.sidebar.radio("Theme", ["Light", "Dark"], index=0 if st.session_state.theme=="light" else 1, horizontal=True)
    st.session_state.theme = choice.lower()
    return st.session_state.theme

def get_theme():
    return st.session_state.get("theme", "light")

def inject_css():
    theme = get_theme()
    if theme == "dark":
        bg, card, text, muted, border = "#0f172a", "#1e293b", "#e2e8f0", "#94a3b8", "#334155"
        blue_900, blue_500, blue_50 = "#93c5fd", "#3b82f6", "#1e293b"
        insight_bg, rec_bg = "#1e293b", "#2a2418"
    else:
        bg, card, text, muted, border = "#FFFFFF", "#FFFFFF", "#1E293B", "#475569", "#E2E8F0"
        blue_900, blue_500, blue_50 = "#0A2463", "#2563EB", "#EFF6FF"
        insight_bg, rec_bg = "#EFF6FF", "#FFFBEB"

    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, .stApp, [data-testid="stAppViewContainer"] {{
    background-color: {bg} !important; color: {text} !important;
    font-family: 'DM Sans', sans-serif;
}}
.main.block-container {{ padding: 2rem 2.5rem 3rem; max-width: 1300px; }}
.page-header {{ background: linear-gradient(135deg, {blue_900} 0%, {blue_500} 100%);
  border-radius: 16px; padding: 1.8rem 2.2rem; margin-bottom: 1.5rem; color: white; position: relative; overflow: hidden; }}
.page-header h1 {{ font-family:'Plus Jakarta Sans',sans-serif; font-size:1.7rem; font-weight:800; margin:0; }}
.page-header p {{ opacity:.85; margin:.3rem 0 0 0; }}
.kpi-card {{ background: {card}; border: 1px solid {border}; border-radius: 14px;
  padding: 1.2rem 1.4rem; box-shadow: 0 1px 6px rgba(0,0,0,.06); }}
.kpi-label {{ font-size:.78rem; font-weight:600; text-transform:uppercase; letter-spacing:.06em; color:{muted}; margin-bottom:.4rem; }}
.kpi-value {{ font-family:'Plus Jakarta Sans',sans-serif; font-size:2.0rem; font-weight:800; line-height:1; }}
.kpi-delta {{ font-size:.8rem; color:{muted}; margin-top:.3rem; }}
.section-card {{ background: {card}; border: 1px solid {border}; border-radius: 14px;
  padding: 1.4rem 1.6rem; box-shadow: 0 1px 6px rgba(0,0,0,.05); margin-bottom: 1.2rem; }}
.section-title {{ font-family:'Plus Jakarta Sans',sans-serif; font-size:1.05rem; font-weight:700;
  color:{blue_500}; margin-bottom:.8rem; padding-bottom:.5rem; border-bottom:2px solid {border}; }}
.insight-box {{ background: {insight_bg}; border-left: 4px solid {blue_500};
  border-radius: 0 10px 10px 0; padding:.9rem 1.1rem; margin:.6rem 0 1.2rem 0; font-size:.9rem; }}
.rec-box {{ background: {rec_bg}; border-left: 4px solid #F59E0B;
  border-radius: 0 10px 10px 0; padding:.9rem 1.1rem; margin:.6rem 0 1.2rem 0; font-size:.9rem; }}
#MainMenu, footer {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

def render_header(title: str, subtitle: str = ""):
    left, right = st.columns([5,1])
    with left:
        st.markdown(f'<div class="page-header"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)
    with right:
        lp = Path("assets/kayfa_logo.png")
        if lp.exists(): st.image(str(lp), width=110)

def kpi_row(items, default_color="#2563EB"):
    cols = st.columns(len(items))
    for col, it in zip(cols, items):
        label, val = it["label"], it["value"]
        color = it.get("color", default_color)
        delta = it.get("delta", "")
        with col:
            st.markdown(f"""<div class="kpi-card" style="border-top:4px solid {color}">
              <div class="kpi-label">{label}</div>
              <div class="kpi-value" style="color:{color}">{val}</div>
              <div class="kpi-delta">{delta}</div></div>""", unsafe_allow_html=True)

def insight(text): st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)
def rec(text): st.markdown(f'<div class="rec-box">{text}</div>', unsafe_allow_html=True)

def plotly_template():
    return "plotly_white" if get_theme() == "light" else "plotly_dark"