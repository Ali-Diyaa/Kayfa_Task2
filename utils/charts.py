import plotly.graph_objects as go
import plotly.express as px

KAYFA_BLUE = "#1e40af"
KAYFA_BLUE_LIGHT = "#3b82f6"
KAYFA_RED = "#d62728"
KAYFA_GREEN = "#2ca02c"
KAYFA_NEUTRAL = "#6b7280"

def base_layout(fig, title):
    fig.update_layout(
        title=dict(text=title, x=0.01),
        template="plotly_white",
        font=dict(family="Inter, sans-serif", size=14),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=60, b=40),
        hovermode="x unified"
    )
    return fig

def insight(text, cta):
    import streamlit as st
    st.markdown(f"**Insight:** {text}")
    st.success(f"**Action:** {cta}")