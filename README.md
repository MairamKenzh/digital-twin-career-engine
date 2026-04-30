# 🧠 Digital Twin Career Engine

An AI-powered "Digital Twin" that analyzes a user's skills, interests, and digital footprint to predict optimal career paths, identify skill gaps, and guide professional growth.

---

# Project Objective

This project builds a highly advanced **Digital Twin system** that:

- Predicts your future career trajectory
- Maps your current skill set
- Identifies missing skills
- Generates actionable learning paths
- Acts as an AI-powered career assistant

---

#  5-Layer Gen AI Architecture

## 1️ Platform Layer (NotebookLM + MCP)

The system uses **NotebookLM** as a structured knowledge base for personal data such as:

- Skills
- Interests
- Academic background

Antigravity acts as the execution layer and connects conceptually through MCP (Model Context Protocol) to query structured data.

---

## 2️ Model Layer (Machine Learning)

A custom ML pipeline processes the user profile:

- Dataset: `jobs_dataset.csv`
- Script: `predict_roles.py`

### Method:
- Cosine Similarity / Matching
- Skill vector comparison

### Output:
- Top career match
- Missing skills
- Role alignment score

---

## 3️ Agent Layer (Antigravity)

Antigravity acts as the **execution agent**:

- Takes ML output (best role + missing skills)
- Generates structured insights
- Produces:
agent_output.md
platform_agent_proof.md


### Capabilities:
- Resource generation
- Career planning
- Learning recommendations

---

## 4️ Application Layer (Streamlit UI)

Interactive dashboard built with **Streamlit**.

### Features:

####  Character Class
Transforms user into a **digital identity archetype** (e.g. Creative Technologist)

####  Career Engine
Displays:
- Best career match
- Missing skills
- Role explanation

#### 🗺️ Quest System
Gamified progression system:
- Skill unlocks
- Learning roadmap

####  Twin Chat
AI assistant with modes:
- Mentor
- Strategist
- Roast Mode 

Powered by **LM Studio (local LLM)**

####  Skill Aura
Visual representation of:
- Hard skills
- Soft skills

####  Balance Wheel
Radar chart comparing skills

####  Semester Wrapped
Summary card:
- Top skill
- Best role
- Key insights

---

## 5️ Infrastructure Layer

### Local:
- Python
- Streamlit
- LM Studio (LLaMA 3 8B)

### External:
- Antigravity (Agent Layer)
- NotebookLM (Data Layer)

---

#  How It Works

1. User data is structured (profile + dataset)
2. ML model predicts best-fit roles
3. Missing skills are extracted
4. Antigravity agent generates insights
5. UI visualizes everything interactively
6. Local LLM enables real-time AI chat

---

#  Project Structure
app.py # Main Streamlit app
predict_roles.py # ML model
jobs_dataset.csv # Career dataset
user_profile.json # User data
agent_output.md # Agent insights
agent_resources.py # Resource generation
generate_resources.py # Data processing


---

#  How to Run

```bash
pip install -r requirements.txt
py -m streamlit run app.py

Make sure:

LM Studio is running
Model is loaded
Local server is active

#### Key Innovation

This project combines:

Machine Learning
Local LLM (no API cost)
Agent-based automation
Gamified UI/UX

To create a personal AI career assistant

# Conclusion

The Digital Twin Career Engine demonstrates a full-stack GenAI system:

Data → Model → Agent → UI → Infrastructure

It transforms raw user data into actionable, intelligent career insights in an interactive and engaging way.