"""
Memory Store for OpenBridge
Persistent storage for agent memory and stream data.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

logger = logging.getLogger("openbridge.memory")


class MemoryStore:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self._cache: dict[str, Any] = {}
        self._lock = asyncio.Lock()

    async def init(self):
        """Initialize the memory store."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        await self._load_cache()
        logger.info("Memory store initialized.")

    async def close(self):
        """Save cache before closing."""
        await self._save_cache()
        logger.info("Memory store closed.")

    async def _load_cache(self):
        """Load cache from disk."""
        cache_file = self.data_dir / "memory.json"
        if cache_file.exists():
            try:
                with open(cache_file) as f:
                    self._cache = json.load(f)
                logger.debug(f"Loaded memory cache from {cache_file}")
            except Exception as e:
                logger.error(f"Error loading cache: {e}")
                self._cache = {}

    async def _save_cache(self):
        """Save cache to disk."""
        cache_file = self.data_dir / "memory.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump(self._cache, f, indent=2, default=str)
            logger.debug(f"Saved memory cache to {cache_file}")
        except Exception as e:
            logger.error(f"Error saving cache: {e}")

    async def get(self, key: str, default: Any = None) -> Any:
        """Get a value from memory."""
        async with self._lock:
            return self._cache.get(key, default)

    async def set(self, key: str, value: Any, persist: bool = True):
        """Set a value in memory."""
        async with self._lock:
            self._cache[key] = value
            if persist:
                await self._save_cache()

    async def delete(self, key: str):
        """Delete a value from memory."""
        async with self._lock:
            self._cache.pop(key, None)
            await self._save_cache()

    async def append_to_list(self, key: str, item: Any, max_length: int = 1000):
        """Append an item to a list in memory."""
        async with self._lock:
            if key not in self._cache:
                self._cache[key] = []
            self._cache[key].append(item)
            # Trim if exceeds max length
            if len(self._cache[key]) > max_length:
                self._cache[key] = self._cache[key][-max_length:]
            await self._save_cache()

    async def get_list(self, key: str, default: list | None = None) -> list:
        """Get a list from memory."""
        async with self._lock:
            return self._cache.get(key, default or [])

    # Stream-specific helpers
    async def record_chat_message(self, username: str, message: str, timestamp: datetime = None):
        """Record a chat message."""
        entry = {
            "username": username,
            "message": message,
            "timestamp": (timestamp or datetime.now()).isoformat(),
        }
        await self.append_to_list("chat_history", entry, max_length=5000)

    async def get_recent_chat(self, limit: int = 100) -> list[dict]:
        """Get recent chat messages."""
        history = await self.get_list("chat_history", [])
        return history[-limit:]

    async def record_clip(self, clip_id: str, title: str, url: str, timestamp: datetime = None):
        """Record a created clip."""
        entry = {
            "clip_id": clip_id,
            "title": title,
            "url": url,
            "timestamp": (timestamp or datetime.now()).isoformat(),
        }
        await self.append_to_list("clips", entry, max_length=500)

    async def get_clips(self, limit: int = 50) -> list[dict]:
        """Get recorded clips."""
        return await self.get_list("clips", [])[-limit:]

    async def record_viewer_count(self, count: int, timestamp: datetime = None):
        """Record viewer count."""
        entry = {
            "count": count,
            "timestamp": (timestamp or datetime.now()).isoformat(),
        }
        await self.append_to_list("viewer_history", entry, max_length=10000)

    async def get_peak_viewers(self, session_key: str = "current_session") -> int:
        """Get peak viewers for current session."""
        history = await self.get_list("viewer_history", [])
        if not history:
            return 0
        return max(entry.get("count", 0) for entry in history)

    async def record_mod_action(self, action: str, target: str, reason: str = ""):
        """Record a moderation action."""
        entry = {
            "action": action,
            "target": target,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
        }
        await self.append_to_list("mod_actions", entry, max_length=1000)

    async def get_mod_actions(self, limit: int = 100) -> list[dict]:
        """Get recent moderation actions."""
        return await self.get_list("mod_actions", [])[-limit:]

    async def increment_counter(self, key: str, amount: int = 1) -> int:
        """Increment a counter and return new value."""
        async with self._lock:
            current = self._cache.get(key, 0)
            new_value = current + amount
            self._cache[key] = new_value
            await self._save_cache()
            return new_value

    async def reset_session(self):
        """Reset session-specific data."""
        async with self._lock:
            # Keep some data, clear session-specific
            session_keys = ["current_session", "session_start", "session_viewers"]
            for key in session_keys:
                self._cache.pop(key, None)
            await self._save_cache()
