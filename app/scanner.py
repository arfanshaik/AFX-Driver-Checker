import json
import platform
import subprocess
from datetime import datetime

POWERSHELL_SCRIPT = r"""
$ErrorActionPreference = "SilentlyContinue"
Get-CimInstance Win32_PnPSignedDriver |
Select-Object DeviceName, DriverVersion, DriverProviderName, DriverDate, DeviceClass, IsSigned, Manufacturer, InfName |
ConvertTo-Json -Depth 3 -Compress
"""

def _normalize_date(value):
    if not value:
        return ""
    text = str(value).strip()

    if len(text) >= 8 and text[:8].isdigit():
        try:
            dt = datetime.strptime(text[:8], "%Y%m%d")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            pass

    for candidate in (text[:10], text):
        try:
            dt = datetime.fromisoformat(candidate.replace("Z", "+00:00"))
            return dt.date().isoformat()
        except Exception:
            pass

    return text

def scan_drivers():
    if platform.system() != "Windows":
        return []

    command = [
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-Command", POWERSHELL_SCRIPT
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )
    except Exception:
        return []

    if result.returncode != 0 or not result.stdout.strip():
        return []

    try:
        raw = json.loads(result.stdout)
    except json.JSONDecodeError:
        return []

    if isinstance(raw, dict):
        raw = [raw]

    drivers = []
    for item in raw:
        name = (item.get("DeviceName") or "").strip()
        if not name:
            continue
        drivers.append({
            "device_name": name,
            "version": str(item.get("DriverVersion") or ""),
            "provider": str(item.get("DriverProviderName") or ""),
            "driver_date": _normalize_date(item.get("DriverDate")),
            "device_class": str(item.get("DeviceClass") or ""),
            "signed": bool(item.get("IsSigned")) if item.get("IsSigned") is not None else None,
            "manufacturer": str(item.get("Manufacturer") or ""),
            "inf_name": str(item.get("InfName") or ""),
            "status": "OK",
        })

    return drivers
