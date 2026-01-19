import time
import numpy as np
from smbus2 import SMBus


class MAX30102:
    ADDRESS = 0x57

    def __init__(self, bus=1):
        self.bus = SMBus(bus)
        self._init_sensor()

    def _init_sensor(self):
        # Reset
        self.bus.write_byte_data(self.ADDRESS, 0x09, 0x40)
        time.sleep(0.1)

        # FIFO config
        self.bus.write_byte_data(self.ADDRESS, 0x08, 0x0F)

        # SpO2 mode (RED + IR)
        self.bus.write_byte_data(self.ADDRESS, 0x09, 0x03)

        # SPO2 config: 100Hz, 411us
        self.bus.write_byte_data(self.ADDRESS, 0x0A, 0x27)

        # LED currents (moderate)
        self.bus.write_byte_data(self.ADDRESS, 0x0C, 0x24)  # RED
        self.bus.write_byte_data(self.ADDRESS, 0x0D, 0x24)  # IR

    def read_fifo(self):
        data = self.bus.read_i2c_block_data(self.ADDRESS, 0x07, 6)

        red = ((data[0] << 16) | (data[1] << 8) | data[2]) & 0x3FFFF
        ir  = ((data[3] << 16) | (data[4] << 8) | data[5]) & 0x3FFFF

        return red, ir

    def shutdown(self):
        # Turn OFF LEDs
        self.bus.write_byte_data(self.ADDRESS, 0x0C, 0x00)
        self.bus.write_byte_data(self.ADDRESS, 0x0D, 0x00)
        self.bus.close()


# ----------------------------------------------------

def measure_vitals(mode="heart", duration=10):
    """
    mode: "heart", "spo2", "both"
    returns: BPM, SpO2, or dict
    """

    sensor = MAX30102()
    start = time.time()

    red_vals, ir_vals, timestamps = [], [], []

    print("🫀 Place finger on sensor... Hold still.")

    while time.time() - start < duration:
        red, ir = sensor.read_fifo()

        # Finger detection threshold
        if ir > 5000:
            red_vals.append(red)
            ir_vals.append(ir)
            timestamps.append(time.time())

        time.sleep(0.02)

    sensor.shutdown()  # 🔥 TURN LED OFF

    if len(ir_vals) < 200:
        print("❌ Weak signal / finger not steady")
        return None

    # ---------------- BPM ----------------
    ir = np.array(ir_vals)
    ir = np.convolve(ir, np.ones(7) / 7, mode="same")  # smooth

    mean_ir = np.mean(ir)
    peaks = []

    MIN_PEAK_DISTANCE = 0.4  # seconds (max ~150 BPM)

    for i in range(1, len(ir) - 1):
        if ir[i] > mean_ir and ir[i] > ir[i - 1] and ir[i] > ir[i + 1]:
            if not peaks or (timestamps[i] - peaks[-1]) > MIN_PEAK_DISTANCE:
                peaks.append(timestamps[i])

    bpm = None
    if len(peaks) >= 5:
        intervals = np.diff(peaks)
        bpm = int(60 / np.median(intervals))

        # Reject nonsense
        if bpm < 40 or bpm > 160:
            bpm = None

    # ---------------- SpO₂ ----------------
    red = np.array(red_vals)
    ir = np.array(ir_vals)

    red_dc = np.mean(red)
    ir_dc = np.mean(ir)

    red_ac = np.std(red)
    ir_ac = np.std(ir)

    spo2 = None
    if ir_ac > 0 and red_ac > 0:
        R = (red_ac / red_dc) / (ir_ac / ir_dc)
        spo2 = int(110 - 25 * R)
        spo2 = max(90, min(100, spo2))

    # ---------------- RETURN ----------------
    if mode == "heart":
        return bpm
    elif mode == "spo2":
        return spo2
    else:
        return {"bpm": bpm, "spo2": spo2}


# ----------------------------------------------------

if __name__ == "__main__":
    vitals = measure_vitals("both")
    print("❤️ Heart Rate:", vitals["bpm"])
    print("🩸 SpO₂:", vitals["spo2"])