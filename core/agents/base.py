"""
Base Agent for OpenBridge
All agents inherit from this class.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger("openbridge.agents")


class BaseAgent(ABC):
    def __init__(self, name: str, config: dict | None = None):
        self.name = name
        self.config = config or {}
        self._running = False
        self._task: asyncio.Task | None = None
        self._stats = {
            "actions_taken": 0,
            "errors": 0,
            "uptime_seconds": 0,
        }

    @abstractmethod
    async def run(self):
        """Main agent loop. Must be implemented by subclasses."""
        pass

    def start(self):
        """Start the agent."""
        if self._running:
            logger.warning(f"Agent {self.name} is already running.")
            return
        self._running = True
        self._task = asyncio.create_task(self.run())
        logger.info(f"Agent {self.name} started.")

    async def stop(self):
        """Stop the agent."""
        logger.info(f"Stopping agent {self.name}...")
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info(f"Agent {self.name} stopped.")

    @property
    def is_running(self) -> bool:
        return self._running

    def report(self) -> dict:
        """Return agent status report."""
        return {
            "name": self.name,
            "running": self._running,
            "stats": self._stats.copy(),
            "config": self.config,
        }

    def increment_stat(self, key: str, amount: int = 1):
        """Increment a stat counter."""
        if key in self._stats:
            self._stats[key] += amount
        else:
            self._stats[key] = amount
