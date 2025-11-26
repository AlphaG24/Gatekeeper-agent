import asyncio
import os
from dotenv import load_dotenv
from src.agents.navigator import NavigatorAgent

# Load Environment
load_dotenv()

async def main():
    print("🚀 Starting GateKeeper Agent Test...")
    
    # Initialize the Agent
    agent = NavigatorAgent()
    
    # Boot up the browser
    await agent.start_session()
    
    # Run the mission
    # We are vague on purpose to test the Vision capabilities
    await agent.run_task(
        goal="Go to saucedemo.com, log in using username 'standard_user' and password 'secret_sauce', then verify I am on the inventory page."
    )

if __name__ == "__main__":
    asyncio.run(main())