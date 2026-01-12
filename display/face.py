"""
Face Display Module
"""

import asyncio
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class FaceDisplay:
    def __init__(self):
        self.assets_path = Path(__file__).parent.parent / "assets" / "faces"
        self.current_state = "idle"
        logger.info("Face display initialized")
    
    async def show_idle(self):
        """Display idle face"""
        self.current_state = "idle"
        logger.info("Showing idle face")
        # TODO: Implement actual display rendering
        await asyncio.sleep(0.1)
    
    async def show_happy(self):
        """Display happy face"""
        self.current_state = "happy"
        logger.info("Showing happy face")
        # TODO: Implement actual display rendering
        await asyncio.sleep(0.1)
    
    async def show_concerned(self):
        """Display concerned face"""
        self.current_state = "concerned"
        logger.info("Showing concerned face")
        # TODO: Implement actual display rendering
        await asyncio.sleep(0.1)
    
    async def show_alert(self):
        """Display alert face"""
        self.current_state = "alert"
        logger.info("Showing alert face")
        # TODO: Implement actual display rendering
        await asyncio.sleep(0.1)
    
    async def show_speaking(self):
        """Display speaking animation"""
        self.current_state = "speaking"
        logger.info("Showing speaking face")
        # TODO: Implement actual speaking animation
        await asyncio.sleep(0.1)
    
    def get_current_state(self) -> str:
        """Get current face state"""
        return self.current_state
