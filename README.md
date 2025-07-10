# Android QA Toolkit

A CLI-based toolkit for Android QA engineers.  
Handles screen recording, bugreport generation, and device info extraction via ADB.

Built for real-world Linux QA workflows. Minimal dependencies. Script-first, no fluff.

---

## Use Case

When you’re tired of manually screen recording, pulling device info, and generating bugreports for every test run — this tool wraps them into one flow.

Used for:
- exploratory or regression sessions
- accessibility testing (TalkBack / Switch Access)
- quick reproducibility reports

---

## Features

- Interactive CLI prompts:
  - Screen recording: duration (0 / 10 / 30 / 60 / 90 seconds)
  - Quality settings: low / medium / high
  - Bugreport: on/off
- Generates device report including:
  - model, ROM build, serial, TalkBack/SwitchAccess version
  - timestamp, F/R, regression status
- Outputs to timestamped folders: `output/YYYYMMDD_HHMMSS/`
- Designed for local use only. Nothing leaves your machine.

---
## Demo Mode

For demonstration or portfolio purposes, a simulated version is available:  
`demo_android_qa_toolkit.py`

This script does not require a real device. It prints simulated `[INFO]` output with realistic delays and generates:

- a fake screen recording filename  
- a fake bugreport path  
- a mock device report `.txt` file with placeholder data

All generated files are stored in:

## Security & Legal Disclaimer

This tool uses ADB to collect data from connected Android devices.  
**It can include sensitive information.** That’s on you.

Examples of potentially sensitive data:
- device serial number
- installed package names (from bugreport)
- screen content during recording

You are responsible for:
- not committing output files to public repos  
- redacting sensitive content before sharing logs  
- knowing what your organization allows

---

## .gitignore recommendation

