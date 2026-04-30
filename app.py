import streamlit as st
import json
import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objects as go
from openai import OpenAI

st.set_page_config(page_title="MirrorMind Digital Twin", layout="wide")

# =========================
# LOAD DATA
# =========================
with open("user_profile.json", "r", encoding="utf-8") as f:
    profile = json.load(f)

jobs = pd.read_csv("jobs_dataset.csv")

if os.path.exists("agent_output.md"):
    with open("agent_output.md", "r", encoding="utf-8") as f:
        agent_output = f.read()
else:
    agent_output = "No Antigravity agent output found yet."


client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)
# =========================
# ML CAREER MATCHING
# =========================
user_text = " ".join(profile["hard_skills"] + profile["soft_skills"] + profile["interests"])
corpus = [user_text] + jobs["skills"].tolist()

vectorizer = CountVectorizer()
vectors = vectorizer.fit_transform(corpus)
similarities = cosine_similarity(vectors[0], vectors[1:]).flatten()

results = []
user_skills_lower = set(skill.lower() for skill in profile["hard_skills"])

for i, row in jobs.iterrows():
    job = row["job_title"]
    skills = row["skills"].split()
    missing = [skill for skill in skills if skill.lower() not in user_skills_lower]

    results.append({
        "job": job,
        "score": round(float(similarities[i]) * 100, 2),
        "missing_skills": missing[:5]
    })

results = sorted(results, key=lambda x: x["score"], reverse=True)
top3 = results[:3]
best_role = top3[0]["job"]
next_unlock = top3[0]["missing_skills"][0] if top3[0]["missing_skills"] else "Portfolio Polish"

# =========================
# IDENTITY LOGIC
# =========================
if "3D Modeling" in profile["hard_skills"] or "VR" in profile["hard_skills"]:
    character_class = "Immersive AI Explorer"
    class_desc = "A hybrid creator blending visual thinking, immersive media, and future-facing technology."
elif "Graphic Design" in profile["hard_skills"] or "UI UX" in profile["hard_skills"]:
    character_class = "Creative Interface Architect"
    class_desc = "A visual strategist shaping future digital experiences through design and AI."
else:
    character_class = "Creative AI Explorer"
    class_desc = "A multidisciplinary builder connecting creativity, technology, and experimentation."

portfolio_ideas = [
    "AI-powered moodboard generator",
    "VR gallery concept",
    "AI assistant interface redesign",
    "Interactive futuristic portfolio homepage",
]

quests = [
    {"title": "Build one polished portfolio case study", "status": "Unlocked"},
    {"title": "Learn advanced Figma workflows", "status": "In Progress"},
    {"title": "Try Unity basics for interactive design", "status": "Locked"},
    {"title": "Prototype one AI + design project", "status": "Unlocked"},
]

pages = [
    "Identity",
    "Character",
    "Future Paths",
    "Skill Aura",
    "Quest Line",
    "Twin Chat",
    "Agent Resources",
    "Wrapped",
    "About Project"
]

if "page" not in st.session_state:
    st.session_state.page = "Identity"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi Mairam. I’m MirrorMind — your free AI-style digital twin. Ask me about your career path, missing skills, portfolio, resources, or roast mode."
        }
    ]

# =========================
# HELPERS
# =========================
def set_page(page_name):
    st.session_state.page = page_name

def is_active(page_name):
    return st.session_state.page == page_name

def render_pills(items, css_class):
    html = '<div class="pill-grid">'
    for item in items:
        html += f'<span class="{css_class}">{item}</span>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def get_missing_skills():
    if top3 and top3[0]["missing_skills"]:
        return top3[0]["missing_skills"]
    return ["portfolio polish", "project documentation"]

def smart_free_reply(prompt, mode):
    text = prompt.lower()
    missing = get_missing_skills()
    missing_text = ", ".join(missing[:3])

    profile_summary = (
        f"{profile['name']} has hard skills in {', '.join(profile['hard_skills'])}, "
        f"soft skills in {', '.join(profile['soft_skills'])}, and interests in {', '.join(profile['interests'])}."
    )

    # ROAST MODE has priority
    if mode == "Roast":
        if "portfolio" in text:
            return (
                "Brutally honest? Your ideas are strong, but a portfolio is not built from imagination alone. "
                "Pick ONE concept, finish it, document it, and stop collecting new tabs like they are achievements."
            )
        if "skill" in text or "learn" in text:
            return (
                f"Your next skill unlock is **{missing_text}**. The roast: you do not need 47 tutorials. "
                "You need one tutorial, one mini-project, and the emotional strength to actually finish it."
            )
        if "role" in text or "career" in text or "job" in text:
            return (
                f"Your best role direction is **{best_role}**. But right now the gap is not potential — it is proof. "
                "Talent is cute. Finished projects are employable."
            )
        return (
            f"You are clearly creative and future-facing, but MirrorMind is detecting a dangerous level of "
            f"'I have an idea' energy. Convert it into one finished project related to **{best_role}**."
        )

    # RESOURCE QUESTIONS
    if "resource" in text or "github" in text or "learn" in text or "tutorial" in text or "course" in text:
        return (
            f"Based on your Antigravity Agent output and ML prediction, your next learning focus should be **{missing_text}**.\n\n"
            f"Recommended path:\n"
            f"1. Learn the basics of **{missing[0]}**.\n"
            f"2. Find a beginner GitHub project related to **{best_role}**.\n"
            f"3. Build a small portfolio prototype.\n"
            f"4. Write a case study explaining your process.\n\n"
            f"Agent Layer note: check the **Agent Resources** page for the Antigravity-generated action plan."
        )

    # CAREER QUESTIONS
    if "career" in text or "role" in text or "job" in text or "future" in text:
        if mode == "Strategist":
            return (
                f"Strategic answer: your strongest current path is **{best_role}**.\n\n"
                f"Why: {profile_summary}\n\n"
                f"Your next move should be:\n"
                f"- Target one role: **{best_role}**\n"
                f"- Close skill gaps: **{missing_text}**\n"
                f"- Build 2 proof-based portfolio projects\n"
                f"- Use your design + AI + immersive media direction as your personal brand."
            )
        return (
            f"Your strongest predicted career path is **{best_role}**. "
            f"This fits because your profile combines creativity, visual communication, AI interest, and immersive media. "
            f"Your next unlock is **{next_unlock}**."
        )

    # SKILL QUESTIONS
    if "skill" in text or "missing" in text or "gap" in text or "improve" in text:
        return (
            f"Your main missing skills are **{missing_text}**.\n\n"
            f"I recommend this order:\n"
            f"1. Learn **{missing[0]}** first.\n"
            f"2. Apply it in a small project.\n"
            f"3. Document the project as a portfolio case study.\n"
            f"4. Then move to the next missing skill."
        )

    # PORTFOLIO QUESTIONS
    if "portfolio" in text or "project" in text or "build" in text:
        ideas = "\n".join([f"- {idea}" for idea in portfolio_ideas])
        return (
            f"For your profile, the portfolio should prove that you are not just creative, but also execution-focused.\n\n"
            f"Best project ideas:\n{ideas}\n\n"
            f"My top recommendation: build an **AI assistant interface redesign** or a **VR gallery concept**."
        )

    # ABOUT PROJECT QUESTIONS
    if "explain" in text or "what is this" in text or "project" in text:
        return (
            "MirrorMind is a Digital Twin Career Engine. It analyzes your profile, predicts career paths using ML, "
            "maps missing skills, generates a growth roadmap, and includes an Antigravity Agent output for learning resources."
        )

    # SEMESTER / WRAPPED QUESTIONS
    if "wrapped" in text or "semester" in text:
        return (
            f"Your Semester Wrapped summary: your strongest direction is **creative technology**. "
            f"Your top strength is creativity, your best role match is **{best_role}**, and your next skill unlock is **{next_unlock}**."
        )

    # DEFAULT
    if mode == "Strategist":
        return (
            f"Strategic summary: position yourself as **{character_class}**, target **{best_role}**, "
            f"learn **{missing_text}**, and build one polished case study this month."
        )

    return (
        f"Based on your digital twin profile, I would guide you toward **{best_role}**. "
        f"Your strongest identity is **{character_class}**, and your next growth step is **{next_unlock}**."
    )

# =========================

def lmstudio_reply(prompt, mode):
    text = prompt.strip().lower()
    if text in ["hi", "hello", "hey", "привет", "сәлем"]:
        return "Hey 👋 I’m MirrorMind, your AI digital twin. Ask me about your career path, skills, portfolio, or next move."
    if text in ["thanks", "thank you", "спасибо", "рахмет"]:
        return "You’re welcome 🚀 I’m here whenever you need career or portfolio guidance."

    missing = ", ".join(get_missing_skills()[:3])

    system_prompt = f"""
You are MirrorMind, a real local AI digital twin career coach.

User profile:
Name: {profile["name"]}
Hard skills: {profile["hard_skills"]}
Soft skills: {profile["soft_skills"]}
Interests: {profile["interests"]}

Best role: {best_role}
Character class: {character_class}
Next skill unlock: {next_unlock}
Missing skills: {missing}

Antigravity Agent Output:
{agent_output[:2500]}

Mode: {mode}

Rules:
- Answer specifically for this user.
- Be practical, clear, and career-focused.
- If mode is Roast, be witty and direct, but not cruel.
- Keep answers structured and useful.
"""

    try:
        response = client.chat.completions.create(
            model="meta-llama-3-8b-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        return (
            "LM Studio is not connected, so I used fallback mode.\n\n"
            + smart_free_reply(prompt, mode)
        )
# CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 12% 18%, rgba(100, 116, 255, 0.10), transparent 24%),
        radial-gradient(circle at 88% 8%, rgba(99, 102, 241, 0.14), transparent 24%),
        radial-gradient(circle at 78% 88%, rgba(56, 189, 248, 0.07), transparent 28%),
        linear-gradient(135deg, #050816 0%, #070b18 52%, #0b1020 100%);
    color: #f8fafc;
}

.block-container {
    max-width: 1400px;
    padding-top: 1.9rem;
    padding-bottom: 3rem;
}

h1, h2, h3, .section-title, .hero-title, .card-title, .summary-value, .metric-value {
    font-family: 'Space Grotesk', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(5,8,22,0.98), rgba(8,13,28,0.98));
    border-right: 1px solid rgba(255,255,255,0.07);
}

.sidebar-hero {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 4px 18px 4px;
}

.orb {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background:
        radial-gradient(circle at 35% 30%, #ffffff, transparent 18%),
        radial-gradient(circle at 50% 50%, rgba(56,189,248,0.95), rgba(124,58,237,0.65));
    box-shadow:
        0 0 22px rgba(56,189,248,0.35),
        0 0 42px rgba(124,58,237,0.22);
}

.sidebar-brand {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 24px;
    font-weight: 800;
    color: white;
    letter-spacing: -0.03em;
}

.sidebar-caption {
    color: #94a3b8;
    font-size: 13px;
    margin-top: 2px;
}

.twin-status, .sidebar-box, .insight-panel {
    padding: 18px;
    border-radius: 24px;
    background: rgba(255,255,255,0.028);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 18px 42px rgba(0,0,0,0.22);
    margin-bottom: 18px;
}

.status-label, .summary-label {
    color: #a5b4fc;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.12em;
    margin-bottom: 8px;
}

.status-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 24px;
    font-weight: 800;
    color: white;
}

.status-sub, .sidebar-label {
    color: #94a3b8;
    font-size: 13px;
}

.level-bar {
    height: 8px;
    background: rgba(255,255,255,0.08);
    border-radius: 999px;
    overflow: hidden;
    margin-top: 16px;
}

.level-fill {
    width: 82%;
    height: 100%;
    background: linear-gradient(90deg, rgba(124,58,237,0.9), rgba(56,189,248,0.85));
    border-radius: 999px;
}

.level-text {
    color: #cbd5e1;
    font-size: 12px;
    margin-top: 8px;
}

.sidebar-value {
    font-size: 20px;
    font-weight: 800;
    color: white;
    margin-top: 6px;
}

.insight-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 19px;
    font-weight: 800;
    margin-bottom: 14px;
    color: white;
}

.insight-item {
    padding: 12px 0 12px 14px;
    border-left: 2px solid rgba(56,189,248,0.35);
    color: #dbeafe;
    font-size: 14px;
    line-height: 1.45;
}

.spacer { height: 34px; }
.small-spacer { height: 16px; }

.section-title {
    font-size: 24px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 8px;
    letter-spacing: -0.035em;
}

.section-title::after {
    content: "";
    display: block;
    width: 54px;
    height: 3px;
    border-radius: 999px;
    background: linear-gradient(90deg, #8b5cf6, #38bdf8);
    margin-top: 10px;
    opacity: 0.75;
}

.section-subtitle {
    color: #a7b4c8;
    font-size: 15px;
    margin-bottom: 22px;
    line-height: 1.6;
}

.hero {
    border-radius: 34px;
    padding: 46px;
    border: 1px solid rgba(255,255,255,0.105);
    background:
        linear-gradient(135deg, rgba(124,58,237,0.135), rgba(14,165,233,0.055)),
        rgba(255,255,255,0.022);
    box-shadow:
        0 22px 70px rgba(0,0,0,0.36),
        0 0 42px rgba(124,58,237,0.12),
        0 0 72px rgba(14,165,233,0.06);
    margin-bottom: 38px;
}

.hero-badge {
    display: inline-flex;
    padding: 9px 16px;
    border-radius: 999px;
    background: rgba(124,58,237,0.13);
    border: 1px solid rgba(196,181,253,0.26);
    color: #ddd6fe;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 22px;
}

.hero-title {
    font-size: 64px;
    line-height: 1;
    font-weight: 800;
    letter-spacing: -0.055em;
    max-width: 1100px;
    background: linear-gradient(90deg, #ffffff, #e0e7ff, #c7d2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    margin-top: 22px;
    font-size: 19px;
    line-height: 1.75;
    color: #cbd5e1;
    max-width: 980px;
}

.summary-card, .glow-card, .content-card, .metric, .info-box, .step-card, .role-card, .quest, .wrapped, .nav-shell {
    background: rgba(255,255,255,0.032);
    border: 1px solid rgba(255,255,255,0.085);
    box-shadow: 0 18px 42px rgba(0,0,0,0.22);
}

.summary-card {
    padding: 25px;
    border-radius: 28px;
    min-height: 137px;
}

.summary-value {
    color: #ffffff;
    font-size: 27px;
    font-weight: 800;
}

.glow-card {
    border-radius: 26px;
    padding: 24px;
    min-height: 154px;
    margin-bottom: 14px;
}

.module-card {
    transition: 0.28s ease;
    cursor: pointer;
}

.module-card:hover {
    transform: translateY(-4px);
    box-shadow:
        0 20px 46px rgba(0,0,0,0.32),
        0 0 36px rgba(99,102,241,0.18),
        0 0 54px rgba(14,165,233,0.08);
}

.card-title {
    font-size: 21px;
    font-weight: 800;
    margin-bottom: 12px;
    color: #ffffff;
}

.card-text, .info-box-text, .step-text {
    color: #b8c3d5;
    font-size: 14px;
    line-height: 1.6;
}

.content-card {
    padding: 34px;
    border-radius: 30px;
    margin-top: 24px;
}

.metric {
    padding: 23px;
    border-radius: 22px;
}

.metric-label {
    color: #94a3b8;
    font-size: 13px;
    font-weight: 700;
}

.metric-value {
    color: white;
    font-size: 30px;
    font-weight: 800;
}

.pill-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 11px;
    margin-bottom: 30px;
    margin-top: 10px;
}

.pill, .pill-blue, .pill-pink, .pill-green {
    display: inline-block;
    padding: 9px 13px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
}

.pill {
    color: #ddd6fe;
    background: rgba(124,58,237,0.13);
    border: 1px solid rgba(167,139,250,0.28);
}

.pill-blue {
    color: #cffafe;
    background: rgba(14,165,233,0.105);
    border: 1px solid rgba(56,189,248,0.28);
}

.pill-pink {
    color: #fbcfe8;
    background: rgba(219,39,119,0.105);
    border: 1px solid rgba(244,114,182,0.28);
}

.pill-green {
    color: #bbf7d0;
    background: rgba(34,197,94,0.105);
    border: 1px solid rgba(74,222,128,0.28);
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
    margin-top: 22px;
    margin-bottom: 24px;
}

.info-box, .step-card, .role-card, .quest {
    border-radius: 22px;
    padding: 22px;
}

.info-box-title, .step-title, .role-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 18px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 10px;
}

.step-number {
    color: #a5b4fc;
    font-weight: 900;
    font-size: 13px;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}

.role-score {
    color: #c4b5fd;
    font-weight: 800;
    margin: 8px 0;
}

.quest-unlocked { border-left: 4px solid #22c55e; }
.quest-progress { border-left: 4px solid #f59e0b; }
.quest-locked { border-left: 4px solid #64748b; }

.wrapped {
    padding: 38px;
    border-radius: 34px;
}

.nav-shell {
    margin-top: 36px;
    margin-bottom: 26px;
    padding: 22px 24px;
    border-radius: 26px;
}

button[kind="secondary"] {
    background: linear-gradient(135deg, rgba(99,102,241,0.42), rgba(14,165,233,0.32)) !important;
    border: 1px solid rgba(255,255,255,0.11) !important;
    border-radius: 16px !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    box-shadow: 0 10px 24px rgba(0,0,0,0.18);
}

button[kind="secondary"]:hover {
    transform: translateY(-2px);
}

div[role="radiogroup"] {
    display: flex;
    flex-wrap: wrap;
    gap: 11px;
    background: rgba(255,255,255,0.02);
    padding: 13px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.07);
}

div[role="radiogroup"] label {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 10px 16px;
    border-radius: 14px;
    color: #cbd5e1;
    font-weight: 700;
    cursor: pointer;
}

div[role="radiogroup"] input {
    display: none;
}

div[role="radiogroup"] input:checked + div {
    background: linear-gradient(135deg, rgba(99,102,241,0.38), rgba(14,165,233,0.30));
    color: white;
    font-weight: 800;
    border-radius: 12px;
}

div[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 12px 16px;
    margin-bottom: 14px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-hero">
        <div class="orb"></div>
        <div>
            <div class="sidebar-brand">MirrorMind</div>
            <div class="sidebar-caption">Creative Digital Twin</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="twin-status">
        <div class="status-label">TWIN STATUS</div>
        <div class="status-title">{profile["name"]}</div>
        <div class="status-sub">Future-facing creative profile activated</div>
        <div class="level-bar"><div class="level-fill"></div></div>
        <div class="level-text">Identity Sync: 82%</div>
    </div>
    """, unsafe_allow_html=True)

    for label, value in [
        ("Current Class", character_class),
        ("Best Match", best_role),
        ("Next Unlock", next_unlock)
    ]:
        st.markdown(f"""
        <div class="sidebar-box">
            <div class="sidebar-label">{label}</div>
            <div class="sidebar-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-panel">
        <div class="insight-title">Quick Insights</div>
        <div class="insight-item">Creative-tech fusion is your strongest zone</div>
        <div class="insight-item">AI + design is your clearest direction</div>
        <div class="insight-item">Portfolio proof matters more than more ideas</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# HERO
# =========================
st.markdown("""
<div class="hero">
    <div class="hero-badge">MirrorMind • AI Digital Twin • Creative Career Engine</div>
    <div class="hero-title">Your future is not predicted. It is designed.</div>
    <div class="hero-sub">
        MirrorMind turns your academic, creative, and digital footprint into a living career interface:
        role predictions, skill gaps, quests, portfolio ideas, and a free AI-style twin chat.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# SNAPSHOT
# =========================
st.markdown('<div class="section-title">Career Snapshot</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">The three most important insights from your digital twin.</div>', unsafe_allow_html=True)

a, b, c = st.columns(3)
with a:
    st.markdown(f'<div class="summary-card"><div class="summary-label">BEST ROLE MATCH</div><div class="summary-value">{best_role}</div></div>', unsafe_allow_html=True)
with b:
    st.markdown(f'<div class="summary-card"><div class="summary-label">CHARACTER CLASS</div><div class="summary-value">{character_class}</div></div>', unsafe_allow_html=True)
with c:
    st.markdown(f'<div class="summary-card"><div class="summary-label">NEXT SKILL UNLOCK</div><div class="summary-value">{next_unlock}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# =========================
# MODULES
# =========================
st.markdown('<div class="section-title">Choose a Module to Explore</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Click a module below to navigate through your AI digital twin system.</div>', unsafe_allow_html=True)

modules = [
    ("Character Class", "Transforms your profile into a creative-tech identity.", "Character"),
    ("Career Engine", "Predicts your strongest future roles with ML similarity.", "Future Paths"),
    ("Quest Map", "Turns skill gaps into unlockable missions.", "Quest Line"),
    ("Twin Chat", "Talk to your digital twin in Mentor, Strategist, or Roast mode.", "Twin Chat"),
]

cols = st.columns(4)
for col, (title, text, target) in zip(cols, modules):
    with col:
        st.markdown(f"""
        <div class="glow-card module-card">
            <div class="card-title">{title}</div>
            <div class="card-text">{text}</div>
        </div>
        """, unsafe_allow_html=True)
        label = "Current Page" if is_active(target) else f"Open {title}"
        if st.button(label, use_container_width=True, key=f"open_{target}"):
            set_page(target)

st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# =========================
# QUICK PROMPTS
# =========================
st.markdown('<div class="section-title">Quick Prompts</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Jump directly into the chatbot with a useful question.</div>', unsafe_allow_html=True)

quick_prompt = None
q1, q2, q3, q4 = st.columns(4)
with q1:
    if st.button("What is my best role?", use_container_width=True):
        quick_prompt = "What is my best role?"
        set_page("Twin Chat")
with q2:
    if st.button("What should I learn next?", use_container_width=True):
        quick_prompt = "What should I learn next?"
        set_page("Twin Chat")
with q3:
    if st.button("Give me portfolio ideas", use_container_width=True):
        quick_prompt = "Give me portfolio ideas"
        set_page("Twin Chat")
with q4:
    if st.button("Show agent resources", use_container_width=True):
        set_page("Agent Resources")

# =========================
# NAVIGATION
# =========================
st.markdown("""
<div class="nav-shell">
    <div class="section-title">Explore MirrorMind Sections</div>
    <div class="section-subtitle">Use this navigation to move through the project deliverables.</div>
</div>
""", unsafe_allow_html=True)

selected_page = st.radio(
    "Explore MirrorMind",
    pages,
    index=pages.index(st.session_state.page),
    horizontal=True,
    label_visibility="collapsed"
)

st.session_state.page = selected_page
page = st.session_state.page

# =========================
# PAGES
# =========================
if page == "Identity":
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("Identity Core")

    x1, x2, x3 = st.columns(3)
    with x1:
        st.markdown(f'<div class="metric"><div class="metric-label">Name</div><div class="metric-value">{profile["name"]}</div></div>', unsafe_allow_html=True)
    with x2:
        st.markdown(f'<div class="metric"><div class="metric-label">Hard Skills</div><div class="metric-value">{len(profile["hard_skills"])}</div></div>', unsafe_allow_html=True)
    with x3:
        st.markdown(f'<div class="metric"><div class="metric-label">Interests</div><div class="metric-value">{len(profile["interests"])}</div></div>', unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        st.write("### Skill Profile")
        st.write("Hard Skills")
        render_pills(profile["hard_skills"], "pill")
        st.write("Soft Skills")
        render_pills(profile["soft_skills"], "pill-blue")
    with right:
        st.write("### Creative Direction")
        st.write("Interests")
        render_pills(profile["interests"], "pill-pink")
        st.markdown("""
        <div class="info-box">
            <div class="info-box-title">Identity Summary</div>
            <div class="info-box-text">
                Your profile shows a creative-technological direction: design, visual communication,
                artificial intelligence, and immersive media.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Character":
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("Character Class")

    st.markdown("### Generated Digital Identity")

    top_left, top_right = st.columns([2, 1])
    with top_left:
        st.markdown(f"## {character_class}")
        st.caption("Legendary creative-tech class generated from your profile")
        st.write(class_desc)
    with top_right:
        st.metric("Current Level", "Level 3")
        st.metric("Evolution", "78%")

    st.progress(78, text="Evolution Progress to Creative Technologist")

    st.markdown('<div class="small-spacer"></div>', unsafe_allow_html=True)

    st.markdown("### Character Lore")
    st.info(
        "You are a hybrid creator blending visual thinking, immersive media, and future-facing technology. "
        "MirrorMind reads your creative and technical signals as a hybrid identity: visual design, immersive thinking, "
        "AI curiosity, and future-facing experimentation. This class is built for people who connect tools, stories, interfaces, and systems."
    )

    st.markdown("### Core Abilities")
    a1, a2, a3, a4 = st.columns(4)
    with a1:
        with st.container(border=True):
            st.markdown("**Visual Systems**")
            st.write("Turns abstract ideas into clear interfaces, moods, and visual directions.")
    with a2:
        with st.container(border=True):
            st.markdown("**AI Imagination**")
            st.write("Uses generative tools to prototype faster and expand creative possibilities.")
    with a3:
        with st.container(border=True):
            st.markdown("**Immersive Thinking**")
            st.write("Connects 3D, VR, interaction, and storytelling into future experiences.")
    with a4:
        with st.container(border=True):
            st.markdown("**Portfolio Alchemy**")
            st.write("Transforms learning into visible proof through case studies and projects.")

    st.markdown("### Evolution Roadmap")
    r1, r2, r3 = st.columns(3)
    with r1:
        with st.container(border=True):
            st.markdown("**Now**")
            st.write("Immersive AI Explorer")
    with r2:
        with st.container(border=True):
            st.markdown("**Next Unlock**")
            st.write(next_unlock)
    with r3:
        with st.container(border=True):
            st.markdown("**Future Form**")
            st.write("Creative Technologist")

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Future Paths":
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("Future Paths")

    dream_role = st.selectbox("Choose a dream role to inspect", [x["job"] for x in top3])
    selected_role = next((item for item in top3 if item["job"] == dream_role), top3[0])
    missing_text = ", ".join(selected_role["missing_skills"]) if selected_role["missing_skills"] else "No major gaps"

    st.markdown(f"""
    <div class="role-card">
        <div class="role-title">{selected_role["job"]}</div>
        <div class="role-score">Match Score: {selected_role["score"]}%</div>
        <div><b>Missing Skills:</b> {missing_text}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-grid">
        <div class="info-box"><div class="info-box-title">Why this role fits</div><div class="info-box-text">This role fits your creative-technical profile because it combines visual thinking, digital design, experimentation, and emerging technology.</div></div>
        <div class="info-box"><div class="info-box-title">What makes you different</div><div class="info-box-text">Your strongest advantage is your ability to connect design, storytelling, AI, and immersive media.</div></div>
        <div class="info-box"><div class="info-box-title">Main risk</div><div class="info-box-text">The main gap is execution proof. You need finished portfolio projects that show your thinking.</div></div>
        <div class="info-box"><div class="info-box-title">Best next move</div><div class="info-box-text">Pick one role, learn one missing skill, and turn it into one polished case study.</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.write("### Portfolio Project Ideas")
    for i, idea in enumerate(portfolio_ideas, start=1):
        st.markdown(f"""
        <div class="step-card">
            <div class="step-number">PROJECT {i}</div>
            <div class="step-title">{idea}</div>
            <div class="step-text">Build this as a small polished case study with visuals, process, tools used, and final outcome.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Skill Aura":
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("Skill Aura")

    categories = ["Design", "AI", "3D/VR", "Communication", "Creativity", "Teamwork"]
    values = [9, 8, 8, 8, 10, 7]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values, theta=categories, fill="toself", name="Skill Aura"))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 10], gridcolor="rgba(255,255,255,0.18)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.13)")
        ),
        font=dict(color="white"),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write("### Power Meters")
    st.progress(90, text="Design")
    st.progress(80, text="AI")
    st.progress(78, text="3D / VR")
    st.progress(85, text="Communication")

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Quest Line":
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("Quest Line")

    for quest in quests:
        css = "quest-unlocked" if quest["status"] == "Unlocked" else "quest-progress" if quest["status"] == "In Progress" else "quest-locked"
        st.markdown(f"""
        <div class="quest {css}">
            <b>{quest["title"]}</b><br>
            <span style="color:#94a3b8;">Status: {quest["status"]}</span>
        </div>
        """, unsafe_allow_html=True)

    st.write("### Evolution Timeline")
    for stage, title, text in [
        ("STAGE 1", "Creative AI Explorer", "Explore tools, understand your strengths, and define your creative-tech direction."),
        ("STAGE 2", "AI Designer / Game Developer", "Build specific projects that connect design, interactivity, and AI."),
        ("STAGE 3", "Creative Technologist", "Turn your creative and technical skills into a professional identity.")
    ]:
        st.markdown(f"""
        <div class="step-card">
            <div class="step-number">{stage}</div>
            <div class="step-title">{title}</div>
            <div class="step-text">{text}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Twin Chat":
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("Twin Chat")

    mode = st.radio("Choose mode", ["Mentor", "Strategist", "Roast"], horizontal=True)

    st.write("### Suggested Questions")

    suggestions = [
        "What is my best role?",
        "What should I learn next?",
        "Give me portfolio ideas",
        "Roast my current path"
    ]

    cols = st.columns(4)
    for col, suggestion in zip(cols, suggestions):
        with col:
            if st.button(suggestion, use_container_width=True, key=f"suggest_{suggestion}"):
                st.session_state.messages.append({"role": "user", "content": suggestion})
                with st.spinner("MirrorMind is thinking..."):
                    reply = lmstudio_reply(suggestion, mode)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

    if quick_prompt:
        st.session_state.messages.append({"role": "user", "content": quick_prompt})
        with st.spinner("MirrorMind is thinking..."):
            reply = lmstudio_reply(quick_prompt, mode)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask MirrorMind about your future path...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("MirrorMind is thinking..."):
            reply = lmstudio_reply(prompt, mode)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Agent Resources":
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("Antigravity Agent Resources")
    st.caption("This page turns the Antigravity-generated report into a clean action dashboard.")

    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("### Best Career Match")
            st.markdown("**Creative Technologist**")
            st.write("The agent identified this as your strongest direction because your profile combines graphic design, UI/UX, 3D modeling, VR, and generative AI.")
    with c2:
        with st.container(border=True):
            st.markdown("### Missing Skills")
            st.write("- Coding / Programming")
            st.write("- Interaction Design")
            st.write("- Interactive Media")
            st.write("- Physical Computing")

    c3, c4 = st.columns(2)
    with c3:
        with st.container(border=True):
            st.markdown("### Learning Resources")
            st.write("- Interactive & Immersive HQ")
            st.write("- MIT Media Lab Learning Creative Learning")
            st.write("- freeCodeCamp / Codecademy")
            st.write("- Three.js Journey")
    with c4:
        with st.container(border=True):
            st.markdown("### Portfolio Ideas")
            st.write("- AI-powered interactive web experience")
            st.write("- Immersive VR data visualization")
            st.write("- Generative art dashboard")

    st.markdown("### Agent Action Plan")

    steps = [
        ("STEP 1", "Learn the missing technical layer", "Start with JavaScript, creative coding, or WebGL / Three.js because these skills connect your design and 3D background with interactive digital products."),
        ("STEP 2", "Build one interactive portfolio project", "Create a small but polished project such as an AI moodboard, VR gallery, or generative art dashboard."),
        ("STEP 3", "Document the process", "Turn the project into a case study showing the idea, tools, design decisions, screenshots, and final result."),
    ]

    for step, title, body in steps:
        with st.container(border=True):
            st.caption(step)
            st.markdown(f"#### {title}")
            st.write(body)

    st.markdown("### Full Antigravity Agent Output")
    with st.expander("Open full generated report"):
        st.markdown(agent_output)

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Wrapped":
    st.markdown('<div class="wrapped">', unsafe_allow_html=True)
    st.subheader("Semester Wrapped")
    st.caption("A shareable summary card for your semester and digital twin growth.")

    w1, w2, w3 = st.columns(3)
    with w1:
        st.metric("Top Skill", "Creativity")
        st.metric("Best Role Match", best_role)
    with w2:
        st.metric("Character Class", character_class)
        st.metric("Next Unlock", next_unlock)
    with w3:
        st.metric("Career Readiness", "78%")
        st.metric("Portfolio Focus", "AI + Design")

    st.markdown("### Shareable LinkedIn Summary")
    wrapped_text = f"""MirrorMind Semester Wrapped\n\nTop Skill: Creativity\nBest Career Match: {best_role}\nCharacter Class: {character_class}\nNext Skill Unlock: {next_unlock}\nFuture Direction: AI + Design + Immersive Media\n\nReflection: This semester showed that my strongest direction is creative technology, especially combining design, AI, and interactive media into portfolio-ready projects."""

    st.text_area("Copy this summary", wrapped_text, height=220)
    st.download_button(
        label="Download Semester Wrapped TXT",
        data=wrapped_text,
        file_name="semester_wrapped.txt",
        mime="text/plain"
    )

    st.markdown("### Reflection")
    st.info("MirrorMind shows that my strongest path is creative technology. The next step is turning ideas into finished, documented portfolio projects.")

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "About Project":
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("About MirrorMind")

    st.markdown("### Objective")
    st.write("MirrorMind is an AI-powered Digital Twin Career Engine. It analyzes a structured user profile, predicts career paths with machine learning, identifies missing skills, and generates a career development roadmap.")

    st.markdown("### 5-Layer Architecture")

    layers = [
        ("1. Platform Layer", "NotebookLM is used conceptually as the knowledge synthesis layer. In the full architecture, NotebookLM MCP connects NotebookLM data directly to Antigravity."),
        ("2. Model Layer", "A classical ML layer uses CountVectorizer and Cosine Similarity to compare the user skill vector with job role requirements and produce top career matches plus missing skills."),
        ("3. Agent Layer", "Antigravity generates agent_output.md from the ML prediction, recommending learning resources, GitHub directions, and portfolio projects."),
        ("4. Application Layer", "Streamlit provides the dashboard: Identity, Character Class, Future Paths, Skill Aura radar chart, Quest Line, Twin Chat, Agent Resources, and Semester Wrapped."),
        ("5. Infrastructure Layer", "Streamlit and ML run locally. LM Studio runs a local LLM server on localhost:1234. Antigravity and NotebookLM represent agent/platform tooling."),
    ]

    for title, body in layers:
        with st.container(border=True):
            st.markdown(f"#### {title}")
            st.write(body)

    st.markdown("### Technologies")
    st.write("Python, Streamlit, Pandas, Scikit-learn, Plotly, JSON, CSV, Antigravity, LM Studio.")

    st.markdown("### Privacy Note")
    st.warning("Raw CV, transcript, LinkedIn data, and chat history should not be pushed to a public GitHub repository. Only structured example data should be shared.")

    st.markdown('</div>', unsafe_allow_html=True)
