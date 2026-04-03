"""
Growth Intel Agent
Tracks stream analytics and provides reports.
"""

import asyncio
import logging
from datetime import datetime, timedelta

from core.agents.base import BaseAgent
from core.memory.store import MemoryStore

logger = logging.getLogger("openbridge.growth_intel")


class GrowthIntelAgent(BaseAgent):
    def __init__(
        self,
        event_bus: asyncio.Queue,
        memory: MemoryStore,
        twitch_connector: object,
        channel: str,
        config: dict | None = None,
    ):
        super().__init__("growth_intel", config)
        self.event_bus = event_bus
        self.memory = memory
        self.twitch_connector = twitch_connector
        self.channel = channel
        
        # Config
        self.post_stream_summary = self.config.get("post_stream_summary", True)
        
        # State
        self._stream_start_time: datetime | None = None
        self._peak_viewers = 0
        self._chat_messages_count = 0

    async def run(self):
        """Main agent loop."""
        logger.info(f"Growth Intel tracking #{self.channel}")
        
        while self._running:
            try:
                # Track viewer count periodically
                await self._track_viewers()
                
                # Check for stream end
                if self._stream_start_time:
                    await self._check_stream_end()
                
                await asyncio.sleep(30)  # Track every 30 seconds
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Growth Intel error: {e}")
                self.increment_stat("errors")
                await asyncio.sleep(5)

    async def _track_viewers(self):
        """Track viewer count."""
        try:
            # Would get from browser or API
            viewer_count = await self.memory.get("current_viewers", 0)
            
            if viewer_count > 0:
                await self.memory.record_viewer_count(viewer_count)
                
                if viewer_count > self._peak_viewers:
                    self._peak_viewers = viewer_count
                    logger.info(f"New peak viewers: {self._peak_viewers}")
                
                self._chat_messages_count += 1
                
        except Exception as e:
            logger.debug(f"Could not track viewers: {e}")

    async def _check_stream_end(self):
        """Check if stream has ended."""
        # Would check if stream is still live
        # For now, simplified logic
        pass

    async def generate_summary(self) -> dict:
        """Generate a stream summary report."""
        session_data = await self.memory.get_list("viewer_history", [])
        chat_history = await self.memory.get_list("chat_history", [])
        clips = await self.memory.get_list("clips", [])
        mod_actions = await self.memory.get_list("mod_actions", [])
        
        # Calculate stats
        total_chatters = len(set(msg.get("username", "") for msg in chat_history))
        total_messages = len(chat_history)
        
        # Find average viewers
        avg_viewers = 0
        if session_data:
            avg_viewers = sum(entry.get("count", 0) for entry in session_data) / len(session_data)
        
        summary = {
            "channel": self.channel,
            "stream_date": datetime.now().strftime("%Y-%m-%d"),
            "duration_hours": 0,  # Would calculate from start/end time
            "peak_viewers": self._peak_viewers,
            "avg_viewers": round(avg_viewers, 1),
            "total_chatters": total_chatters,
            "total_messages": total_messages,
            "clips_created": len(clips),
            "mod_actions": len(mod_actions),
            "top_chatters": self._get_top_chatters(chat_history, limit=5),
        }
        
        return summary

    def _get_top_chatters(self, chat_history: list, limit: int = 5) -> list[dict]:
        """Get top chatters by message count."""
        chatter_counts: dict[str, int] = {}
        for msg in chat_history:
            username = msg.get("username", "Unknown")
            chatter_counts[username] = chatter_counts.get(username, 0) + 1
        
        sorted_chatters = sorted(chatter_counts.items(), key=lambda x: x[1], reverse=True)
        return [{"username": name, "messages": count} for name, count in sorted_chatters[:limit]]
