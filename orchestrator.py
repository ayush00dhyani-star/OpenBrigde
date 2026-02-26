"""
OpenBridge — Orchestrator
==========================
Spins up all agents. Manages the event bus. Free — no limits, no billing.
"""

import asyncio
import logging
import signal
from datetime import datetime
from typing import Optional

from core.browser.controller import BrowserController
from core.events.bus import EventBus, EventType
from core.memory.store import MemoryStore
from core.agents.base import BaseAgent

logger = logging.getLogger("openbridge.orchestrator")


class OpenBridge:
    def __init__(self, config: dict):
        self.config = config
        self.channel  = config["channel"]
        self.streamer = config.get("streamer", config["channel"])

        self.bus     = EventBus()
        self.memory  = MemoryStore()
        self.browser = BrowserController(
            profile_name=self.channel,
            headless=config.get("headless", False),
        )
        self._agents: dict[str, BaseAgent] = {}
        self._running = False
        self._start_time: Optional[datetime] = None

    # ── Lifecycle ────────────────────────────────────────────── #

    async def run(self):
        await self.memory.init()
        await self.browser.start()
        await self.bus.start()
        await self._setup_agents()

        for agent in self._agents.values():
            agent.start()

        self._running = True
        self._start_time = datetime.now()

        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(self.stop()))

        logger.info(f"✅  OpenBridge live on #{self.channel}  — Ctrl+C to stop")

        # Keep alive
        while self._running:
            await asyncio.sleep(1)

    async def stop(self):
        logger.info("[Orchestrator] Stopping...")
        self._running = False
        for agent in self._agents.values():
            await agent.stop()
        await self.browser.stop()
        await self.memory.close()
        logger.info("[Orchestrator] Stopped.")

    # ── Agent wiring ─────────────────────────────────────────── #

    async def _setup_agents(self):
        cfg  = self.config.get("agents", {})
        acfg = lambda key: cfg.get(key, {})

        # Shared legacy queue for agents that still use raw asyncio.Queue
        legacy_bus: asyncio.Queue = asyncio.Queue(maxsize=1000)

        from core.platforms.twitch import TwitchConnector
        twitch = TwitchConnector(self.browser, self.channel)

        # Always-on agents
        if acfg("chat").get("enabled", True):
            from core.agents.chat_commander import ChatCommanderAgent
            self._agents["chat"] = ChatCommanderAgent(
                event_bus=legacy_bus,
                browser=self.browser,
                channel=self.channel,
                streamer_name=self.streamer,
                config=acfg("chat"),
            )

        if acfg("clip").get("enabled", True):
            from core.agents.clip_sniper import ClipSniperAgent
            self._agents["clip"] = ClipSniperAgent(
                event_bus=legacy_bus,
                browser=self.browser,
                channel=self.channel,
                config=acfg("clip"),
            )

        if acfg("shield").get("enabled", True):
            from core.agents.shield_guard import ShieldGuardAgent
            self._agents["shield"] = ShieldGuardAgent(
                event_bus=legacy_bus,
                memory=self.memory,
                channel=self.channel,
                config=acfg("shield"),
            )

        if acfg("intel").get("enabled", True):
            from core.agents.growth_intel import GrowthIntelAgent
            self._agents["intel"] = GrowthIntelAgent(
                event_bus=legacy_bus,
                memory=self.memory,
                twitch_connector=twitch,
                channel=self.channel,
                config=acfg("intel"),
            )

        if acfg("social").get("enabled", False):
            from core.agents.social_ghost import SocialGhostAgent
            self._agents["social"] = SocialGhostAgent(
                event_bus=legacy_bus,
                browser=self.browser,
                config=acfg("social"),
            )

        if acfg("revenue").get("enabled", False):
            from core.agents.revenue_pilot import RevenuePilotAgent
            self._agents["revenue"] = RevenuePilotAgent(
                event_bus=legacy_bus,
                twitch_connector=twitch,
                config=acfg("revenue"),
            )

        n = len(self._agents)
        logger.info(f"[Orchestrator] {n} agent{'s' if n != 1 else ''} ready: {list(self._agents)}")

    # ── Status ───────────────────────────────────────────────── #

    def status(self) -> dict:
        uptime = None
        if self._start_time:
            uptime = str(datetime.now() - self._start_time).split(".")[0]
        return {
            "channel": self.channel,
            "running": self._running,
            "uptime":  uptime,
            "agents":  {k: v.report() for k, v in self._agents.items()},
        }
