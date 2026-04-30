# Platform + Agent Proof Layer: Digital Twin Career Engine

## 1. Platform Layer: NotebookLM + MCP Explanation
**NotebookLM** acts as the foundational grounding system. By ingesting your specific project files, resumes, and design portfolios, NotebookLM transforms them into an intelligent, personalized context window. It makes the model an expert on *you*.

**MCP (Model Context Protocol)** serves as the crucial bridge. It allows the AI models to securely connect to external data sources, local development environments, and live web tools. In this workflow, MCP enables the agent to read your local files (like `agent_output.md`), execute live web searches to find current resources, and seamlessly synthesize everything back into your local workspace. Together, NotebookLM and MCP create a personalized, real-time operating system for your career progression.

## 2. Model Layer Input Used
The agent leveraged the Machine Learning outputs previously generated in your `agent_output.md` file:
*   **Best Career Match:** Creative Technologist (leveraging your strong background in Graphic Design, UI/UX, 3D Modeling, VR, and Generative AI).
*   **Missing Skills Identified:** 
    *   **Coding / Programming:** (JavaScript, WebGL, Python, C# for Unity)
    *   **Interaction Design / Interactive Media:** (Connecting hardware/software to user inputs)
    *   **Physical Computing / Electronics:** (Arduino, Sensors)

## 3. Agent Layer Live Web Browsing Results
Using the missing skills as a heuristic, live web searches were executed to find the most current and relevant upskilling resources. The search prioritized modern 3D web frameworks (Three.js/WebGL) and interactive media tools (TouchDesigner/p5.js) to perfectly complement your existing 3D and VR background. General creative tech hackathons were also queried to find application opportunities.

## 4. Links / Resources Found
Based on the live web browsing session, here are the curated, up-to-date resources:
*   **GitHub Repository:** [Awesome Creative Coding](https://github.com/terkelg/awesome-creative-coding) – A carefully curated, actively maintained list of creative coding resources, frameworks, and open-source libraries to understand the landscape.
*   **Learning Course:** [Three.js Journey by Bruno Simon](https://threejs-journey.com/) – The gold standard, comprehensive course for translating 3D modeling skills into interactive web experiences using WebGL.
*   **Creative Technology Tool:** [TouchDesigner](https://derivative.ca/) & [p5.js](https://p5js.org/) – Industry-standard tools for creating interactive media, generative art, and connecting sensors to dynamic visuals.
*   **Hackathon / Opportunity:** [MIT Reality Hack](https://www.mitrealityhack.com/) / XR Hackathons on [Devpost](https://devpost.com/hackathons?utf8=%E2%9C%93&search=creative+technology&challenge_type[]=online) – Premier events (both physical and online) for creative technologists to build immersive tech projects and network with peers.

## 5. Final Action Plan
1.  **Immediate Step:** Begin the *Three.js Journey* course. This will directly bridge your existing 3D modeling and UI/UX skills with web programming, tackling your biggest identified skill gap.
2.  **Exploration:** Fork repositories from the *Awesome Creative Coding* GitHub list to dissect how interactive web scenes are constructed and experiment with modifying them.
3.  **Tool Mastery:** Download *TouchDesigner* and complete their beginner tutorials to understand node-based interactive media creation and real-time rendering.
4.  **Application:** Register for an upcoming XR or Creative Tech hackathon on Devpost to force a deadline on an interactive portfolio piece, combining your generative AI knowledge with live user interaction.



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

####  Quest System
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

# How It Works

1. User data is structured (profile + dataset)
2. ML model predicts best-fit roles
3. Missing skills are extracted
4. Antigravity agent generates insights
5. UI visualizes everything interactively
6. Local LLM enables real-time AI chat

---

# Project Structure
