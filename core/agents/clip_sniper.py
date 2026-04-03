"""
Clip Sniper Agent
Auto-clips when chat goes crazy or at manual trigger.
"""

import asyncio
import logging
from datetime import datetime, timedelta

from core.agents.base import BaseAgent
from core.browser.controller import BrowserController

logger = logging.getLogger("openbridge.clip_sniper")


class ClipSniperAgent(BaseAgent):
    def __init__(
        self,
        event_bus: asyncio.Queue,
        browser: BrowserController,
        channel: str,
        config: dict | None = None,
    ):
        super().__init__("clip_sniper", config)
        self.event_bus = event_bus
        self.browser = browser
        self.channel = channel
        
        # Config
        self.clip_cooldown = self.config.get("clip_cooldown", 60)
        
        # State
        self._last_clip_time: datetime | None = None
        self._pending_clips = 0

    async def run(self):
        """Main agent loop."""
        logger.info(f"Clip Sniper ready for #{self.channel}")
        
        while self._running:
            try:
                # Check for hype events from event bus
                await self._check_for_hype()
                
                # Auto-clip on viewer milestones could go here
                
                await asyncio.sleep(1)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Clip Sniper error: {e}")
                self.increment_stat("errors")
                await asyncio.sleep(5)

    async def _check_for_hype(self):
        """Check for hype events and create clips."""
        # Non-blocking check of event bus
        while not self.event_bus.empty():
            try:
                event = self.event_bus.get_nowait()
                if event.type.value == "hype_detected":
                    await self._create_clip(reason="hype", data=event.data)
            except asyncio.QueueEmpty:
                break

    async def _create_clip(self, reason: str = "manual", data: dict | None = None):
        """Create a clip."""
        now = datetime.now()
        
        # Check cooldown
        if self._last_clip_time:
            elapsed = (now - self._last_clip_time).total_seconds()
            if elapsed < self.clip_cooldown:
                logger.info(f"Clip on cooldown ({elapsed:.0f}s/{self.clip_cooldown}s)")
                return
        
        logger.info(f"Creating clip: {reason}")
        
        try:
            await self.browser.click_clip_button()
            self._last_clip_time = now
            self.increment_stat("actions_taken")
            self.increment_stat("clips_created")
            
            # Record clip in memory (would need memory store reference)
            logger.info(f"Clip created! Reason: {reason}")
            
        except Exception as e:
            logger.error(f"Failed to create clip: {e}")
            self.increment_stat("errors")
