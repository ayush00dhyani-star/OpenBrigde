"""
MCP Server for OpenBridge
Exposes OpenBridge as an MCP tool for AI models.
"""

import asyncio
import json
import logging
import sys
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("openbridge.mcp")


class MCPServer:
    """Simple MCP server that exposes OpenBridge actions."""
    
    def __init__(self, bridge_instance=None):
        self.bridge = bridge_instance
        self.tools = {
            "send_chat_message": self.send_chat_message,
            "create_clip": self.create_clip,
            "get_stream_info": self.get_stream_info,
            "get_chat_history": self.get_chat_history,
            "get_analytics": self.get_analytics,
        }

    async def send_chat_message(self, message: str) -> dict:
        """Send a message in the stream chat."""
        if not self.bridge:
            return {"error": "Bridge not connected"}
        await self.bridge.browser.send_chat_message(message)
        return {"success": True, "message": message}

    async def create_clip(self) -> dict:
        """Create a clip of the current stream moment."""
        if not self.bridge:
            return {"error": "Bridge not connected"}
        await self.bridge.browser.click_clip_button()
        return {"success": True, "action": "clip_created"}

    async def get_stream_info(self) -> dict:
        """Get current stream information."""
        if not self.bridge:
            return {"error": "Bridge not connected"}
        is_live = await self.bridge.browser.is_live()
        viewers = await self.bridge.browser.get_viewer_count()
        return {
            "live": is_live,
            "viewers": viewers,
            "channel": self.bridge.channel,
        }

    async def get_chat_history(self, limit: int = 50) -> dict:
        """Get recent chat messages."""
        if not self.bridge:
            return {"error": "Bridge not connected"}
        messages = await self.bridge.browser.get_chat_messages(limit)
        return {"messages": messages}

    async def get_analytics(self) -> dict:
        """Get stream analytics summary."""
        if not self.bridge:
            return {"error": "Bridge not connected"}
        # Would aggregate data from memory store
        return {
            "channel": self.bridge.channel,
            "status": "analytics would be here",
        }

    async def handle_request(self, request: dict) -> dict:
        """Handle an incoming MCP request."""
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "list_tools":
            return {
                "tools": [
                    {
                        "name": name,
                        "description": func.__doc__,
                    }
                    for name, func in self.tools.items()
                ]
            }
        
        if method == "call_tool":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            
            if tool_name not in self.tools:
                return {"error": f"Unknown tool: {tool_name}"}
            
            try:
                result = await self.tools[tool_name](**tool_args)
                return {"result": result}
            except Exception as e:
                return {"error": str(e)}
        
        return {"error": f"Unknown method: {method}"}

    async def run_stdio(self):
        """Run MCP server over stdio."""
        logger.info("MCP Server started (stdio mode)")
        
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                if not line:
                    break
                
                request = json.loads(line)
                response = await self.handle_request(request)
                
                print(json.dumps(response), flush=True)
                
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON: {e}")
            except Exception as e:
                logger.error(f"Error handling request: {e}")


async def main():
    server = MCPServer()
    await server.run_stdio()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("MCP Server stopped")
