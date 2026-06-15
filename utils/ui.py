import streamlit as st
import plotly.express as px
from pathlib import Path

# --- Human-readable labels – no snake_case in the UI ---
_LABELS = {
    "group_id": "Group ID", "attendance_rate": "Attendance Rate",
    "avg_grade": "Average Grade", "score_pct": "Score %",
    "video_watch_hours": "Video Watch Hours", "assessment_seq": "Assessment Sequence",
    "avg_score": "Average Score", "fail_rate": "Failure Rate",
    "concept_name": "Concept", "course_name": "Course",
    "mastery_rate": "Mastery Rate", "buffer_bin": "Submission Timing",
    "grade_pct": "Grade %", "session_datetime": "Session Date",
    "age_band": "Age Band", "engagement_events": "Engagement Events",
    "failed_concepts": "Failed Concepts", "at_risk_score": "At-Risk Score",
    "full_name": "Student", "type": "Assessment Type",
    "stated_num_students": "Stated Size", "true_count": "Actual Size"
}
def human(col: str) -> str:
    return _LABELS.get(col, col.replace("_", " ").title())

def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=DM+Sans:wght@400;500&display=swap');
html, body,.stApp, [data-testid="stAppViewContainer"] { background:#FFFFFF!important; color:#1E293B!important; font-family:'DM Sans',sans-serif; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0A2463 0%, #1447A6 100%)!important; }
[data-testid="stSidebar"] * { color:#FFFFFF!important; }
.main.block-container { padding:1.8rem 2.2rem; max-width:1280px; }
.page-header { margin-bottom:18px; }
.page-header h1 { font-family:'Plus Jakarta Sans',sans-serif; font-size:1.85rem; font-weight:800; margin:0; color:#0A2463; }
.page-header p { color:#475569; margin-top:6px; }
.kpi-card { background:white; padding:16px 18px; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,.06); }
.kpi-label { font-size:.75rem; color:#475569; margin-bottom:6px; font-weight:500; text-transform:uppercase; letter-spacing:.04em; }
.kpi-value { font-size:1.7rem; font-weight:700; line-height:1.2; }
.kpi-delta { font-size:.8rem; color:#64748B; margin-top:4px; }
.section-card { background:white; padding:18px 20px; border-radius:14px; box-shadow:0 2px 10px rgba(0,0,0,.06); margin-bottom:14px; }
.section-title { font-weight:600; font-size:1.1rem; margin-bottom:12px; color:#0A2463; padding-bottom:8px; border-bottom:2px solid #DBEAFE; }
.insight-box { background:#F8FAFC; border-left:4px solid #2563EB; padding:14px 18px; border-radius:8px; margin:12px 0; }
.rec-box { background:#FFFBEB; border-left:4px solid #F59E0B; padding:14px 18px; border-radius:8px; margin:8px 0 16px 0; }
.explore-box { background:#F8FAFC; border:1px dashed #CBD5E1; border-radius:10px; padding:14px 18px; margin:8px 0 20px 0; font-size:.9rem; }
#MainMenu, footer {visibility:hidden;}
.badge-red { background:#FEE2E2; color:#991B1B; padding:2px 8px; border-radius:999px; font-size:.72rem; font-weight:700; }
.badge-amber { background:#FEF3C7; color:#92400E; padding:2px 8px; border-radius:999px; font-size:.72rem; font-weight:700; }
.badge-blue { background:#DBEAFE; color:#1E40AF; padding:2px 8px; border-radius:999px; font-size:.72rem; font-weight:700; }
.badge-green { background:#DCFCE7; color:#166534; padding:2px 8px; border-radius:999px; font-size:.72rem; font-weight:700; }

/* ── Login screen ── */
.login-bg { display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:80vh; }
.login-card { background:white; border-radius:18px; padding:2.5rem 2.8rem;
              box-shadow:0 8px 30px rgba(10,36,99,.12); max-width:420px; width:100%; }
.login-card h2 { font-family:'Plus Jakarta Sans',sans-serif; font-weight:800;
                 color:#0A2463; text-align:center; margin-bottom:.3rem; }
.login-card p  { text-align:center; color:#64748B; margin-bottom:1.6rem; font-size:.95rem; }
button[kind="headerFormSubmit"] { background:#0A2463!important; color:white!important;
    border-radius:10px!important; font-weight:700!important; border:none!important; }
button[kind="headerFormSubmit"]:hover { background:#1447A6!important; }
div[data-testid="stForm"] { border:none!important; background:transparent!important; }
div[data-testid="stTextInputRootElement"] { border-radius:10px!important; }
label[data-testid="stWidgetLabel"] { font-weight:600!important; color:#0A2463!important; }
</style>
""", unsafe_allow_html=True)

def render_header(title: str, subtitle: str=""):
    l, r = st.columns([5,2])
    with l: st.markdown(f'<div class="page-header"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)
    with r:
        for p in ["assets/kayfa_logo.png","assets/kayfa_logo.jpg","kayfaio_logo.jpg","kayfa_logo.png"]:
            if Path(p).exists(): st.image(p, width=300); break

def kpi_row(items):
    cols = st.columns(len(items))
    for col, it in zip(cols, items):
        with col: st.markdown(
            f'''<div class="kpi-card" style="border-top:4px solid {it.get("color","#2563EB")}">
            <div class="kpi-label">{it["label"]}</div>
            <div class="kpi-value" style="color:{it.get("color","#2563EB")}">{it["value"]}</div>
            <div class="kpi-delta">{it.get("delta","")}</div></div>''', unsafe_allow_html=True)

def insight(text): st.markdown(f'<div class="insight-box"><strong>What this means:</strong> {text}</div>', unsafe_allow_html=True)
def rec(text): st.markdown(f'<div class="rec-box"><strong>Recommended Action:</strong> {text}</div>', unsafe_allow_html=True)
def explore(title, text): st.markdown(f'<div class="explore-box"><strong>🔍 Deep Dive – {title}:</strong><br>{text}</div>', unsafe_allow_html=True)

# --- Global sidebar filters – robust to old sessions ---
def filter_bar():
    from utils.db import find_all
    # ensure all keys exist, even if user ran an old version
    defaults = {"groups": [], "courses": [], "types": []}
    if "filters" not in st.session_state:
        st.session_state.filters = defaults.copy()
    else:
        for k, v in defaults.items():
            st.session_state.filters.setdefault(k, v)

    try: groups = sorted({g["group_id"] for g in find_all("q1_attendance") if "group_id" in g})
    except: groups = [f"G{i:02d}" for i in range(1,11)]
    try: courses = sorted({c.get("course_name","") for c in find_all("q3_distribution") if c.get("course_name")})
    except: courses = []
    try: types = sorted({t["type"] for t in find_all("q2_distribution") if "type" in t})
    except: types = ["quiz","assignment","practical","exam"]

    st.markdown("**Filters**")
    sel_g = st.multiselect("Group", groups, default=st.session_state.filters.get("groups", []), placeholder="All Groups")
    sel_c = st.multiselect("Course", courses, default=st.session_state.filters.get("courses", []), placeholder="All Courses") if courses else []
    sel_t = st.multiselect("Assessment Type", types, default=st.session_state.filters.get("types", []), placeholder="All Types")
    st.session_state.filters = {"groups": sel_g, "courses": sel_c, "types": sel_t}

def get_filters():
    return st.session_state.get("filters", {"groups":[], "courses":[], "types":[]})

def apply_filters(df, group_col="group_id", course_col="course_name", type_col="type"):
    f = get_filters()
    if f.get("groups") and group_col in df.columns: df = df[df[group_col].isin(f["groups"])]
    if f.get("courses") and course_col in df.columns: df = df[df[course_col].isin(f["courses"])]
    if f.get("types") and type_col in df.columns: df = df[df[type_col].isin(f["types"])]
    return df

# --- Plotly – always light, black text ---
def style_fig(fig, x=None, y=None):
    fig.update_layout(
        template="plotly_white", paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="DM Sans", color="#1E293B"),
        colorway=["#2563EB","#22C55E","#F59E0B","#EF4444","#6366F1","#06b6d4"],
        margin=dict(t=30,b=50,l=50,r=20), legend_title_text=""
    )
    if x: fig.update_xaxes(title_text=human(x))
    if y: fig.update_yaxes(title_text=human(y))
    return fig

def safe_scatter(df, x, y, **kw):
    import plotly.express as px
    try: fig = px.scatter(df, x=x, y=y, trendline="ols", **kw)
    except: fig = px.scatter(df, x=x, y=y, **kw)
    return style_fig(fig, x, y)