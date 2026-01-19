import asyncio
import logging
import signal
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MainPipeline")

from ai.langchain_agent import NurseAgent
from voice.elevenlabs import VoiceSystem
from voice.stt import STTSystem

class PipelineManager:
    def __init__(self):
        self.agent = NurseAgent()
        # Pass explicit key if needed, or let class handle env var
        self.tts = VoiceSystem(api_key=os.getenv("ELEVENLABS_API_KEY"))
        self.stt = STTSystem()
        self.running = True
        self.interrupted = False

    async def setup(self):
        await self.agent.initialize()
        await self.tts.initialize()
        logger.info("Pipeline components initialized.")

    async def run_loop(self):
        """
        Main Event Loop:
        Mic -> STT -> Agent -> TTS
        """
        logger.info("Starting Medical Voice Agent Pipeline...")
        print("System is ready. (Simulating user input)")
        
        while self.running:
            try:
                # 1. Listen (Blocking or Async wait for VAD)
                # In a real system, we'd have a VAD task running in parallel to TTS
                # If VAD detects speech during TTS, we call self.tts.stop()
                
                # Simulation:
                user_text = await self.stt.listen_and_transcribe()
                
                if not user_text:
                    continue
                    
                print(f"User: {user_text}")
                
                # 2. Check Interruption (simulation logic)
                # Note: In real code, VAD would set a flag or cancel the TTS task
                if self.tts.is_speaking:
                    logger.info("User spoke while agent was speaking -> Stopping TTS")
                    self.tts.stop()
                
                # 3. Process with Agent
                response_stream = self.agent.process_stream(user_text)
                
                # 4. Speak Response (Streamed)
                await self.tts.stream_audio(response_stream)
                
                # Loop simulation delay
                await asyncio.sleep(1)
                
                # For demo purposes, stop after one interaction
                # self.running = False 
                
            except KeyboardInterrupt:
                logger.info("Stopping pipeline...")
                self.running = False
            except Exception as e:
                logger.error(f"Pipeline error: {e}")
                await asyncio.sleep(1)

    def stop(self):
        self.running = False

async def main():
    pipeline = PipelineManager()
    
    # Handle signals
    def signal_handler(sig, frame):
        logger.info("Signal received, shutting down...")
        pipeline.stop()
        
    signal.signal(signal.SIGINT, signal_handler)
    
    await pipeline.setup()
    await pipeline.run_loop()

if __name__ == "__main__":
    asyncio.run(main())
