import os
import time
import asyncio
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

# Import our tools
from src.tools.browser_tool import BrowserTool

class NavigatorAgent:
    def __init__(self, model_name: str = "models/gemini-2.0-flash"):
        self.browser = BrowserTool(headless=True)
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment")
        genai.configure(api_key=api_key)
        
        # --- MAPPING: Added click_and_type ---
        self.tools_map = {
            'click': self.browser.click,
            'click_and_type': self.browser.click_and_type, # <--- NEW SUPER TOOL
            'navigate': self.browser.navigate,
            'refresh': self.browser.refresh,
            'mark_done': self.mark_done
        }
        
        self.model = genai.GenerativeModel(
            model_name=model_name,
            tools=list(self.tools_map.values()),
            system_instruction="""
            You are a Vision-Enabled Browser Agent. 
            
            YOUR MISSION: Log in to SauceDemo.
            
            COORDINATES (1280x720) - CALIBRATED:
            - Username Box: EXACTLY (x=640, y=173)  <-- UPDATE THESE
            - Password Box: EXACTLY (x=640, y=227)  <-- UPDATE THESE
            - Login Button: EXACTLY (x=640, y=326)  <-- UPDATE THESE
            
            STRATEGY:
            1. ACTION: click_and_type(x=640, y=173, text="standard_user")
            2. ACTION: click_and_type(x=640, y=227, text="secret_sauce")
            3. ACTION: click(x=640, y=326)
            4. VERIFY: Do you see "Products"? If yes, mark_done.
            
            If you see the Login Page again, it failed. Use 'refresh' and try slightly different coordinates.
            """
        )
        self.chat = self.model.start_chat()

    def mark_done(self, summary: str):
        print(f"🏁 Mission Conclusion: {summary}")
        return "TASK_COMPLETED"

    async def start_session(self):
        await self.browser.start()

    async def _send_safe_message(self, items):
        """Sends a message with retries for Rate Limits and Malformed Calls."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.chat.send_message(items)
                return response
            except Exception as e:
                err_str = str(e)
                print(f"⚠️ Gemini Error (Attempt {attempt+1}): {err_str}")
                if "429" in err_str:
                    time.sleep(10)
                    continue
                if "MALFORMED_FUNCTION_CALL" in err_str:
                    items.append("Previous call was malformed. Use strict JSON.")
                    time.sleep(2)
                    continue
                raise e
        return None

    async def run_task(self, goal: str):
        print(f"🎯 Navigator Task: {goal}")
        
        if "saucedemo" in goal:
            await self.browser.navigate("https://www.saucedemo.com/")
        
        step = 0
        max_steps = 15
        
        while step < max_steps:
            step += 1
            print(f"\n--- Step {step} ---")
            
            screenshot_path = await self.browser.capture_screen()
            print(f"👀 Analyzing screenshot: {screenshot_path}")
            
            sample_file = genai.upload_file(path=screenshot_path, display_name=f"step_{step}")
            
            response = await self._send_safe_message(
                [sample_file, f"Current Goal: {goal}. Review screen. What is the next step?"]
            )

            if not response or not response.candidates:
                print("❌ Failed to get valid response.")
                break

            try:
                for part in response.candidates[0].content.parts:
                    if part.function_call:
                        fc = part.function_call
                        fn_name = fc.name
                        args = dict(fc.args)
                        
                        print(f"🤖 Gemini Command: {fn_name}({args})")
                        
                        if fn_name == 'mark_done':
                            print("✅ Task Success!")
                            await self.browser.close()
                            return

                        if fn_name in self.tools_map:
                            tool_result = await self.tools_map[fn_name](**args)
                            print(f"🔧 Tool Output: {tool_result}")
                            
                            function_response = {
                                "name": fn_name,
                                "response": {"result": tool_result}
                            }
                            self.chat.send_message(
                                content.Content(
                                    parts=[content.Part(function_response=content.FunctionResponse(**function_response))]
                                )
                            )
                        else:
                            print(f"❌ Unknown function: {fn_name}")

                    elif part.text:
                        print(f"🤖 Agent Thought: {part.text}")
            except Exception as e:
                 print(f"❌ Error parsing response: {e}")

            time.sleep(5) 

        await self.browser.close()