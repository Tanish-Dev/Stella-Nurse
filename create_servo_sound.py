import numpy as np
import wave
import struct
import math
import os

def generate_servo_sound(filename, duration=0.2, start_freq=200, end_freq=400, sample_rate=44100):
    """
    Generates a synthetic servo motor sound (frequency sweep).
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # Frequency sweep (linear chop)
    # Instantaneous frequency f(t) = start_freq + (end_freq - start_freq) * t / duration
    # Phase is integral of frequency
    # phase(t) = start_freq * t + 0.5 * (end_freq - start_freq) * t^2 / duration
    
    phase = 2 * np.pi * (start_freq * t + 0.5 * (end_freq - start_freq) * t**2 / duration)
    
    # Combine a few harmonics to make it sound more "mechanical"
    waveform = 0.6 * np.sin(phase) + 0.3 * np.sin(phase * 2) + 0.1 * np.sin(phase * 3)
    
    # Apply a slight envelope to avoid clicks
    envelope = np.ones_like(t)
    envelope[:1000] = np.linspace(0, 1, 1000)
    envelope[-1000:] = np.linspace(1, 0, 1000)
    
    audio_data = waveform * envelope
    
    # Normalize to 16-bit integer range
    audio_data = (audio_data * 32767).astype(np.int16)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Write to WAV
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
    
    print(f"Generated servo sound: {filename}")

if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "assets", "sounds", "servo.wav")
    try:
        generate_servo_sound(output_path, duration=0.3, start_freq=150, end_freq=300)
    except Exception as e:
        # Fallback if specific dirs don't exist, try relative to script
        print(f"Error writing to {output_path}: {e}")
        # Try current directory as fallback or print instructions
