# AFX Driver Checker

A lightweight Windows driver inspection tool that helps you understand what device drivers are installed on your PC.

> **Built for safety:** AFX Driver Checker does not download or install random drivers. It inspects the drivers already registered by Windows and gives you safe shortcuts to Device Manager and Windows Update.

## Features

- Scan installed Plug-and-Play drivers
- Show:
  - Device name
  - Driver version
  - Driver provider
  - Driver date
  - Driver status
  - Device class
- Search drivers instantly
- Filter by:
  - All
  - OK
  - Potentially Old
  - Missing / Problem
- Simple driver-age heuristic
- Export results to CSV
- Export results to JSON
- Open Windows Device Manager
- Open Windows Update
- Clean desktop UI
- Diagnostic CLI mode
- GitHub Actions tests

## Important

A driver being old does **not automatically mean it is unsafe or needs updating**.

Some hardware vendors intentionally keep stable older drivers. Always prefer drivers from:

1. Windows Update
2. Your laptop/PC manufacturer's official support page
3. Your GPU/chipset manufacturer's official website

Avoid random third-party driver download websites.

## Requirements

- Windows 10 or Windows 11
- Python 3.10+
- PowerShell / Windows Management Instrumentation available

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

Or double-click:

```text
scripts/run_windows.bat
```

## Diagnostic mode

```bash
python main.py --diagnose
```

## Repository structure

```text
AFX-Driver-Checker/
├── README.md
├── main.py
├── requirements.txt
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── ui.py
│   ├── scanner.py
│   ├── analyzer.py
│   ├── exporter.py
│   └── windows_tools.py
├── config/
│   └── settings.json
├── docs/
│   └── DRIVER_SAFETY_GUIDE.md
├── scripts/
│   └── run_windows.bat
├── tests/
│   ├── test_analyzer.py
│   └── test_exporter.py
└── .github/
    └── workflows/
        └── python-tests.yml
```

## What "Potentially Old" means

AFX Driver Checker uses a simple date-based heuristic. By default, drivers older than about three years may be highlighted for review.

This is only a **review signal**, not a recommendation to replace the driver.

## Future ideas

- Hardware vendor detection
- Driver backup
- Restore-point shortcut
- Microsoft Update Catalog lookup
- GPU / chipset special detection
- Driver change history
- Signed/unsigned driver information
- Dashboard charts

## License

MIT

lINK: afxapichecker.netlify.app
