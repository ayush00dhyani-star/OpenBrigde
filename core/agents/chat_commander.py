"""
Chat Commander Agent
Monitors chat, responds to commands, welcomes raiders, detects hype.
"""

import asyncio
import logging
import re
from collections import deque
from datetime import datetime, timedelta

from core.agents.base import BaseAgent
from core.browser.controller import BrowserController
from core.events.bus import Event, EventType

logger = logging.getLogger("openbridge.chat_commander")


class ChatCommanderAgent(BaseAgent):
    def __init__(
        self,
        event_bus: asyncio.Queue,
        browser: BrowserController,
        channel: str,
        streamer_name: str,
        config: dict | None = None,
    ):
        super().__init__("chat_commander", config)
        self.event_bus = event_bus
        self.browser = browser
        self.channel = channel
        self.streamer_name = streamer_name
        
        # Config
        self.hype_threshold = self.config.get("hype_threshold", 15)
        self.command_cooldown = self.config.get("command_cooldown", 30)
        self.welcome_raiders = self.config.get("welcome_raiders", True)
        self.socials_message = self.config.get("socials_message", "")
        self.custom_commands = self.config.get("custom_commands", {})
        
        # State
        self._recent_messages: deque = deque(maxlen=100)
        self._last_command_time: dict[str, datetime] = {}
        self._hype_window: deque = deque()
        self._known_users: set = set()
        self._raid_detected = False

    async def run(self):
        """Main agent loop."""
        logger.info(f"Chat Commander monitoring #{self.channel}")
        
        while self._running:
            try:
                # Navigate to channel if not already there
                if not self.browser.is_running:
                    await asyncio.sleep(5)
                    continue
                
                # Get recent chat messages
                messages = await self.browser.get_chat_messages(limit=20)
                
                for msg in messages:
                    username = msg["username"]
                    text = msg["message"]
                    
                    # Skip if we've seen this message
                    msg_key = f"{username}:{text}"
                    if msg_key in self._recent_messages:
                        continue
                    self._recent_messages.append(msg_key)
                    
                    # Track user activity
                    self._track_user(username)
                    
                    # Check for commands
                    if text.startswith("!"):
                        await self._handle_command(username, text)
                    
                    # Track hype
                    self._track_hype()
                
                # Check for raids (simplified detection)
                await self._check_for_raids()
                
                await asyncio.sleep(2)  # Poll interval
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Chat Commander error: {e}")
                self.increment_stat("errors")
                await asyncio.sleep(5)

    def _track_user(self, username: str):
        """Track user activity."""
        if username not in self._known_users:
            # New user detected
            self._known_users.add(username)
            logger.info(f"New chatter: {username}")
        
        # Add to hype window
        self._hype_window.append(datetime.now())

    def _track_hype(self):
        """Detect hype moments."""
        now = datetime.now()
        window_start = now - timedelta(seconds=10)
        
        # Clean old entries
        while self._hype_window and self._hype_window[0] < window_start:
            self._hype_window.popleft()
        
        # Check threshold
        if len(self._hype_window) >= self.hype_threshold:
            logger.info(f"HYPE DETECTED! {len(self._hype_window)} messages in 10s")
            self.event_bus.put_nowait(Event(
                type=EventType.HYPE_DETECTED,
                data={"count": len(self._hype_window)},
                source="chat_commander",
            ))
            self._hype_window.clear()  # Reset to avoid spam

    async def _handle_command(self, username: str, text: str):
        """Handle chat commands."""
        parts = text.split()
        command = parts[0].lower().lstrip("!")
        
        # Check cooldown
        now = datetime.now()
        last_time = self._last_command_time.get(command)
        if last_time and (now - last_time).total_seconds() < self.command_cooldown:
            return
        
        self._last_command_time[command] = now
        
        # Custom commands
        if command in self.custom_commands:
            response = self.custom_commands[command]
            await self.browser.send_chat_message(response)
            self.increment_stat("actions_taken")
            logger.info(f"Responded to !{command}")
            return
        
        # Built-in commands
        if command == "socials" and self.socials_message:
            await self.browser.send_chat_message(self.socials_message)
            self.increment_stat("actions_taken")
            return
        
        if command == "lurk":
            await self.browser.send_chat_message(f"Thanks for the lurk, {username}!")
            self.increment_stat("actions_taken")
            return
        
        if command == "uptime":
            # Would need stream start time tracking
            await self.browser.send_chat_message("Stream started recently! Check !schedule for stream times.")
            self.increment_stat("actions_taken")
            return
        
        # Publish custom command event for other agents
        self.event_bus.put_nowait(Event(
            type=EventType.CUSTOM_COMMAND,
            data={"command": command, "username": username, "args": parts[1:]},
            source="chat_commander",
        ))

    async def _check_for_raids(self):
        """Check for raid detection (simplified)."""
        # This would normally analyze incoming user patterns
        # For now, just a placeholder
        pass
