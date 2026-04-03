"""
Revenue Pilot Agent
Fires sub drives and merch drops at viewer milestones.
"""

import asyncio
import logging

from core.agents.base import BaseAgent

logger = logging.getLogger("openbridge.revenue_pilot")


class RevenuePilotAgent(BaseAgent):
    def __init__(
        self,
        event_bus: asyncio.Queue,
        twitch_connector: object,
        config: dict | None = None,
    ):
        super().__init__("revenue_pilot", config)
        self.event_bus = event_bus
        self.twitch_connector = twitch_connector
        
        # Config - milestone triggers
        self.milestones = self.config.get("milestones", [100, 500, 1000, 5000])
        self.sub_drive_message = self.config.get(
            "sub_drive_message",
            "🎉 SUB DRIVE! Let's hit {target} viewers! Use your subs!",
        )
        self.merch_drop_message = self.config.get(
            "merch_drop_message",
            "👕 MERCH DROP! Check out the new designs at the store!",
        )
        
        # State
        self._triggered_milestones: set = set()
        self._current_viewers = 0

    async def run(self):
        """Main agent loop."""
        logger.info("Revenue Pilot monitoring for milestones")
        
        while self._running:
            try:
                # Check viewer count against milestones
                await self._check_milestones()
                
                # Listen for sub events
                await self._check_sub_events()
                
                await asyncio.sleep(10)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Revenue Pilot error: {e}")
                self.increment_stat("errors")
                await asyncio.sleep(5)

    async def _check_milestones(self):
        """Check if we've hit a viewer milestone."""
        # Would get actual viewer count from browser or API
        # For now, simplified
        pass

    async def _check_sub_events(self):
        """Check for subscription events."""
        while not self.event_bus.empty():
            try:
                event = self.event_bus.get_nowait()
                if event.type.value == "sub_received":
                    await self._handle_sub(event.data)
                elif event.type.value == "viewer_milestone":
                    await self._handle_milestone(event.data)
            except asyncio.QueueEmpty:
                break

    async def _handle_sub(self, data: dict):
        """Handle a subscription event."""
        username = data.get("username", "Someone")
        tier = data.get("tier", 1)
        
        logger.info(f"New sub from {username} (tier {tier})")
        self.increment_stat("subs_received")
        
        # Could trigger a thank you message or alert

    async def _handle_milestone(self, data: dict):
        """Handle a viewer milestone."""
        viewers = data.get("count", 0)
        
        if viewers in self._triggered_milestones:
            return  # Already triggered
        
        self._triggered_milestones.add(viewers)
        logger.info(f"Milestone reached: {viewers} viewers!")
        
        # Trigger appropriate action
        if viewers >= 1000:
            await self._trigger_merch_drop()
        else:
            await self._trigger_sub_drive(viewers)
        
        self.increment_stat("milestones_hit")

    async def _trigger_sub_drive(self, target: int):
        """Trigger a sub drive announcement."""
        message = self.sub_drive_message.format(target=target)
        logger.info(f"Sub drive triggered: {message}")
        # Would send to chat via browser
        self.increment_stat("sub_drives")

    async def _trigger_merch_drop(self):
        """Trigger a merch drop announcement."""
        message = self.merch_drop_message
        logger.info(f"Merch drop triggered: {message}")
        # Would send to chat via browser
        self.increment_stat("merch_drops")
