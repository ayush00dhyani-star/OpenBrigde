"""
Event Bus for OpenBridge
Handles events between agents.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable

logger = logging.getLogger("openbridge.events")


class EventType(str, Enum):
    CHAT_MESSAGE = "chat_message"
    HYPE_DETECTED = "hype_detected"
    CLIP_CREATED = "clip_created"
    RAID_DETECTED = "raid_detected"
    SUB_RECEIVED = "sub_received"
    VIEWER_MILESTONE = "viewer_milestone"
    STREAM_STARTED = "stream_started"
    STREAM_ENDED = "stream_ended"
    MOD_ACTION = "mod_action"
    CUSTOM_COMMAND = "custom_command"


@dataclass
class Event:
    type: EventType
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = "unknown"


class EventBus:
    def __init__(self):
        self._subscribers: dict[EventType, list[Callable]] = {}
        self._queue: asyncio.Queue[Event] = asyncio.Queue(maxsize=1000)
        self._running = False
        self._task: asyncio.Task | None = None

    async def start(self):
        """Start the event bus processor."""
        self._running = True
        logger.info("Event bus started.")

    async def stop(self):
        """Stop the event bus."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Event bus stopped.")

    def subscribe(self, event_type: EventType, callback: Callable):
        """Subscribe to an event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
        logger.debug(f"Subscribed to {event_type.value}")

    def publish(self, event: Event):
        """Publish an event to the queue."""
        if not self._running:
            return
        try:
            self._queue.put_nowait(event)
            logger.debug(f"Published event: {event.type.value}")
        except asyncio.QueueFull:
            logger.warning("Event queue full, dropping event.")

    async def process_events(self):
        """Process events from the queue."""
        while self._running:
            try:
                event = await asyncio.wait_for(self._queue.get(), timeout=1.0)
                await self._dispatch(event)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing event: {e}")

    async def _dispatch(self, event: Event):
        """Dispatch event to subscribers."""
        callbacks = self._subscribers.get(event.type, [])
        for callback in callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event)
                else:
                    callback(event)
            except Exception as e:
                logger.error(f"Error in event callback: {e}")

    async def wait_for_event(self, event_type: EventType, timeout: float | None = None) -> Event | None:
        """Wait for a specific event type."""
        start_time = asyncio.get_event_loop().time()
        while self._running:
            try:
                event = await asyncio.wait_for(self._queue.get(), timeout=0.5)
                if event.type == event_type:
                    # Put it back for other subscribers
                    self._queue.put_nowait(event)
                    return event
                # Put it back for other subscribers
                self._queue.put_nowait(event)
            except asyncio.TimeoutError:
                pass
            
            if timeout and (asyncio.get_event_loop().time() - start_time) > timeout:
                return None
        
        return None
