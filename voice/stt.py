import asyncio
import logging
import speech_recognition as sr
from functools import partial

logger = logging.getLogger(__name__)

class STTSystem:
    def __init__(self, model: str = "google"):
        self.model = model
        self.recognizer = sr.Recognizer()
        self.microphone = None
        try:
             self.microphone = sr.Microphone()
        except Exception as e:
            logger.error(f"Could not initialize microphone: {e}")
        logger.info(f"STT System initialized using {model} (via SpeechRecognition)")
        
    async def listen_and_transcribe(self) -> str:
        """
        Listens to the microphone and returns text.
        """
        if not self.microphone:
            logger.warning("No microphone available. Returning mock text.")
            await asyncio.sleep(2)
            return "I am feeling a bit dizzy."

        logger.info("Listening for speech...")
        
        loop = asyncio.get_running_loop()
        try:
            # Run blocking listen in executor
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Listen with timeout
                audio = await loop.run_in_executor(
                    None, 
                    partial(self.recognizer.listen, source, timeout=5, phrase_time_limit=10)
                )
            
            logger.info("Processing audio...")
            # Transcribe
            # For real Whisper, use recognize_whisper(audio) - requires openai-whisper installed
            # For now, using Google (fast, free) to verify pipeline
            text = await loop.run_in_executor(
                None, 
                partial(self.recognizer.recognize_google, audio)
            )
            # text = await loop.run_in_executor(None, partial(self.recognizer.recognize_whisper, audio))
            
            logger.info(f"Transcribed: {text}")
            return text
            
        except sr.WaitTimeoutError:
            logger.info("No speech detected (timeout).")
            return ""
        except sr.UnknownValueError:
            logger.info("Could not understand audio.")
            return ""
        except Exception as e:
            logger.error(f"STT Error: {e}")
            return ""
