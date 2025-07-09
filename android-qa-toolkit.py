import subprocess
import os
import datetime

def run_adb_command(command):
    try:
        result = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8').strip()
        return result
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed: {' '.join(command)}")
        print(e.output.decode('utf-8'))
        return None

def get_connected_device_serial():
    try:
        result = subprocess.check_output(["adb", "devices"]).decode("utf-8").strip()
        lines = result.split("\n")[1:]  # Skip the header line
        for line in lines:
            if "\tdevice" in line:
                return line.split("\t")[0]
        return None
    except subprocess.CalledProcessError as e:
        print("[ERROR] Failed to list adb devices.")
        print(e.output.decode('utf-8'))
        return None

def extract_version_from_dumpsys(serial_number, package_name):
    output = run_adb_command(["adb", "-s", serial_number, "shell", "dumpsys", "package", package_name])
    if output:
        for line in output.splitlines():
            if "versionName" in line:
                return line.strip()
    return "N/A"

def get_device_info(serial_number):
    device_info = {
        "Device Model": run_adb_command(["adb", "-s", serial_number, "shell", "getprop", "ro.product.model"]),
        "Build Version": run_adb_command(["adb", "-s", serial_number, "shell", "getprop", "ro.revision"]),
        "Serial Number": run_adb_command(["adb", "-s", serial_number, "shell", "getprop", "ro.serialno"]),
        "ROM Build ID": run_adb_command(["adb", "-s", serial_number, "shell", "getprop", "ro.bootimage.build.id"]),
        "TalkBack Version": extract_version_from_dumpsys(serial_number, "com.google.android.marvin.talkback"),
        "Switch Access Version": extract_version_from_dumpsys(serial_number, "com.google.android.accessibility.switchaccess")
    }
    return device_info

def record_screen(serial_number, duration, quality, output_path):
    resolution_map = {
        "low": "480x800",
        "medium": "720x1280",
        "high": "1080x1920"
    }
    bitrate_map = {
        "low": "1000000",
        "medium": "2500000",
        "high": "5000000"
    }
    resolution = resolution_map.get(quality, "720x1280")
    bitrate = bitrate_map.get(quality, "2500000")

    os.makedirs(output_path, exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_path, f"record_{timestamp}.mp4")

    print(f"[INFO] Recording screen ({duration}s, {quality})...")
    command = ["adb", "-s", serial_number, "shell", "screenrecord", f"--time-limit", str(duration), f"--bit-rate", bitrate, f"--size", resolution, f"/sdcard/tmp_record.mp4"]
    subprocess.run(command)

    run_adb_command(["adb", "-s", serial_number, "pull", "/sdcard/tmp_record.mp4", output_file])
    run_adb_command(["adb", "-s", serial_number, "shell", "rm", "/sdcard/tmp_record.mp4"])
    print(f"[INFO] Video saved to {output_file}")

def generate_bugreport(serial_number, output_path):
    os.makedirs(output_path, exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = os.path.join(output_path, f"bugreport_{timestamp}.zip")
    print("[INFO] Generating bugreport...")
    command = ["adb", "-s", serial_number, "bugreport", report_file]
    subprocess.run(command)
    print(f"[INFO] Bugreport saved to {report_file}")

def write_device_info_report(device_info, output_path, regression=None, fr_status=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_lines = ["Device Info Report", "-------------------"]
    for key, value in device_info.items():
        report_lines.append(f"{key}: {value}")
    report_lines.append("")
    report_lines.append(f"Timestamp: {timestamp}")

    # Default regression info
    if regression is None:
        regression = "No, No issue observed in other app/build version so far"
    report_lines.append(f"Regression: {regression}")

    # Default F/R info
    if fr_status is None:
        fr_status = "5/5"
    report_lines.append(f"F/R: {fr_status}")

    os.makedirs(output_path, exist_ok=True)
    report_file = os.path.join(output_path, f"device_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(report_file, "w") as f:
        f.write("\n".join(report_lines))

    print(f"[INFO] Report written to {report_file}")

def prompt_user_choices():
    print("=== A11y QA Toolkit ===")
    record = input("Enter recording duration in seconds (0, 10, 30, 60, 90): ").strip()
    try:
        record = int(record)
    except ValueError:
        record = 0
    
    if record not in [0, 10, 30, 60, 90]:
        print("[WARN] Invalid record duration. Defaulting to 0 (no recording).")
        record = 0

    quality = input("Choose quality (low, medium, high): ").strip().lower()
    if quality not in ["low", "medium", "high"]:
        print("[WARN] Invalid quality. Defaulting to 'medium'.")
        quality = "medium"

    bugreport_input = input("Generate bugreport? (Y/N): ").strip().lower()
    bugreport = bugreport_input == 'y'

    return record, quality, bugreport

def main():
    record, quality, bugreport = prompt_user_choices()

    serial_number = get_connected_device_serial()
    if not serial_number:
        print("[ERROR] No connected device detected.")
        return

    timestamp_folder = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join("output", timestamp_folder)

    device_info = get_device_info(serial_number)

    if record > 0:
        record_screen(serial_number, record, quality, output_path)

    if bugreport:
        generate_bugreport(serial_number, output_path)

    write_device_info_report(device_info, output_path)

if __name__ == "__main__":
    main()
