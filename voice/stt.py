import asyncio
import logging

logger = logging.getLogger(__name__)

class STTSystem:
    def __init__(self, model: str = "whisper-1"):
        self.model = model
        logger.info(f"STT System initialized with model {model}")
        
    async def listen_and_transcribe(self) -> str:
        """
        Simulates listening to microphone and transcribing audio.
        In production, this would use sounddevice/pyaudio and a local Whisper or API.
        """
        logger.info("Listening (simulated)...")
        # Simulate silence detection and speech
        await asyncio.sleep(2.0) # Listening...
        
        # Simulate returning a user query
        # We can implement a simple input() fallback for testing if no mic
        return "I am feeling a bit dizzy and my chest hurts."
