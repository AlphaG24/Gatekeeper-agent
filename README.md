GateKeeper: Vision-Enabled Authentication Agent 🔐
Capstone Project – Google AI Agents Intensive 2025

GateKeeper is an autonomous, multimodal AI agent built to solve one of the most fundamental and fragile steps in browser automation: Authentication.
Powered by Gemini 2.0 Flash, it visually interprets login pages, identifies UI components from pixels—not selectors—and executes precise, self-correcting interactions to reliably perform login flows.

🎥 Project Demo

[![GateKeeper Demo](https://img.youtube.com/vi/l1SjV7rIf40/0.jpg)](https://youtu.be/l1SjV7rIf40)

(Click the thumbnail above to watch the demo video.)

🏗️ System Architecture

GateKeeper follows a closed-loop “See → Reason → Act → Verify” pipeline for robust navigation:

1. Vision Layer — “The Eye”

Playwright captures a 1280×720 screenshot of the current browser state.

2. Navigator Agent — “The Brain”

Gemini 2.0 Flash analyzes the screenshot to:

Detect username/password fields

Identify login buttons

Spot error messages (e.g., “Invalid Password”)

Generate the next interaction plan

3. Browser Tool — “The Hand”

Executes atomic actions like click_and_type()

Injects red/blue visual markers into the DOM to confirm precision

Ensures pixel-aligned, repeatable interactions

4. Verifier Layer

Validates URL transitions and page content changes

Detects stuck or failed states

Triggers a self-healing refresh loop when necessary

🛠️ Tech Stack

Model: Google Gemini 2.0 Flash

Automation: Playwright (Headless Chromium)

Language: Python 3.11+

Deployment: Docker + Google Cloud Run

Environment: Virtualenv (venv)

🚀 Getting Started
1. Clone the Repository
git clone https://github.com/AlphaG24/Gatekeeper-agent.git
cd Gatekeeper-agent

2. Install Dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

3. Configure API Key

Create a .env file in the project root:

GOOGLE_API_KEY=your_gemini_api_key_here

4. Run the Agent
python test_login.py

🧠 Key Features
🔁 Self-Healing Execution

Automatically detects failed login attempts and triggers retry or refresh logic.

👁️ Vision-First Navigation

Fully pixel-based — no CSS selectors, XPaths, or brittle DOM checks.

🎯 Visual Debug Markers

Injects colored markers into the webpage to show exactly where the AI is interacting.

☁️ Cloud-Ready Architecture

Includes:

Dockerfile

Cloud-run friendly wrappers

Zero-config deployment instructions

🧩 Why This Matters

Authentication is the biggest blocker for autonomous agents and RPA systems. GateKeeper demonstrates a robust, vision-driven method for handling login workflows that change frequently or deliberately break selector-based automation.

✍️ Submitted By

Raghav
Google × Kaggle — AI Agents Intensive 2025