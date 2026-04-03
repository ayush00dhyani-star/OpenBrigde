"""
Shield Guard Agent
Moderation that understands gaming culture.
"""

import asyncio
import logging
import re
from datetime import datetime

from core.agents.base import BaseAgent
from core.memory.store import MemoryStore

logger = logging.getLogger("openbridge.shield_guard")


class ShieldGuardAgent(BaseAgent):
    def __init__(
        self,
        event_bus: asyncio.Queue,
        memory: MemoryStore,
        channel: str,
        config: dict | None = None,
    ):
        super().__init__("shield_guard", config)
        self.event_bus = event_bus
        self.memory = memory
        self.channel = channel
        
        # Config
        self.sensitivity = self.config.get("sensitivity", "medium")
        self.timeout_duration = self.config.get("timeout_duration", 600)
        
        # Sensitivity multipliers
        self._sensitivity_multipliers = {
            "low": 0.5,
            "medium": 1.0,
            "high": 2.0,
        }
        
        # Banned patterns (gaming-friendly)
        self._banned_patterns = [
            r"(?i)\b(hate|racist|nazi|kkk)\b",
            r"(?i)\b(die|death|suicide)\b.*\b(yourself|you)\b",
            r"(?i)\b(rape|raping)\b",
            r"(?i)(https?://)?[^\s]*\.(com|net|org|xyz|top)[^\s]*",  # Links
        ]
        
        # Allowed gaming terms that might trigger false positives
        self._allowed_terms = [
            "gg ez",
            "git gud",
            "noob",
            "trash",
            "diff",
            "jungle diff",
            "mid diff",
        ]
        
        # User warning tracking
        self._user_warnings: dict[str, int] = {}

    async def run(self):
        """Main agent loop."""
        logger.info(f"Shield Guard protecting #{self.channel} (sensitivity: {self.sensitivity})")
        
        while self._running:
            try:
                # Check for mod action events
                await self._process_events()
                
                await asyncio.sleep(1)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Shield Guard error: {e}")
                self.increment_stat("errors")
                await asyncio.sleep(5)

    async def _process_events(self):
        """Process moderation events."""
        while not self.event_bus.empty():
            try:
                event = self.event_bus.get_nowait()
                if event.type.value == "chat_message":
                    await self._analyze_message(event.data)
            except asyncio.QueueEmpty:
                break

    async def _analyze_message(self, data: dict):
        """Analyze a message for violations."""
        username = data.get("username", "")
        message = data.get("message", "")
        
        # Skip if message contains allowed terms
        for allowed in self._allowed_terms:
            if allowed.lower() in message.lower():
                return
        
        # Check against banned patterns
        multiplier = self._sensitivity_multipliers.get(self.sensitivity, 1.0)
        violation_score = 0
        
        for pattern in self._banned_patterns:
            if re.search(pattern, message):
                violation_score += 1 * multiplier
        
        # Take action if score exceeds threshold
        if violation_score >= 1.0:
            await self._take_action(username, message, violation_score)

    async def _take_action(self, username: str, message: str, score: float):
        """Take moderation action."""
        # Track warnings
        warnings = self._user_warnings.get(username, 0) + 1
        self._user_warnings[username] = warnings
        
        if warnings >= 3:
            # Timeout user
            logger.warning(f"Timing out {username} (score: {score}, warnings: {warnings})")
            # Would call browser to timeout user
            await self.memory.record_mod_action(
                action="timeout",
                target=username,
                reason=f"Repeated violations (score: {score:.1f})",
            )
            self.increment_stat("timeouts")
        else:
            logger.info(f"Warning for {username} (score: {score}, warning #{warnings})")
            await self.memory.record_mod_action(
                action="warning",
                target=username,
                reason=f"Potential violation (score: {score:.1f})",
            )
            self.increment_stat("warnings")
