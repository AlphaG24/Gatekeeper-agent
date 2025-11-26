import os
import asyncio
from fastapi import FastAPI, BackgroundTasks
from src.agents.navigator import NavigatorAgent

app = FastAPI()

# Cloud Run requires listening on the PORT environment variable
PORT = int(os.getenv("PORT", 8080))

async def run_agent_task(goal: str):
    """Runs the agent in the background"""
    print(f"🚀 Triggering Cloud Agent for: {goal}")
    try:
        agent = NavigatorAgent()
        await agent.start_session()
        await agent.run_task(goal)
    except Exception as e:
        print(f"❌ Agent Error: {e}")

@app.get("/")
def home():
    return {"status": "GateKeeper Agent is Online", "usage": "Send POST to /run"}

@app.post("/run")
async def trigger_agent(background_tasks: BackgroundTasks):
    # We run the agent in the background so the HTTP request doesn't time out
    goal = "Go to saucedemo.com, log in using username 'standard_user' and password 'secret_sauce', then verify I am on the inventory page."
    background_tasks.add_task(run_agent_task, goal)
    return {"status": "Agent started", "goal": goal}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
