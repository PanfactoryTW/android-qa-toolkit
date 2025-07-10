import os
import datetime
import time

# Simulated output path
timestamp_folder = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = os.path.join("output_demo", timestamp_folder)
os.makedirs(output_path, exist_ok=True)

print("[INFO] Connected device detected: SAMPLE_SERIAL_1234")
time.sleep(1.2)

print("[INFO] Starting screen recording (30s, high)...")
time.sleep(2.0)

print("[INFO] Recording complete. Video saved to:")
print(f"{os.path.join(output_path, 'record_SAMPLE_20250709_1522.mp4')}")
time.sleep(1.5)

print("[INFO] Generating bugreport...")
time.sleep(2.0)

print(f"[INFO] Bugreport saved to {os.path.join(output_path, 'bugreport_SAMPLE_20250709_1522.zip')}")
time.sleep(1.2)

print("[INFO] Writing device info report...")
time.sleep(1.0)

report_lines = [
    "Device Info Report",
    "-------------------",
    "Device Model: SAMPLE_DEVICE",
    "Build Version: 12345",
    "Serial Number: SAMPLE_SERIAL_1234",
    "ROM Build ID: SAMPLE_ROM_BUILD",
    "TalkBack Version: versionName=999.9.9",
    "Switch Access Version: versionName=888.8.8",
    "",
    f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    "Regression: No, No issue observed in other app/build version so far",
    "F/R: 5/5"
]

report_file = os.path.join(output_path, "device_report_SAMPLE.txt")
with open(report_file, "w") as f:
    f.write("\n".join(report_lines))

time.sleep(0.8)
print(f"[INFO] Report written to {report_file}")
time.sleep(0.6)
print("[INFO] Demo run complete. All sample files generated.")
