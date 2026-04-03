"""
Browser Controller for OpenBridge
Controls a real browser to interact with streaming platforms.
"""

import asyncio
import logging
from pathlib import Path
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

logger = logging.getLogger("openbridge.browser")


class BrowserController:
    def __init__(self, profile_name: str, headless: bool = False):
        self.profile_name = profile_name
        self.headless = headless
        self._playwright = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None
        self._running = False

    async def start(self):
        """Start the browser and navigate to Twitch."""
        logger.info("Starting browser...")
        
        self._playwright = await async_playwright().start()
        
        # User data directory for session persistence
        user_data_dir = Path("sessions") / self.profile_name
        user_data_dir.mkdir(parents=True, exist_ok=True)
        
        self._browser = await self._playwright.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=self.headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )
        
        self._page = self._browser.pages[0] if self._browser.pages else await self._browser.new_page()
        
        # Anti-detection
        await self._page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)
        
        self._running = True
        logger.info("Browser started.")

    async def stop(self):
        """Stop the browser."""
        logger.info("Stopping browser...")
        self._running = False
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
        logger.info("Browser stopped.")

    @property
    def page(self) -> Page:
        if not self._page:
            raise RuntimeError("Browser not started. Call start() first.")
        return self._page

    @property
    def is_running(self) -> bool:
        return self._running

    async def navigate_to_channel(self, channel: str, platform: str = "twitch"):
        """Navigate to a channel page."""
        urls = {
            "twitch": f"https://www.twitch.tv/{channel}",
            "kick": f"https://kick.com/{channel}",
            "youtube": f"https://www.youtube.com/@{channel}/live",
        }
        url = urls.get(platform, urls["twitch"])
        logger.info(f"Navigating to {url}")
        await self._page.goto(url, wait_until="domcontentloaded")

    async def send_chat_message(self, message: str):
        """Send a message in chat."""
        # Twitch chat input selector
        chat_input = self._page.locator('textarea[data-a-target="chat-input"]')
        if await chat_input.count() > 0:
            await chat_input.fill(message)
            await self._page.keyboard.press("Enter")
            logger.info(f"Sent chat message: {message}")
        else:
            logger.warning("Chat input not found.")

    async def click_clip_button(self):
        """Click the clip button to create a clip."""
        # Twitch clip button selector
        clip_button = self._page.locator('[data-a-target="clip-button"]')
        if await clip_button.count() > 0:
            await clip_button.click()
            logger.info("Clip button clicked.")
        else:
            logger.warning("Clip button not found.")

    async def get_chat_messages(self, limit: int = 50) -> list[dict]:
        """Get recent chat messages from the DOM."""
        messages = []
        chat_lines = self._page.locator('[data-test-selector="chat-line-message"]')
        count = await chat_lines.count()
        
        start_idx = max(0, count - limit)
        for i in range(start_idx, count):
            line = chat_lines.nth(i)
            try:
                username_el = line.locator('[data-a-target="chat-message-username"]')
                message_el = line.locator('[data-a-target="chat-message-text"]')
                
                username = await username_el.inner_text() if await username_el.count() > 0 else "Unknown"
                message = await message_el.inner_text() if await message_el.count() > 0 else ""
                
                messages.append({"username": username.strip(), "message": message.strip()})
            except Exception as e:
                logger.debug(f"Error parsing chat line: {e}")
        
        return messages

    async def get_viewer_count(self) -> int:
        """Get current viewer count."""
        viewer_el = self._page.locator('[data-a-target="live-badge"]')
        try:
            text = await viewer_el.inner_text()
            # Extract number from text like "1.2K viewers"
            import re
            match = re.search(r'([\d,.]+[KMB]?)', text)
            if match:
                num_str = match.group(1).replace(',', '')
                multiplier = {'K': 1000, 'M': 1000000, 'B': 1000000000}.get(num_str[-1].upper(), 1)
                if num_str[-1].upper() in ['K', 'M', 'B']:
                    return int(float(num_str[:-1]) * multiplier)
                return int(float(num_str))
        except Exception:
            pass
        return 0

    async def is_live(self) -> bool:
        """Check if the stream is live."""
        live_badge = self._page.locator('[data-a-target="live-badge"]')
        return await live_badge.count() > 0
