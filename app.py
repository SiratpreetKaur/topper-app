"""
👑 TOPPER SYSTEM — Deployment-Ready Version
Storage: st.session_state (per-user, in-memory, works on any cloud host)
For persistence across sessions → connect Supabase (see README.md)
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
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════
#  SESSION STATE STORAGE  (safe for cloud deployment)
#  All data lives per-browser-session — no shared files
# ══════════════════════════════════════════════════════
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

# Shorthand accessors
def get_tasks():   return st.session_state["tasks"]
def get_study():   return st.session_state["study"]
def get_events():  return st.session_state["events"]
def get_profile(): return st.session_state["profile"]

today = str(date.today())

# ══════════════════════════════════════════════════════
#  ROYAL GOLD CSS
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Cormorant+Garamond:wght@600;700&family=Raleway:wght@300;400;500;600;700&display=swap');

* { font-family:'Raleway',sans-serif; box-sizing:border-box; }

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse at 15% 60%,rgba(180,140,0,.18) 0%,transparent 55%),
        radial-gradient(ellipse at 85% 15%,rgba(212,175,55,.14) 0%,transparent 50%),
        linear-gradient(160deg,#080600 0%,#100e00 45%,#181200 100%);
    color:#f5e6b0; min-height:100vh;
}
[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#0a0800 0%,#141000 100%) !important;
    border-right:1px solid rgba(212,175,55,.25) !important;
}
[data-testid="stSidebar"] * { color:#d4af37 !important; }
#MainMenu,footer,header { visibility:hidden; }
.stDeployButton { display:none; }

.sb-profile {
    background:linear-gradient(135deg,rgba(212,175,55,.12),rgba(212,175,55,.04));
    border:1px solid rgba(212,175,55,.35); border-radius:16px;
    padding:18px 14px 14px; margin:10px 0 20px; text-align:center;
}
.sb-avatar { width:72px;height:72px;border-radius:50%;border:2px solid #d4af37;
    object-fit:cover;margin-bottom:8px;box-shadow:0 0 18px rgba(212,175,55,.3); }
.sb-avatar-placeholder { width:72px;height:72px;border-radius:50%;
    border:2px dashed rgba(212,175,55,.5);background:rgba(212,175,55,.08);
    display:inline-flex;align-items:center;justify-content:center;
    font-size:32px;margin-bottom:8px; }
.sb-username { font-family:'Cinzel',serif;font-size:15px;font-weight:700;
    color:#f5e6b0 !important;letter-spacing:1.5px; }
.sb-tagline  { font-size:11px;color:rgba(212,175,55,.6) !important;
    letter-spacing:1px;text-transform:uppercase;margin-top:3px; }

.royal-title {
    font-family:'Cinzel',serif;font-size:46px;font-weight:900;text-align:center;
    background:linear-gradient(135deg,#d4af37 0%,#f5e6b0 50%,#b8860b 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;letter-spacing:3px;margin-bottom:4px;
}
.gold-divider { width:80px;height:2px;
    background:linear-gradient(90deg,transparent,#d4af37,transparent);
    margin:6px auto 18px; }
.meta-bar { display:flex;justify-content:center;gap:24px;align-items:center;
    margin:4px 0 26px;flex-wrap:wrap; }
.meta-badge { font-family:'Cormorant Garamond',serif;font-size:19px;font-weight:700;
    color:#f5e6b0;background:linear-gradient(135deg,rgba(212,175,55,.15),rgba(212,175,55,.04));
    border:1px solid rgba(212,175,55,.4);padding:9px 26px;border-radius:50px; }
.section-heading { font-family:'Cinzel',serif;font-size:20px;font-weight:700;
    color:#d4af37;letter-spacing:2px;margin:22px 0 14px; }

.timer-wrapper { background:linear-gradient(135deg,rgba(212,175,55,.1),rgba(0,0,0,.3));
    border:2px solid rgba(212,175,55,.4);border-radius:24px;
    padding:44px 20px 40px;margin:20px 0 32px;text-align:center;
    box-shadow:0 0 60px rgba(212,175,55,.08); }
.timer-display { font-family:'Cinzel',serif;font-size:108px;font-weight:900;
    background:linear-gradient(135deg,#d4af37 0%,#f5e6b0 50%,#b8860b 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;letter-spacing:6px;line-height:1; }
.timer-label { font-size:11px;color:rgba(212,175,55,.6);letter-spacing:4px;
    text-transform:uppercase;margin-top:10px; }

.event-chip { display:inline-block;
    background:linear-gradient(135deg,rgba(212,175,55,.2),rgba(184,134,11,.1));
    border:1px solid rgba(212,175,55,.45);border-radius:20px;
    padding:5px 14px;font-size:13px;color:#f5e6b0;margin:4px 4px 4px 0;
    box-shadow:0 0 8px rgba(212,175,55,.15); }
.hrs-badge { font-family:'Cinzel',serif;font-size:36px;font-weight:900;
    background:linear-gradient(135deg,#d4af37,#f5e6b0);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text; }

.profile-avatar-big { width:130px;height:130px;border-radius:50%;
    border:3px solid #d4af37;object-fit:cover;
    box-shadow:0 0 40px rgba(212,175,55,.35);display:block;margin:0 auto 16px; }
.profile-stat-box { background:linear-gradient(135deg,rgba(212,175,55,.1),rgba(0,0,0,.2));
    border:1px solid rgba(212,175,55,.3);border-radius:14px;
    padding:18px;text-align:center; }
.profile-stat-num { font-family:'Cinzel',serif;font-size:32px;font-weight:900;
    background:linear-gradient(135deg,#d4af37,#f5e6b0);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text; }
.profile-stat-label { font-size:11px;color:rgba(212,175,55,.6);
    letter-spacing:2px;text-transform:uppercase;margin-top:4px; }

.stButton>button {
    background:linear-gradient(135deg,#b8860b,#d4af37) !important;
    color:#0a0800 !important;border:none !important;border-radius:10px !important;
    font-family:'Raleway',sans-serif !important;font-weight:700 !important;
    font-size:14px !important;padding:12px 20px !important;
    letter-spacing:1px !important;text-transform:uppercase !important;
    transition:all .2s !important;width:100% !important;
}
.stButton>button:hover {
    background:linear-gradient(135deg,#d4af37,#f5e6b0) !important;
    box-shadow:0 4px 20px rgba(212,175,55,.35) !important;
    transform:translateY(-2px) !important;
}

.stTextInput>div>div>input,
.stTextArea>div>div>textarea,
.stNumberInput>div>div>input {
    background:#1a1500 !important;
    border:1px solid rgba(212,175,55,.45) !important;
    border-radius:10px !important;color:#f5e6b0 !important;
    font-size:15px !important;caret-color:#d4af37;
}
.stTextInput>div>div>input::placeholder,
.stTextArea>div>div>textarea::placeholder { color:rgba(212,175,55,.35) !important; }
.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus {
    border-color:#d4af37 !important;
    box-shadow:0 0 0 2px rgba(212,175,55,.25) !important;
    background:#211c00 !important;
}
[data-baseweb="select"]>div { background:#1a1500 !important;border-color:rgba(212,175,55,.45) !important; }
[data-baseweb="popover"],[data-baseweb="menu"] { background:#1a1500 !important; }
[data-baseweb="option"] { background:#1a1500 !important;color:#f5e6b0 !important; }

label[data-testid="stWidgetLabel"] p,
label[data-testid="stWidgetLabel"] {
    font-weight:600 !important;font-size:12px !important;
    color:rgba(212,175,55,.8) !important;text-transform:uppercase !important;
    letter-spacing:1.5px !important;
}

.stProgress>div>div>div>div {
    background:linear-gradient(90deg,#b8860b,#d4af37,#f5e6b0) !important;
    border-radius:100px !important;
}
.stProgress>div>div>div { background:rgba(212,175,55,.12) !important;
    border-radius:100px !important;height:10px !important; }

.stCheckbox label p { font-size:16px !important;font-weight:500 !important;color:#f5e6b0 !important; }
div[data-testid="stCaptionContainer"] p { color:rgba(212,175,55,.55) !important;font-size:13px !important; }
div[data-testid="stNotificationContent"] { background:rgba(212,175,55,.1) !important;color:#f5e6b0 !important; }
.stNumberInput button { background:rgba(212,175,55,.15) !important;
    border:1px solid rgba(212,175,55,.3) !important;color:#d4af37 !important;
    width:auto !important;padding:6px 12px !important;
    text-transform:none !important;letter-spacing:0 !important;font-size:16px !important; }
[data-testid="stFileUploader"] { border:1px dashed rgba(212,175,55,.4) !important;
    border-radius:12px !important;background:rgba(212,175,55,.05) !important; }
[data-testid="stFileUploader"] * { color:rgba(212,175,55,.8) !important; }

.main .block-container { padding-bottom:70px !important; }

/* ── Google AdSense placeholder bar ── */
.ad-bar { position:fixed;bottom:0;left:0;width:100%;z-index:9999;
    background:linear-gradient(90deg,#080600,#141000,#080600);
    border-top:1px solid rgba(212,175,55,.25);
    padding:0; min-height:60px;
    display:flex;align-items:center;justify-content:center; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════
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
        <div class='meta-badge'>📅 &nbsp;{date.today().strftime('%A, %d %B %Y')}</div>
        <div class='meta-badge'>🔥 &nbsp;{streak()} Day Streak</div>
        <div class='meta-badge'>👑 &nbsp;{uname}</div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════
with st.sidebar:
    p      = get_profile()
    uname  = p.get("username") or "Scholar"
    av_b64 = p.get("avatar_b64", "")
    if av_b64:
        st.markdown(f"<div class='sb-profile'><img class='sb-avatar' src='data:image/png;base64,{av_b64}'/><div class='sb-username'>{uname}</div><div class='sb-tagline'>Topper System</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='sb-profile'><div class='sb-avatar-placeholder'>👑</div><div class='sb-username'>{uname}</div><div class='sb-tagline'>Topper System</div></div>", unsafe_allow_html=True)
    menu = st.radio("Navigation", ["📋 Tasks", "⏱️ Timer", "📊 Tracker", "📅 Calendar", "👤 Profile"])

# ══════════════════════════════════════════════════════
#  📋 TASKS
# ══════════════════════════════════════════════════════
if menu == "📋 Tasks":
    header("Study Dashboard")
    tasks = get_tasks()

    ca, cb = st.columns([3, 1])
    with ca:
        task = st.text_input("Task Name", key="task_input", placeholder="e.g. Revise Chapter 5…")
        desc = st.text_area("Description (optional)", key="desc_input", placeholder="Add details…", height=90)
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
            c1, c2 = st.columns([12, 1])
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
    st.markdown(f"<div class='section-heading'>📊 Progress — {done_n} / {total} Completed</div>", unsafe_allow_html=True)
    st.progress(done_n / total if total else 0)
    if total > 0 and done_n == total:
        st.balloons()
        st.success("🏆  All tasks completed — You're a Topper today!")

# ══════════════════════════════════════════════════════
#  ⏱️ TIMER
# ══════════════════════════════════════════════════════
elif menu == "⏱️ Timer":
    header("Focus Timer")
    _, cc, _ = st.columns([1, 2, 1])
    with cc:
        work = st.number_input("Work Duration (min)", value=25, min_value=1, key="work_min")
        st.number_input("Break Duration (min)", value=5, min_value=1, key="brk_min")
        if "timer_time" not in st.session_state:
            st.session_state.timer_time = work * 60
            st.session_state.timer_run  = False
        mm = st.session_state.timer_time // 60
        ss_val = st.session_state.timer_time % 60
        st.markdown(f"<div class='timer-wrapper'><div class='timer-display'>{mm:02d}:{ss_val:02d}</div><div class='timer-label'>Focus Session</div></div>", unsafe_allow_html=True)
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("▶  Start", key="btn_start"): st.session_state.timer_run = True
        with b2:
            if st.button("⏸  Pause", key="btn_pause"): st.session_state.timer_run = False
        with b3:
            if st.button("↺  Reset", key="btn_reset"):
                st.session_state.timer_time = work * 60; st.session_state.timer_run = False
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

# ══════════════════════════════════════════════════════
#  📊 TRACKER
# ══════════════════════════════════════════════════════
elif menu == "📊 Tracker":
    header("Performance")
    study = get_study()
    _, cc, _ = st.columns([1, 2, 1])
    with cc:
        goal = st.number_input("Daily Goal (hours)", value=int(study["goal"]), min_value=1)
        study["goal"] = goal
        hrs = st.number_input("Add Study Hours", step=0.5, min_value=0.0)
        if st.button("✅  Update Hours"):
            study["study_hours"][today] = study["study_hours"].get(today, 0) + hrs
            st.success("Hours updated!")
        today_hrs = study["study_hours"].get(today, 0)
        st.markdown(f"<div class='section-heading'>Today: {today_hrs:.1f} / {goal} hrs</div>", unsafe_allow_html=True)
        st.progress(min(today_hrs / goal, 1.0))

# ══════════════════════════════════════════════════════
#  📅 CALENDAR
# ══════════════════════════════════════════════════════
elif menu == "📅 Calendar":
    header("Royal Calendar")
    study  = get_study()
    events = get_events()

    if "cal_year"     not in st.session_state: st.session_state.cal_year     = date.today().year
    if "cal_month"    not in st.session_state: st.session_state.cal_month    = date.today().month
    if "cal_selected" not in st.session_state: st.session_state.cal_selected = None

    cy, cm = st.session_state.cal_year, st.session_state.cal_month

    nl, nt, nr = st.columns([1, 4, 1])
    with nl:
        if st.button("◀", key="prev_m"):
            st.session_state.cal_month = 12 if cm == 1 else cm - 1
            if cm == 1: st.session_state.cal_year = cy - 1
            st.session_state.cal_selected = None; st.rerun()
    with nt:
        mn = date(cy, cm, 1).strftime("%B %Y").upper()
        st.markdown(f"<div style='text-align:center;font-family:Cinzel,serif;font-size:24px;font-weight:900;"
                    f"background:linear-gradient(135deg,#d4af37,#f5e6b0);-webkit-background-clip:text;"
                    f"-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:4px;padding:6px 0'>{mn}</div>",
                    unsafe_allow_html=True)
    with nr:
        if st.button("▶", key="next_m"):
            st.session_state.cal_month = 1 if cm == 12 else cm + 1
            if cm == 12: st.session_state.cal_year = cy + 1
            st.session_state.cal_selected = None; st.rerun()

    cal_obj = calendar.Calendar(firstweekday=0)
    weeks   = cal_obj.monthdayscalendar(cy, cm)
    sel_d   = st.session_state.cal_selected
    DAYS    = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

    hdr = "".join(f"<div class='ch'>{d}</div>" for d in DAYS)
    cells = ""
    for week in weeks:
        for dn in week:
            if dn == 0:
                cells += "<div class='ce'></div>"; continue
            ds  = f"{cy}-{cm:02d}-{dn:02d}"
            cls = "cd"
            if   ds == sel_d:          cls += " csel"
            elif ds == today:           cls += " ctod"
            elif events.get(ds):        cls += " cevt"
            hrs_v   = study["study_hours"].get(ds, 0)
            hrs_lbl = f"<div class='ch_lbl'>{hrs_v:.0f}h</div>" if hrs_v > 0 and ds != sel_d else ""
            dot     = "<div class='cdot'></div>" if events.get(ds) and ds != sel_d else ""
            cells  += f"<div class='{cls}'><span class='cnum'>{dn}</span>{hrs_lbl}{dot}</div>"

    cal_html = f"""<!DOCTYPE html><html><head>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Raleway:wght@400;600&display=swap" rel="stylesheet">
    <style>
      *{{box-sizing:border-box;margin:0;padding:0}}
      body{{background:transparent}}
      @keyframes gp{{
        0%,100%{{box-shadow:0 0 10px rgba(212,175,55,.35),0 0 20px rgba(212,175,55,.1)}}
        50%{{box-shadow:0 0 22px rgba(212,175,55,.75),0 0 40px rgba(212,175,55,.25)}}
      }}
      .grid{{display:grid;grid-template-columns:repeat(7,1fr);gap:7px;padding:4px}}
      .ch{{text-align:center;font-size:11px;font-weight:700;color:rgba(212,175,55,.55);
           letter-spacing:2px;text-transform:uppercase;padding:0 0 12px;font-family:Raleway,sans-serif}}
      .ce{{height:68px}}
      .cd{{height:68px;border-radius:12px;background:rgba(212,175,55,.04);
           border:1px solid rgba(212,175,55,.14);display:flex;flex-direction:column;
           align-items:center;justify-content:center;position:relative;}}
      .cnum{{font-family:Cinzel,serif;font-size:16px;font-weight:700;color:#c8a84b;line-height:1}}
      .ch_lbl{{font-family:Raleway,sans-serif;font-size:9px;font-weight:600;
               color:rgba(212,175,55,.65);margin-top:4px;letter-spacing:.3px}}
      .cdot{{width:5px;height:5px;border-radius:50%;background:#d4af37;
             margin-top:4px;box-shadow:0 0 6px rgba(212,175,55,.9)}}
      .ctod{{background:rgba(212,175,55,.14)!important;border:2px solid #d4af37!important;
             box-shadow:0 0 16px rgba(212,175,55,.25)!important}}
      .ctod .cnum{{color:#f5e6b0}}
      .cevt{{background:linear-gradient(135deg,rgba(212,175,55,.18),rgba(184,134,11,.07))!important;
             border:2px solid rgba(212,175,55,.78)!important;animation:gp 2.5s ease-in-out infinite}}
      .cevt .cnum{{color:#f5e6b0}}
      .csel{{background:linear-gradient(135deg,#b8860b,#d4af37)!important;
             border:2px solid #f5e6b0!important;box-shadow:0 4px 24px rgba(212,175,55,.6)!important}}
      .csel .cnum{{color:#0a0800;font-weight:900}}
    </style></head><body>
    <div class="grid">{hdr}{cells}</div>
    </body></html>"""

    components.html(cal_html, height=len(weeks) * 78 + 52, scrolling=False)

    all_days = [f"{cy}-{cm:02d}-{dn:02d}" for w in weeks for dn in w if dn > 0]
    opts = ["— select a date —"] + [
        date.fromisoformat(d).strftime("%d %B")
        + (" ✦" if events.get(d) else "")
        + (f" · {study['study_hours'][d]:.0f}h" if study["study_hours"].get(d, 0) > 0 else "")
        for d in all_days
    ]
    st.markdown("<div style='font-size:11px;color:rgba(212,175,55,.45);letter-spacing:2px;"
                "text-transform:uppercase;margin:12px 0 6px;'>✦ Select a date for details</div>",
                unsafe_allow_html=True)
    picked = st.selectbox("", opts, key="cal_picker", label_visibility="collapsed")
    if picked != "— select a date —":
        idx = opts.index(picked) - 1
        new_sel = all_days[idx]
        if new_sel != st.session_state.cal_selected:
            st.session_state.cal_selected = new_sel; st.rerun()
        sel_d = new_sel

    sel = st.session_state.cal_selected
    if sel:
        sel_label = date.fromisoformat(sel).strftime("%A, %d %B %Y")
        sel_hrs   = study["study_hours"].get(sel, 0)
        sel_evts  = events.get(sel, [])
        st.markdown(f"<div class='section-heading'>✦ {sel_label}</div>", unsafe_allow_html=True)
        dl, dr = st.columns([3, 2])
        with dl:
            st.markdown(f"<div class='hrs-badge'>{sel_hrs:.1f} hrs</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:11px;color:rgba(212,175,55,.55);letter-spacing:2px;text-transform:uppercase;'>Studied</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if sel_evts:
                st.markdown("<div style='font-size:11px;color:rgba(212,175,55,.55);letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;'>Events</div>", unsafe_allow_html=True)
                st.markdown("".join(f"<span class='event-chip'>✦ {e}</span>" for e in sel_evts), unsafe_allow_html=True)
            else:
                st.markdown("<div style='font-size:13px;color:rgba(212,175,55,.35);'>No events yet — add one →</div>", unsafe_allow_html=True)
        with dr:
            new_evt = st.text_input("Add Event", key=f"evt_{sel}", placeholder="e.g. Physics Test…")
            if st.button("＋ Add Event", key=f"add_evt_{sel}"):
                if new_evt.strip():
                    events.setdefault(sel, []).append(new_evt.strip()); st.rerun()
            add_hrs = st.number_input("Log Study Hours", step=0.5, min_value=0.0, key=f"hrs_{sel}")
            if st.button("✅ Log Hours", key=f"log_hrs_{sel}"):
                study["study_hours"][sel] = study["study_hours"].get(sel, 0) + add_hrs; st.rerun()
            if sel_evts:
                del_evt = st.selectbox("Remove event", ["—"] + sel_evts, key=f"del_{sel}")
                if del_evt != "—":
                    if st.button("🗑 Remove", key=f"rm_{sel}"):
                        events[sel].remove(del_evt)
                        if not events[sel]: del events[sel]
                        st.rerun()

# ══════════════════════════════════════════════════════
#  👤 PROFILE
# ══════════════════════════════════════════════════════
elif menu == "👤 Profile":
    header("My Profile")
    profile = get_profile()
    study   = get_study()
    tasks   = get_tasks()
    events  = get_events()

    _, cc, _ = st.columns([1, 2, 1])
    with cc:
        av_b64 = profile.get("avatar_b64", "")
        if av_b64:
            st.markdown(f"<img class='profile-avatar-big' src='data:image/png;base64,{av_b64}'/>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='text-align:center;font-size:80px;margin-bottom:16px;'>👑</div>", unsafe_allow_html=True)
        new_name = st.text_input("Username", value=profile.get("username", ""), placeholder="Enter your name…")
        uploaded = st.file_uploader("Upload Avatar", type=["png", "jpg", "jpeg", "webp"])
        if st.button("💾  Save Profile"):
            if new_name.strip(): profile["username"] = new_name.strip()
            if uploaded: profile["avatar_b64"] = base64.b64encode(uploaded.read()).decode()
            st.success("Profile saved! ✦"); st.rerun()

    st.markdown("<div class='section-heading' style='text-align:center;'>✦ Your Stats</div>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    for col, num, lbl in [
        (s1, f"{sum(study['study_hours'].values()):.1f}", "Total Hours"),
        (s2, streak(), "Day Streak"),
        (s3, sum(1 for t in tasks if t["done"]), "Tasks Done"),
        (s4, sum(len(v) for v in events.values()), "Events"),
    ]:
        col.markdown(f"<div class='profile-stat-box'><div class='profile-stat-num'>{num}</div><div class='profile-stat-label'>{lbl}</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  GOOGLE ADSENSE BAR
#  Replace the placeholder below with your actual
#  AdSense <script> tag once your site is approved.
#  Format:  <ins class="adsbygoogle" ...></ins>
# ══════════════════════════════════════════════════════
st.markdown("""
<div class='ad-bar'>
  <!-- PASTE YOUR GOOGLE ADSENSE CODE HERE AFTER APPROVAL -->
  <!-- Example:
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>
  <ins class="adsbygoogle" style="display:inline-block;width:728px;height:60px"
       data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  -->
  <span style="color:#d4af37;font-size:11px;font-weight:600;letter-spacing:2.5px;text-transform:uppercase;">
    ✦ &nbsp; Your Ad Here &nbsp;|&nbsp; Topper System 👑 &nbsp; ✦
  </span>
</div>
""", unsafe_allow_html=True)