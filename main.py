#!/usr/bin/env python3
"""
Stella-Nurse Robot Main Application
"""

import asyncio
import logging
from sensors.heart import HeartRateSensor
from sensors.temperature import TemperatureSensor
from voice.elevenlabs import VoiceSystem
from wakeword.listener import WakeWordListener
from ai.langchain_agent import NurseAgent
from display.face import FaceDisplay

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StellaNurse:
    def __init__(self):
        self.heart_sensor = HeartRateSensor()
        self.temp_sensor = TemperatureSensor()
        self.voice = VoiceSystem()
        self.wakeword = WakeWordListener()
        self.agent = NurseAgent()
        self.display = FaceDisplay()
    
    async def start(self):
        """Start the Stella-Nurse robot"""
        logger.info("Starting Stella-Nurse...")
        
        # Initialize all systems
        await self.display.show_idle()
        
        # Main loop
        while True:
            # Wait for wake word
            if await self.wakeword.listen():
                await self.handle_interaction()
            
            await asyncio.sleep(0.1)
    
    async def handle_interaction(self):
        """Handle user interaction"""
        logger.info("Wake word detected, starting interaction")
        await self.display.show_happy()
        
        # Get sensor data
        heart_rate = await self.heart_sensor.read()
        temperature = await self.temp_sensor.read()
        
        # Process with AI agent
        response = await self.agent.process(heart_rate, temperature)
        
        # Speak response
        await self.display.show_speaking()
        await self.voice.speak(response)
        
        await self.display.show_idle()


async def main():
    stella = StellaNurse()
    await stella.start()


if __name__ == "__main__":
    asyncio.run(main())
