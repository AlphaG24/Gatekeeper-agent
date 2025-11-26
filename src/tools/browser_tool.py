# GateKeeper Module: browser_tool.py
import asyncio
from playwright.async_api import async_playwright, Page, Browser
from typing import Dict, Any, Optional

class BrowserTool:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def start(self):
        """Initializes the browser session with VIDEO RECORDING."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=['--no-sandbox', '--disable-setuid-sandbox'] # Helps stability in WSL
        )
        
        # Create a context with video recording enabled
        # Videos will be saved to the 'videos/' folder
        self.context = await self.browser.new_context(
            record_video_dir="videos/",
            record_video_size={"width": 1280, "height": 720},
            viewport={"width": 1280, "height": 720}
        )
        
        self.page = await self.context.new_page()
        print("🌐 Browser Tool Started (Rec 🔴)")

    async def navigate(self, url: str):
        """Goes to a specific URL."""
        print(f"👉 Navigating to: {url}")
        try:
            await self.page.goto(url, timeout=30000)
            await self.page.wait_for_load_state("networkidle")
            return f"Successfully navigated to {url}"
        except Exception as e:
            return f"Error navigating: {str(e)}"

    async def click(self, x: int, y: int):
        """Clicks at coordinates AND draws a red dot to show where."""
        try:
            # 1. VISUAL DEBUG: Draw a red dot at the click location
            await self.page.evaluate(f"""
                const dot = document.createElement('div');
                dot.style.position = 'absolute';
                dot.style.left = '{x}px';
                dot.style.top = '{y}px';
                dot.style.width = '10px';
                dot.style.height = '10px';
                dot.style.backgroundColor = 'red';
                dot.style.borderRadius = '50%';
                dot.style.zIndex = '10000';
                dot.style.pointerEvents = 'none'; // Click through it
                document.body.appendChild(dot);
            """)
            
            # 2. Perform the actual click
            await self.page.mouse.click(x, y)
            
            # 3. Wait longer for reaction
            await asyncio.sleep(2) 
            return f"Clicked at ({x}, {y}) (Visual Marker Added)"
        except Exception as e:
            return f"Failed to click: {str(e)}"

    async def type_text(self, text: str):
        """Types text into the currently focused element."""
        try:
            await self.page.keyboard.type(text)
            return f"Typed: '{text}'"
        except Exception as e:
            return f"Failed to type: {str(e)}"

    async def capture_screen(self) -> str:
        """Takes a screenshot and saves it for the AI to read."""
        path = "screenshots/current_state.png"
        await self.page.screenshot(path=path)
        return path

    async def close(self):
        if self.context:
            await self.context.close() # Closes context and saves video
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("🔒 Browser Tool Closed")

    async def refresh(self):
        """Reloads the current page."""
        try:
            await self.page.reload()
            await self.page.wait_for_load_state("networkidle")
            return "Page refreshed successfully"
        except Exception as e:
            return f"Failed to refresh: {str(e)}"    

    async def click_and_type(self, x: int, y: int, text: str):
        """Clicks a location to focus it, then types text."""
        try:
            # 1. Visual Marker (Red Dot)
            await self.page.evaluate(f"""
                const dot = document.createElement('div');
                dot.style.position = 'absolute';
                dot.style.left = '{x}px';
                dot.style.top = '{y}px';
                dot.style.width = '10px';
                dot.style.height = '10px';
                dot.style.backgroundColor = 'blue';  // Blue for typing!
                dot.style.borderRadius = '50%';
                dot.style.zIndex = '10000';
                dot.style.pointerEvents = 'none';
                document.body.appendChild(dot);
            """)
            
            # 2. Click to focus
            await self.page.mouse.click(x, y)
            await asyncio.sleep(0.5) # Wait for focus
            
            # 3. Type the text
            await self.page.keyboard.type(text)
            
            return f"Clicked ({x},{y}) and Typed '{text}'"
        except Exception as e:
            return f"Failed to type: {str(e)}"        