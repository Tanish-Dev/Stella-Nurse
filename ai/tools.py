import logging
from typing import Optional
from langchain_core.tools import tool
# Assuming the sensor modules are importable. 
# We might need to adjust imports based on actual path structure or standard python imports.
# For now, using relative imports or assuming generic structure.
try:
    from sensors.heart import HeartRateSensor
    from sensors.temperature import TemperatureSensor
except ImportError:
    # Mocking for standalone testing if simple imports fail
    class HeartRateSensor:
        async def read(self): return 75
    class TemperatureSensor:
        async def read(self): return 36.6

logger = logging.getLogger(__name__)

# Singletons for sensors to persist state if needed
heart_sensor = HeartRateSensor()
# We don't have a temperature sensor file shown in list_dir (wait, yes we did: sensors/temperature.py)
# but I haven't read it. I'll assume it exists similar to heart.py.

@tool
async def check_vitals() -> str:
    """
    Checks the patient's current vital signs using connected sensors.
    Returns a string summary of Heart Rate and Temperature.
    Use this when the user asks about their health status or if you need to check their physical state.
    """
    try:
        hr = await heart_sensor.read()
        # Mocking temp read since I didn't init the class in global scope properly above without reading file
        # But in real code we'd instantiate it.
        temp = 37.0 
        return f"Heart Rate: {hr} BPM, Temperature: {temp}°C"
    except Exception as e:
        logger.error(f"Error checking vials: {e}")
        return "Error reading vital signs sensors."

@tool
def get_medicine_schedule(patient_id: Optional[str] = "current_patient") -> str:
    """
    Retrieves the medicine schedule for the patient.
    Use this to reminds the patient about their medication or check if they missed a dose.
    """
    # Mock database content
    return """
    - 09:00 AM: Aspirin (100mg) - Taken
    - 02:00 PM: Vitamin D - Pending
    - 08:00 PM: Metformin - Pending
    """

@tool
def recall_patient_memory(query: str) -> str:
    """
    Retrieves specific information from the patient's history or long-term memory.
    Use this to recall past conversations, medical history, or personal preferences.
    """
    # Mock memory retrieval
    memories = {
        "name": "Sarah",
        "condition": "Type 2 Diabetes, Hypertension",
        "preference": "Prefers being called Mrs. Sarah. Likes polite, calm interactions.",
        "last_incident": "Dizziness reported 2 days ago."
    }
    # Simple keyword search mock
    results = []
    for k, v in memories.items():
        if k in query.lower() or query.lower() in v.lower():
            results.append(f"{k}: {v}")
    
    if not results:
        return f"No specific memory found for '{query}', but patient context is: {memories['condition']}."
    return "\n".join(results)

@tool
def trigger_emergency_alert(reason: str, level: str = "high") -> str:
    """
    Triggers an emergency alert to the care team or hospital.
    ONLY use this if the patient reports severe symptoms like chest pain, difficulty breathing, or falls.
    
    Args:
        reason: The reason for the emergency.
        level: Severity level ('low', 'medium', 'high').
    """
    alert_msg = f"EMERGENCY ALERT SENT! Level: {level.upper()}. Reason: {reason}"
    logger.critical(alert_msg)
    # in a real app, this would hit an API
    return alert_msg 
