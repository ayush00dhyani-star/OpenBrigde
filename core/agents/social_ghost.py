"""
Social Ghost Agent
Posts clips and announcements to Twitter and Discord.
"""

import asyncio
import logging

from core.agents.base import BaseAgent
from core.browser.controller import BrowserController

logger = logging.getLogger("openbridge.social_ghost")


class SocialGhostAgent(BaseAgent):
    def __init__(
        self,
        event_bus: asyncio.Queue,
        browser: BrowserController,
        config: dict | None = None,
    ):
        super().__init__("social_ghost", config)
        self.event_bus = event_bus
        self.browser = browser
        
        # Config
        self.platforms = self.config.get("platforms", ["twitter", "discord"])
        self.post_on_go_live = self.config.get("post_on_go_live", True)
        self.post_clips = self.config.get("post_clips", True)
        self.discord_server = self.config.get("discord_server", "")
        self.discord_channel = self.config.get("discord_channel", "")
        
        # State
        self._posted_go_live = False
        self._pending_posts: list[dict] = []

    async def run(self):
        """Main agent loop."""
        logger.info(f"Social Ghost ready (platforms: {self.platforms})")
        
        while self._running:
            try:
                # Check for clip events
                await self._check_for_clips()
                
                # Check for go-live events
                await self._check_go_live()
                
                await asyncio.sleep(5)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Social Ghost error: {e}")
                self.increment_stat("errors")
                await asyncio.sleep(5)

    async def _check_for_clips(self):
        """Check for new clips to post."""
        while not self.event_bus.empty():
            try:
                event = self.event_bus.get_nowait()
                if event.type.value == "clip_created":
                    if self.post_clips:
                        await self._post_clip(event.data)
            except asyncio.QueueEmpty:
                break

    async def _check_go_live(self):
        """Check if stream just went live."""
        # Would check stream status
        # For now, simplified
        pass

    async def _post_clip(self, clip_data: dict):
        """Post a clip to configured platforms."""
        clip_url = clip_data.get("url", "")
        clip_title = clip_data.get("title", "New clip!")
        
        message = f"🎮 {clip_title}\n{clip_url}"
        
        for platform in self.platforms:
            try:
                if platform == "twitter":
                    await self._post_to_twitter(message)
                elif platform == "discord":
                    await self._post_to_discord(message)
            except Exception as e:
                logger.error(f"Failed to post to {platform}: {e}")

    async def _post_to_twitter(self, message: str):
        """Post to Twitter/X."""
        logger.info(f"Posting to Twitter: {message[:50]}...")
        # Would use browser to navigate to Twitter and post
        # Or use Twitter API if credentials provided
        self.increment_stat("posts_twitter")

    async def _post_to_discord(self, message: str):
        """Post to Discord."""
        logger.info(f"Posting to Discord ({self.discord_channel}): {message[:50]}...")
        # Would use Discord webhook or browser automation
        self.increment_stat("posts_discord")

    async def post_go_live_announcement(self):
        """Post that the stream is now live."""
        message = f"🔴 LIVE NOW! Come hang out!\n\nhttps://twitch.tv/{self.browser.profile_name if hasattr(self.browser, 'profile_name') else 'channel'}"
        
        for platform in self.platforms:
            try:
                if platform == "twitter":
                    await self._post_to_twitter(message)
                elif platform == "discord":
                    await self._post_to_discord(message)
            except Exception as e:
                logger.error(f"Failed to post go-live to {platform}: {e}")
        
        self._posted_go_live = True
        self.increment_stat("announcements")
