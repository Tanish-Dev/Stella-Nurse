import asyncio
import logging
from typing import AsyncGenerator

logger = logging.getLogger(__name__)

class VoiceSystem:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.voice_id = "21m00Tcm4TlvDq8ikWAM" # Default voice
        self.is_speaking = False
        logger.info("Voice system initialized")
    
    async def initialize(self):
        """Initialize ElevenLabs connection"""
        if not self.api_key:
             logger.warning("ElevenLabs API Key missing!")
        logger.info("Initializing ElevenLabs voice system...")
    
    async def speak(self, text: str):
        """Convert text to speech and play fully"""
        logger.info(f"Speaking: {text}")
        self.is_speaking = True
        try:
            # audio = generate(text=text, voice=self.voice_id, model="eleven_monolingual_v1")
            # play(audio)
            await asyncio.sleep(len(text) * 0.05) # Simulation
        finally:
            self.is_speaking = False
            
    async def stream_audio(self, text_iterator: AsyncGenerator[str, None]):
        """
        Consumes a text generator and streams audio.
        Handles interruption checking.
        """
        logger.info("Starting audio stream...")
        self.is_speaking = True
        try:
            async for text_chunk in text_iterator:
                if not self.is_speaking: 
                    # Interrupted externally
                    logger.info("TTS Interrupted!")
                    break
                if not text_chunk.strip():
                    continue
                    
                # logger.debug(f"Streaming chunk: {text_chunk}")
                # audio_stream = generate(text=text_chunk, stream=True, ...)
                # stream(audio_stream) 
                
                # Simulation of playback time per chunk
                await asyncio.sleep(len(text_chunk) * 0.05)
                
        except Exception as e:
            logger.error(f"Error in TTS stream: {e}")
        finally:
            self.is_speaking = False
            
    def stop(self):
        """Interrupts speech"""
        if self.is_speaking:
            logger.info("Stopping speech output.")
            self.is_speaking = False
            
    async def set_voice(self, voice_id: str):
        """Set the voice ID to use"""
        self.voice_id = voice_id
        logger.info(f"Voice set to: {voice_id}")
