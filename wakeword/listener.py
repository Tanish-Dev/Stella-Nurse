"""
Wake Word Listener Module
"""

import asyncio
import logging

logger = logging.getLogger(__name__)


class WakeWordListener:
    def __init__(self, wake_word: str = "Stella"):
        self.wake_word = wake_word
        self.is_listening = False
        logger.info(f"Wake word listener initialized with wake word: '{wake_word}'")
    
    async def start(self):
        """Start listening for wake word"""
        self.is_listening = True
        logger.info("Wake word listener started")
    
    async def listen(self) -> bool:
        """Listen for wake word and return True if detected"""
        # TODO: Implement actual wake word detection
        # This could use Porcupine, Snowboy, or similar
        await asyncio.sleep(0.1)
        return False  # Placeholder
    
    async def stop(self):
        """Stop listening for wake word"""
        self.is_listening = False
        logger.info("Wake word listener stopped")
