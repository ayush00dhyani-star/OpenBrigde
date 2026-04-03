"""
Twitch Connector for OpenBridge
Handles Twitch-specific operations.
"""

import logging

logger = logging.getLogger("openbridge.twitch")


class TwitchConnector:
    def __init__(self, browser, channel: str):
        self.browser = browser
        self.channel = channel

    async def get_stream_info(self) -> dict | None:
        """Get current stream information."""
        try:
            is_live = await self.browser.is_live()
            viewer_count = await self.browser.get_viewer_count()
            
            return {
                "live": is_live,
                "viewers": viewer_count,
                "channel": self.channel,
            }
        except Exception as e:
            logger.error(f"Error getting stream info: {e}")
            return None

    async def send_chat_message(self, message: str):
        """Send a message in Twitch chat."""
        await self.browser.send_chat_message(message)

    async def create_clip(self) -> str | None:
        """Create a Twitch clip and return the URL."""
        await self.browser.click_clip_button()
        # Would need to wait for clip creation and get URL
        return None

    async def get_moderators(self) -> list[str]:
        """Get list of channel moderators."""
        # Would scrape or use API
        return []

    async def timeout_user(self, username: str, duration: int, reason: str = ""):
        """Timeout a user."""
        command = f"/timeout {username} {duration} {reason}".strip()
        await self.browser.send_chat_message(command)

    async def ban_user(self, username: str, reason: str = ""):
        """Ban a user."""
        command = f"/ban {username} {reason}".strip()
        await self.browser.send_chat_message(command)
