"""
👑 TOPPER SYSTEM — Fully Responsive (Desktop + Mobile)
"""

import streamlit as st
import streamlit.components.v1 as components
import time, json, os, calendar, base64
from datetime import date, timedelta
import pandas as pd

st.set_page_config(
    page_title="👑 Topper System",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="auto",   # open on desktop, collapsed on mobile automatically
)

# ══════════════════════════════════════════════════════════════
#  SESSION STATE STORAGE
# ══════════════════════════════════════════════════════════════
def ss_init():
    defaults = {
        "tasks":   [],
        "study":   {"study_hours": {}, "goal": 5},
        "events":  {},
        "profile": {"username": "", "avatar_b64": ""},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

ss_init()

def get_tasks():   return st.session_state["tasks"]
def get_study():   return st.session_state["study"]
def get_events():  return st.session_state["events"]
def get_profile(): return st.session_state["profile"]

today = str(date.today())

# ══════════════════════════════════════════════════════════════
#  FULLY RESPONSIVE ROYAL GOLD CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Cormorant+Garamond:wght@600;700&family=Raleway:wght@300;400;500;600;700&display=swap');

/* ── BASE ── */
* { font-family:'Raleway',sans-serif; box-sizing:border-box;
    -webkit-tap-highlight-color:transparent; }

/* ── BACKGROUND ── */
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse at 15% 60%,rgba(180,140,0,.18) 0%,transparent 55%),
        radial-gradient(ellipse at 85% 15%,rgba(212,175,55,.14) 0%,transparent 50%),
        linear-gradient(160deg,#080600 0%,#100e00 45%,#181200 100%);
    color:#f5e6b0; min-height:100vh;
}

/* ── MAIN CONTENT — responsive padding ── */
.main .block-container {
    padding: 2rem 3rem 90px 3rem !important;
    max-width: 1200px !important;
    margin: 0 auto !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#0a0800 0%,#141000 100%) !important;
    border-right:1px solid rgba(212,175,55,.25) !important;
    min-width: 240px !important;
}
[data-testid="stSidebar"] * { color:#d4af37 !important; }
[data-testid="stSidebar"] .stRadio label {
    font-size:15px !important;
    padding:10px 0 !important;
    cursor:pointer !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    color:#f5e6b0 !important;
}

#MainMenu,footer,header { visibility:hidden; }
.stDeployButton { display:none; }

/* ── SIDEBAR PROFILE CARD ── */
.sb-profile {
    background:linear-gradient(135deg,rgba(212,175,55,.12),rgba(212,175,55,.04));
    border:1px solid rgba(212,175,55,.35); border-radius:16px;
    padding:20px 16px 16px; margin:10px 0 24px; text-align:center;
}
.sb-avatar {
    width:80px; height:80px; border-radius:50%;
    border:2px solid #d4af37; object-fit:cover;
    margin-bottom:10px; box-shadow:0 0 20px rgba(212,175,55,.35);
    display:block; margin-left:auto; margin-right:auto;
}
.sb-avatar-placeholder {
    width:80px; height:80px; border-radius:50%;
    border:2px dashed rgba(212,175,55,.5); background:rgba(212,175,55,.08);
    display:flex; align-items:center; justify-content:center;
    font-size:36px; margin:0 auto 10px;
}
.sb-username {
    font-family:'Cinzel',serif; font-size:15px; font-weight:700;
    color:#f5e6b0 !important; letter-spacing:1.5px;
}
.sb-tagline {
    font-size:11px; color:rgba(212,175,55,.6) !important;
    letter-spacing:1px; text-transform:uppercase; margin-top:4px;
}

/* ── PAGE TITLES ── */
.royal-title {
    font-family:'Cinzel',serif;
    font-size: clamp(26px, 4vw, 48px);
    font-weight:900; text-align:center;
    background:linear-gradient(135deg,#d4af37 0%,#f5e6b0 50%,#b8860b 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; letter-spacing:3px; margin-bottom:4px; line-height:1.2;
}
.gold-divider {
    width:80px; height:2px;
    background:linear-gradient(90deg,transparent,#d4af37,transparent);
    margin:8px auto 20px;
}

/* ── META BADGES ── */
.meta-bar {
    display:flex; justify-content:center; gap:12px;
    align-items:center; margin:0 0 28px; flex-wrap:wrap;
}
.meta-badge {
    font-family:'Cormorant Garamond',serif;
    font-size: clamp(13px, 1.6vw, 19px);
    font-weight:700; color:#f5e6b0;
    background:linear-gradient(135deg,rgba(212,175,55,.15),rgba(212,175,55,.04));
    border:1px solid rgba(212,175,55,.4);
    padding:8px 20px; border-radius:50px; white-space:nowrap;
}

/* ── SECTION HEADINGS ── */
.section-heading {
    font-family:'Cinzel',serif;
    font-size: clamp(15px, 2vw, 20px);
    font-weight:700; color:#d4af37; letter-spacing:2px; margin:22px 0 14px;
}

/* ── TIMER ── */
.timer-wrapper {
    background:linear-gradient(135deg,rgba(212,175,55,.1),rgba(0,0,0,.3));
    border:2px solid rgba(212,175,55,.4); border-radius:24px;
    padding:clamp(28px,5vw,50px) 20px clamp(24px,4vw,44px);
    margin:20px 0 28px; text-align:center;
    box-shadow:0 0 60px rgba(212,175,55,.08);
}
.timer-display {
    font-family:'Cinzel',serif;
    font-size: clamp(52px, 12vw, 110px);
    font-weight:900;
    background:linear-gradient(135deg,#d4af37 0%,#f5e6b0 50%,#b8860b 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; letter-spacing:6px; line-height:1;
}
.timer-label {
    font-size:11px; color:rgba(212,175,55,.6);
    letter-spacing:4px; text-transform:uppercase; margin-top:12px;
}

/* ── EVENT CHIPS ── */
.event-chip {
    display:inline-block;
    background:linear-gradient(135deg,rgba(212,175,55,.2),rgba(184,134,11,.1));
    border:1px solid rgba(212,175,55,.45); border-radius:20px;
    padding:6px 16px; font-size:13px; color:#f5e6b0; margin:4px 4px 4px 0;
    box-shadow:0 0 8px rgba(212,175,55,.15);
}
.hrs-badge {
    font-family:'Cinzel',serif;
    font-size: clamp(28px, 4vw, 40px);
    font-weight:900;
    background:linear-gradient(135deg,#d4af37,#f5e6b0);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text;
}

/* ── PROFILE ── */
.profile-avatar-big {
    width:clamp(90px,12vw,130px); height:clamp(90px,12vw,130px);
    border-radius:50%; border:3px solid #d4af37; object-fit:cover;
    box-shadow:0 0 40px rgba(212,175,55,.35); display:block; margin:0 auto 16px;
}
.profile-stat-box {
    background:linear-gradient(135deg,rgba(212,175,55,.1),rgba(0,0,0,.2));
    border:1px solid rgba(212,175,55,.3); border-radius:14px;
    padding:clamp(12px,2vw,20px); text-align:center;
}
.profile-stat-num {
    font-family:'Cinzel',serif;
    font-size: clamp(22px, 3vw, 34px);
    font-weight:900;
    background:linear-gradient(135deg,#d4af37,#f5e6b0);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text;
}
.profile-stat-label {
    font-size:clamp(9px,1.2vw,11px); color:rgba(212,175,55,.6);
    letter-spacing:2px; text-transform:uppercase; margin-top:6px;
}

/* ── BUTTONS ── */
.stButton>button {
    background:linear-gradient(135deg,#b8860b,#d4af37) !important;
    color:#0a0800 !important; border:none !important;
    border-radius:12px !important;
    font-family:'Raleway',sans-serif !important;
    font-weight:700 !important; font-size:14px !important;
    padding:13px 20px !important; min-height:48px !important;
    letter-spacing:1px !important; text-transform:uppercase !important;
    transition:all .2s !important; width:100% !important;
}
.stButton>button:hover {
    background:linear-gradient(135deg,#d4af37,#f5e6b0) !important;
    box-shadow:0 4px 22px rgba(212,175,55,.4) !important;
    transform:translateY(-2px) !important;
}
.stButton>button:active { transform:scale(0.97) !important; }

/* ── INPUTS ── */
.stTextInput>div>div>input,
.stTextArea>div>div>textarea,
.stNumberInput>div>div>input {
    background:#1a1500 !important;
    border:1px solid rgba(212,175,55,.45) !important;
    border-radius:10px !important; color:#f5e6b0 !important;
    font-size:16px !important; padding:12px 14px !important;
    caret-color:#d4af37;
}
.stTextInput>div>div>input::placeholder,
.stTextArea>div>div>textarea::placeholder { color:rgba(212,175,55,.35) !important; }
.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus {
    border-color:#d4af37 !important;
    box-shadow:0 0 0 3px rgba(212,175,55,.2) !important;
    background:#211c00 !important;
}
[data-baseweb="select"]>div {
    background:#1a1500 !important; border-color:rgba(212,175,55,.45) !important;
    border-radius:10px !important;
}
[data-baseweb="popover"],[data-baseweb="menu"] { background:#1a1500 !important; border:1px solid rgba(212,175,55,.3) !important; }
[data-baseweb="option"] { background:#1a1500 !important; color:#f5e6b0 !important; }
[data-baseweb="option"]:hover { background:rgba(212,175,55,.15) !important; }

/* ── LABELS ── */
label[data-testid="stWidgetLabel"] p,
label[data-testid="stWidgetLabel"] {
    font-weight:600 !important; font-size:12px !important;
    color:rgba(212,175,55,.8) !important; text-transform:uppercase !important;
    letter-spacing:1.5px !important;
}

/* ── PROGRESS ── */
.stProgress>div>div>div>div {
    background:linear-gradient(90deg,#b8860b,#d4af37,#f5e6b0) !important;
    border-radius:100px !important;
}
.stProgress>div>div>div {
    background:rgba(212,175,55,.12) !important;
    border-radius:100px !important; height:10px !important;
}

/* ── CHECKBOX ── */
.stCheckbox label p {
    font-size:15px !important; font-weight:500 !important;
    color:#f5e6b0 !important; line-height:1.5 !important;
}
.stCheckbox>label { min-height:44px !important; padding:8px 0 !important; }

/* ── MISC ── */
div[data-testid="stCaptionContainer"] p { color:rgba(212,175,55,.55) !important; font-size:13px !important; }
div[data-testid="stNotificationContent"] { background:rgba(212,175,55,.1) !important; color:#f5e6b0 !important; }
.stNumberInput button {
    background:rgba(212,175,55,.15) !important; border:1px solid rgba(212,175,55,.3) !important;
    color:#d4af37 !important; min-width:44px !important; min-height:44px !important;
    text-transform:none !important; letter-spacing:0 !important; font-size:18px !important;
}
[data-testid="stFileUploader"] {
    border:1px dashed rgba(212,175,55,.4) !important;
    border-radius:12px !important; background:rgba(212,175,55,.05) !important;
}
[data-testid="stFileUploader"] * { color:rgba(212,175,55,.8) !important; }

/* ── AD BAR ── */
.ad-bar {
    position:fixed; bottom:0; left:0; width:100%; z-index:9999;
    background:linear-gradient(90deg,#080600,#141000,#080600);
    border-top:1px solid rgba(212,175,55,.25);
    padding:0; min-height:52px;
    display:flex; align-items:center; justify-content:center;
}

/* ══════════════════════════════════════════════════════
   MOBILE OVERRIDES  (screens ≤ 768px)
══════════════════════════════════════════════════════ */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem 0.8rem 80px !important;
    }
    .royal-title { font-size:26px !important; letter-spacing:1px !important; }
    .meta-badge  { font-size:12px !important; padding:6px 10px !important; }
    .section-heading { font-size:15px !important; letter-spacing:1px !important; }
    .timer-display { font-size:64px !important; letter-spacing:3px !important; }
    .timer-wrapper { padding:24px 14px 20px !important; }
    .profile-stat-box { padding:12px 6px !important; }
    .profile-stat-num { font-size:22px !important; }
    .profile-stat-label { font-size:9px !important; letter-spacing:1px !important; }
}

/* ══════════════════════════════════════════════════════
   SMALL PHONE OVERRIDES  (screens ≤ 420px)
══════════════════════════════════════════════════════ */
@media (max-width: 420px) {
    .main .block-container { padding: 0.75rem 0.6rem 75px !important; }
    .royal-title { font-size:22px !important; }
    .meta-badge  { font-size:11px !important; padding:5px 8px !important; }
    .timer-display { font-size:52px !important; }
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════
def streak():
    study = get_study()
    s = 1 if study["study_hours"].get(today, 0) > 0 else 0
    d = date.today() - timedelta(days=1)
    while study["study_hours"].get(str(d), 0) > 0:
        s += 1; d -= timedelta(days=1)
    return s

def header(title):
    uname = get_profile().get("username") or "Scholar"
    st.markdown(f"<div class='royal-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='meta-bar'>
        <div class='meta-badge'>📅 {date.today().strftime('%d %b %Y')}</div>
        <div class='meta-badge'>🔥 {streak()} Day Streak</div>
        <div class='meta-badge'>👑 {uname}</div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    p      = get_profile()
    uname  = p.get("username") or "Scholar"
    av_b64 = p.get("avatar_b64", "")
    if av_b64:
        st.markdown(f"""<div class='sb-profile'>
            <img class='sb-avatar' src='data:image/png;base64,{av_b64}'/>
            <div class='sb-username'>{uname}</div>
            <div class='sb-tagline'>Topper System</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class='sb-profile'>
            <div class='sb-avatar-placeholder'>👑</div>
            <div class='sb-username'>{uname}</div>
            <div class='sb-tagline'>Topper System</div>
        </div>""", unsafe_allow_html=True)
    menu = st.radio("Navigation", [
        "📋 Tasks", "⏱️ Timer", "📊 Tracker", "📅 Calendar", "👤 Profile"
    ])

# ══════════════════════════════════════════════════════════════
#  📋 TASKS
# ══════════════════════════════════════════════════════════════
if menu == "📋 Tasks":
    header("Study Dashboard")
    tasks = get_tasks()

    # Desktop: side-by-side inputs + button | Mobile: stacks automatically
    ca, cb = st.columns([3, 1])
    with ca:
        task = st.text_input("Task Name", key="task_input", placeholder="e.g. Revise Chapter 5…")
        desc = st.text_area("Description (optional)", key="desc_input",
                            placeholder="Add details…", height=85)
    with cb:
        st.write(""); st.write(""); st.write(""); st.write("")
        if st.button("＋  Add Task", use_container_width=True):
            if task.strip():
                tasks.append({"task": task.strip(), "desc": desc.strip(), "done": False})
                st.rerun()

    st.markdown("<div class='section-heading'>✦ Your Tasks</div>", unsafe_allow_html=True)

    if not tasks:
        st.info("No tasks yet — add your first task above 🎯")
    else:
        del_idx = None
        for i, t in enumerate(tasks):
            c1, c2 = st.columns([11, 1])
            with c1:
                chk = st.checkbox(t["task"], value=t["done"], key=f"chk_{i}")
                tasks[i]["done"] = chk
                if t.get("desc"): st.caption(t["desc"])
            with c2:
                if st.button("✕", key=f"del_{i}"): del_idx = i
        if del_idx is not None:
            tasks.pop(del_idx); st.rerun()

    total  = len(tasks)
    done_n = sum(1 for t in tasks if t["done"])
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-heading'>📊 Progress — {done_n} / {total} Completed</div>",
                unsafe_allow_html=True)
    st.progress(done_n / total if total else 0)
    if total > 0 and done_n == total:
        st.balloons()
        st.success("🏆  All tasks completed — You're a Topper today!")

# ══════════════════════════════════════════════════════════════
#  ⏱️ TIMER
# ══════════════════════════════════════════════════════════════
elif menu == "⏱️ Timer":
    header("Focus Timer")

    # Centre column — looks great on both desktop and mobile
    _, cc, _ = st.columns([1, 2, 1])
    with cc:
        work = st.number_input("Work Duration (min)", value=25, min_value=1, key="work_min")
        st.number_input("Break Duration (min)", value=5, min_value=1, key="brk_min")

        if "timer_time" not in st.session_state:
            st.session_state.timer_time = work * 60
            st.session_state.timer_run  = False

        mm     = st.session_state.timer_time // 60
        ss_val = st.session_state.timer_time % 60
        st.markdown(
            f"<div class='timer-wrapper'>"
            f"<div class='timer-display'>{mm:02d}:{ss_val:02d}</div>"
            f"<div class='timer-label'>Focus Session</div></div>",
            unsafe_allow_html=True)

        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("▶  Start", key="btn_start"):
                st.session_state.timer_run = True
        with b2:
            if st.button("⏸  Pause", key="btn_pause"):
                st.session_state.timer_run = False
        with b3:
            if st.button("↺  Reset", key="btn_reset"):
                st.session_state.timer_time = work * 60
                st.session_state.timer_run  = False

    if st.session_state.get("timer_run", False):
        time.sleep(1)
        st.session_state.timer_time -= 1
        if st.session_state.timer_time <= 0:
            study = get_study()
            study["study_hours"][today] = study["study_hours"].get(today, 0) + (work / 60)
            st.session_state.timer_time = work * 60
            st.session_state.timer_run  = False
            st.balloons()
        st.rerun()

# ══════════════════════════════════════════════════════════════
#  📊 TRACKER
# ══════════════════════════════════════════════════════════════
elif menu == "📊 Tracker":
    header("Performance")
    study = get_study()

    _, cc, _ = st.columns([1, 2, 1])
    with cc:
        goal = st.number_input("Daily Goal (hours)", value=int(study["goal"]), min_value=1)
        study["goal"] = goal
        hrs = st.number_input("Add Study Hours", step=0.5, min_value=0.0)
        if st.button("✅  Update Hours", use_container_width=True):
            study["study_hours"][today] = study["study_hours"].get(today, 0) + hrs
            st.success("Hours updated!")
        today_hrs = study["study_hours"].get(today, 0)
        st.markdown(
            f"<div class='section-heading'>Today: {today_hrs:.1f} / {goal} hrs</div>",
            unsafe_allow_html=True)
        st.progress(min(today_hrs / goal, 1.0))

    # Weekly chart — full width
    st.markdown("<div class='section-heading'>📅 This Week</div>", unsafe_allow_html=True)
    days, hrs_list = [], []
    for i in range(6, -1, -1):
        d = date.today() - timedelta(days=i)
        days.append(d.strftime("%a"))
        hrs_list.append(study["study_hours"].get(str(d), 0))
    df = pd.DataFrame({"Day": days, "Hours": hrs_list})
    st.bar_chart(df.set_index("Day"), use_container_width=True)

# ══════════════════════════════════════════════════════════════
#  📅 CALENDAR
# ══════════════════════════════════════════════════════════════
elif menu == "📅 Calendar":
    header("Royal Calendar")
    study  = get_study()
    events = get_events()

    if "cal_year"     not in st.session_state: st.session_state.cal_year     = date.today().year
    if "cal_month"    not in st.session_state: st.session_state.cal_month    = date.today().month
    if "cal_selected" not in st.session_state: st.session_state.cal_selected = None

    cy, cm = st.session_state.cal_year, st.session_state.cal_month

    # Month navigation
    nl, nt, nr = st.columns([1, 4, 1])
    with nl:
        if st.button("◀", key="prev_m"):
            st.session_state.cal_month = 12 if cm == 1 else cm - 1
            if cm == 1: st.session_state.cal_year = cy - 1
            st.session_state.cal_selected = None; st.rerun()
    with nt:
        mn = date(cy, cm, 1).strftime("%B %Y").upper()
        st.markdown(
            f"<div style='text-align:center;font-family:Cinzel,serif;"
            f"font-size:clamp(18px,3vw,26px);font-weight:900;"
            f"background:linear-gradient(135deg,#d4af37,#f5e6b0);"
            f"-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
            f"background-clip:text;letter-spacing:4px;padding:6px 0'>{mn}</div>",
            unsafe_allow_html=True)
    with nr:
        if st.button("▶", key="next_m"):
            st.session_state.cal_month = 1 if cm == 12 else cm + 1
            if cm == 12: st.session_state.cal_year = cy + 1
            st.session_state.cal_selected = None; st.rerun()

    # Build HTML calendar grid
    cal_obj = calendar.Calendar(firstweekday=0)
    weeks   = cal_obj.monthdayscalendar(cy, cm)
    sel_d   = st.session_state.cal_selected

    # Full day names for desktop, single letters adapt via CSS clamp
    DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    hdr  = "".join(f"<div class='ch'>{d}</div>" for d in DAYS)

    cells = ""
    for week in weeks:
        for dn in week:
            if dn == 0:
                cells += "<div class='ce'></div>"; continue
            ds  = f"{cy}-{cm:02d}-{dn:02d}"
            cls = "cd"
            if   ds == sel_d:    cls += " csel"
            elif ds == today:    cls += " ctod"
            elif events.get(ds): cls += " cevt"
            hrs_v   = study["study_hours"].get(ds, 0)
            hrs_lbl = f"<div class='ch_lbl'>{hrs_v:.0f}h</div>" if hrs_v > 0 and ds != sel_d else ""
            dot     = "<div class='cdot'></div>" if events.get(ds) and ds != sel_d else ""
            cells  += f"<div class='{cls}'><span class='cnum'>{dn}</span>{hrs_lbl}{dot}</div>"

    cal_html = f"""<!DOCTYPE html><html><head>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Raleway:wght@400;600&display=swap" rel="stylesheet">
    <style>
      *{{box-sizing:border-box;margin:0;padding:0}}
      body{{background:transparent}}
      @keyframes gp{{
        0%,100%{{box-shadow:0 0 10px rgba(212,175,55,.35)}}
        50%{{box-shadow:0 0 24px rgba(212,175,55,.78)}}
      }}
      .grid{{display:grid;grid-template-columns:repeat(7,1fr);gap:clamp(4px,1vw,8px);padding:2px}}
      .ch{{
        text-align:center;font-weight:700;
        color:rgba(212,175,55,.55);letter-spacing:1.5px;text-transform:uppercase;
        padding:0 0 12px;font-family:Raleway,sans-serif;
        font-size:clamp(9px,1.4vw,12px);
      }}
      .ce{{height:clamp(48px,8vw,72px)}}
      .cd{{
        height:clamp(48px,8vw,72px);border-radius:clamp(8px,1.2vw,12px);
        background:rgba(212,175,55,.04);border:1px solid rgba(212,175,55,.14);
        display:flex;flex-direction:column;align-items:center;justify-content:center;
        transition:all .15s;
      }}
      .cnum{{
        font-family:Cinzel,serif;font-weight:700;color:#c8a84b;line-height:1;
        font-size:clamp(13px,2.2vw,17px);
      }}
      .ch_lbl{{
        font-family:Raleway,sans-serif;font-weight:600;
        color:rgba(212,175,55,.65);margin-top:3px;
        font-size:clamp(7px,1.1vw,10px);
      }}
      .cdot{{
        width:clamp(4px,0.8vw,6px);height:clamp(4px,0.8vw,6px);
        border-radius:50%;background:#d4af37;margin-top:3px;
        box-shadow:0 0 6px rgba(212,175,55,.9);
      }}
      .ctod{{
        background:rgba(212,175,55,.14)!important;
        border:2px solid #d4af37!important;
        box-shadow:0 0 14px rgba(212,175,55,.28)!important;
      }}
      .ctod .cnum{{color:#f5e6b0}}
      .cevt{{
        background:linear-gradient(135deg,rgba(212,175,55,.18),rgba(184,134,11,.07))!important;
        border:2px solid rgba(212,175,55,.8)!important;
        animation:gp 2.5s ease-in-out infinite;
      }}
      .cevt .cnum{{color:#f5e6b0}}
      .csel{{
        background:linear-gradient(135deg,#b8860b,#d4af37)!important;
        border:2px solid #f5e6b0!important;
        box-shadow:0 4px 20px rgba(212,175,55,.65)!important;
      }}
      .csel .cnum{{color:#0a0800;font-weight:900}}
    </style></head><body>
    <div class="grid">{hdr}{cells}</div>
    </body></html>"""

    components.html(cal_html, height=len(weeks) * 80 + 55, scrolling=False)

    # Date selector dropdown
    all_days = [f"{cy}-{cm:02d}-{dn:02d}" for w in weeks for dn in w if dn > 0]
    opts = ["— select a date —"] + [
        date.fromisoformat(d).strftime("%d %B")
        + (" ✦" if events.get(d) else "")
        + (f" · {study['study_hours'][d]:.0f}h" if study["study_hours"].get(d, 0) > 0 else "")
        for d in all_days
    ]
    st.markdown(
        "<div style='font-size:11px;color:rgba(212,175,55,.45);letter-spacing:2px;"
        "text-transform:uppercase;margin:12px 0 6px;'>✦ Select a date for details</div>",
        unsafe_allow_html=True)
    picked = st.selectbox("", opts, key="cal_picker", label_visibility="collapsed")
    if picked != "— select a date —":
        idx = opts.index(picked) - 1
        new_sel = all_days[idx]
        if new_sel != st.session_state.cal_selected:
            st.session_state.cal_selected = new_sel; st.rerun()
        sel_d = new_sel

    # Day detail panel
    sel = st.session_state.cal_selected
    if sel:
        sel_label = date.fromisoformat(sel).strftime("%A, %d %B %Y")
        sel_hrs   = study["study_hours"].get(sel, 0)
        sel_evts  = events.get(sel, [])

        st.markdown(f"<div class='section-heading'>✦ {sel_label}</div>", unsafe_allow_html=True)

        # Desktop: two columns | Mobile: single column stacked
        dl, dr = st.columns([3, 2])
        with dl:
            st.markdown(f"<div class='hrs-badge'>{sel_hrs:.1f} hrs studied</div>",
                        unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if sel_evts:
                st.markdown(
                    "<div style='font-size:11px;color:rgba(212,175,55,.55);"
                    "letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;'>Events</div>",
                    unsafe_allow_html=True)
                st.markdown(
                    "".join(f"<span class='event-chip'>✦ {e}</span>" for e in sel_evts),
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    "<div style='font-size:13px;color:rgba(212,175,55,.35);'>No events yet — add one →</div>",
                    unsafe_allow_html=True)

        with dr:
            new_evt = st.text_input("Add Event", key=f"evt_{sel}",
                                    placeholder="e.g. Physics Test…")
            if st.button("＋ Add Event", key=f"add_evt_{sel}", use_container_width=True):
                if new_evt.strip():
                    events.setdefault(sel, []).append(new_evt.strip()); st.rerun()

            add_hrs = st.number_input("Log Study Hours", step=0.5, min_value=0.0, key=f"hrs_{sel}")
            if st.button("✅ Log Hours", key=f"log_hrs_{sel}", use_container_width=True):
                study["study_hours"][sel] = study["study_hours"].get(sel, 0) + add_hrs; st.rerun()

            if sel_evts:
                del_evt = st.selectbox("Remove event", ["—"] + sel_evts, key=f"del_{sel}")
                if del_evt != "—":
                    if st.button("🗑 Remove", key=f"rm_{sel}", use_container_width=True):
                        events[sel].remove(del_evt)
                        if not events[sel]: del events[sel]
                        st.rerun()

# ══════════════════════════════════════════════════════════════
#  👤 PROFILE
# ══════════════════════════════════════════════════════════════
elif menu == "👤 Profile":
    header("My Profile")
    profile = get_profile()
    study   = get_study()
    tasks   = get_tasks()
    events  = get_events()

    # Centre on desktop, full width on mobile
    _, cc, _ = st.columns([1, 2, 1])
    with cc:
        av_b64 = profile.get("avatar_b64", "")
        if av_b64:
            st.markdown(
                f"<img class='profile-avatar-big' src='data:image/png;base64,{av_b64}'/>",
                unsafe_allow_html=True)
        else:
            st.markdown(
                "<div style='text-align:center;font-size:80px;margin-bottom:14px;'>👑</div>",
                unsafe_allow_html=True)
        new_name = st.text_input("Username", value=profile.get("username", ""),
                                 placeholder="Enter your name…")
        uploaded = st.file_uploader("Upload Avatar Photo",
                                    type=["png", "jpg", "jpeg", "webp"])
        if st.button("💾  Save Profile", use_container_width=True):
            if new_name.strip(): profile["username"] = new_name.strip()
            if uploaded: profile["avatar_b64"] = base64.b64encode(uploaded.read()).decode()
            st.success("Profile saved! ✦"); st.rerun()

    st.markdown(
        "<div class='section-heading' style='text-align:center;margin-top:32px;'>✦ Your Stats</div>",
        unsafe_allow_html=True)

    # 4 columns on desktop, 2x2 on mobile (CSS handles this)
    s1, s2, s3, s4 = st.columns(4)
    for col, num, lbl in [
        (s1, f"{sum(study['study_hours'].values()):.1f}", "Total Hours"),
        (s2, streak(),                                    "Day Streak"),
        (s3, sum(1 for t in tasks if t["done"]),          "Tasks Done"),
        (s4, sum(len(v) for v in events.values()),        "Events"),
    ]:
        col.markdown(
            f"<div class='profile-stat-box'>"
            f"<div class='profile-stat-num'>{num}</div>"
            f"<div class='profile-stat-label'>{lbl}</div></div>",
            unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  AD BAR
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class='ad-bar'>
  <!-- PASTE YOUR GOOGLE ADSENSE CODE HERE AFTER APPROVAL -->
  <span style="color:#d4af37;font-size:11px;font-weight:600;
               letter-spacing:2.5px;text-transform:uppercase;">
    ✦ &nbsp; Your Ad Here &nbsp;|&nbsp; Topper System 👑 &nbsp; ✦
  </span>
</div>
""", unsafe_allow_html=True)
