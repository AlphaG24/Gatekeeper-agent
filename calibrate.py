import asyncio
from playwright.async_api import async_playwright

async def get_coordinates():
    async with async_playwright() as p:
        # Launch headless to match the Agent's environment EXACTLY
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_viewport_size({"width": 1280, "height": 720})
        
        print("📏 Navigating to SauceDemo...")
        await page.goto("https://www.saucedemo.com/")
        
        # Get Bounding Boxes for the elements
        user_box = await page.locator("#user-name").bounding_box()
        pass_box = await page.locator("#password").bounding_box()
        btn_box = await page.locator("#login-button").bounding_box()
        
        # Calculate Centers
        u_x = user_box['x'] + user_box['width'] / 2
        u_y = user_box['y'] + user_box['height'] / 2
        
        p_x = pass_box['x'] + pass_box['width'] / 2
        p_y = pass_box['y'] + pass_box['height'] / 2
        
        b_x = btn_box['x'] + btn_box['width'] / 2
        b_y = btn_box['y'] + btn_box['height'] / 2
        
        print("\n🎯 --- GOLDEN COORDINATES (1280x720) ---")
        print(f"Username Center: x={int(u_x)}, y={int(u_y)}")
        print(f"Password Center: x={int(p_x)}, y={int(p_y)}")
        print(f"Login Btn Center: x={int(b_x)}, y={int(b_y)}")
        print("---------------------------------------")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(get_coordinates())