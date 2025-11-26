GateKeeper: Vision-Enabled Authentication Agent 🔐
A Capstone Project for the Google AI Agents Intensive

GateKeeper is an autonomous, vision-driven authentication agent built to tackle one of the hardest problems in browser automation: reliable login workflows.
Instead of depending on fragile HTML selectors, GateKeeper uses Gemini 2.0 Flash to see, reason, and act on real UI elements — making it resilient to DOM changes, dynamic layouts, and anti-bot patterns.

🎥 Project Demo

(Insert YouTube Demo Link Here)

🏗️ System Architecture

GateKeeper uses a feedback-driven, closed-loop “See → Reason → Act → Verify” pipeline:

1. Vision Layer — “The Eye”

Playwright captures a full-page (1280×720) screenshot that represents the current browser state.

2. Navigator Agent — “The Brain”

Gemini 2.0 Flash performs multimodal reasoning to:

Locate username/password fields

Identify actionable UI components (login buttons, toggles, banners)

Detect error messages like “Invalid Password”

Suggest next steps to correct failures

3. Browser Tool — “The Hand”

A custom atomic-action toolkit executes precise actions:

click_and_type()

click()

DOM injection of visual markers (red/blue dots) for debugging
Each action is grounded to the model’s predicted coordinates.

4. Verifier Layer

After every action, the agent checks:

URL changes

Page transitions

Error banners
If login fails or stalls, it triggers a self-healing refresh loop.

🛠️ Tech Stack

Model: Google Gemini 2.0 Flash (google-generativeai)

Automation: Playwright (Chromium)

Language: Python 3.11+

Environment: Virtualenv / venv

Runtime: Local development machine

🚀 Getting Started
1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/gatekeeper-agent.git
cd gatekeeper-agent

2. Install Dependencies
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

3. Configure API Key

Create a .env file:

GOOGLE_API_KEY=your_gemini_api_key_here

4. Run the Agent
python test_login.py

🧠 Key Features
🔁 Self-Healing Execution

Automatically retries or refreshes when interactions fail or login loops stall.

👁️ Vision-First Navigation

No CSS selectors.
No XPaths.
No brittle DOM dependencies.
UI interaction is driven solely by visual understanding.

🎯 Precise Interaction Markers

Colored markers (red/blue dots) are injected into the DOM so you can see exactly where the model thinks the UI elements are.

🧩 Modular Design

Each component is atomic and fully replaceable — vision, navigation, verification, and execution.

📌 Use Case

GateKeeper solves real-world issues in automation:

Websites with dynamic HTML

Anti-bot protection using unpredictable DOMs

Authentication flows that constantly redesign their UI

Login screens behind iframes or shadow DOM

🏁 Project Status

This agent is a submission-ready implementation for the Google × Kaggle AI Agents Intensive 2025, showcasing autonomous reasoning, multimodal action planning, and robust operation across login workflows.

✍️ Author

Raghav
Google × Kaggle AI Agents Intensive — Capstone Project (2025)