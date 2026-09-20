from datetime import date, datetime

OLD_DRIVER_YEARS = 3

def _parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value[:10], "%Y-%m-%d").date()
    except Exception:
        return None

def driver_age_years(driver_date, today=None):
    parsed = _parse_date(driver_date)
    if not parsed:
        return None
    today = today or date.today()
    return max(0.0, (today - parsed).days / 365.25)

def analyze_driver(driver, today=None):
    device_name = str(driver.get("device_name", "")).strip()
    version = str(driver.get("version", "")).strip()
    status = str(driver.get("status", "OK")).strip().upper()
    signed = driver.get("signed")
    age = driver_age_years(driver.get("driver_date", ""), today=today)

    reasons = []
    health = "OK"

    if not device_name or not version or status not in {"OK", ""}:
        health = "Problem"
        reasons.append("Missing driver information or Windows reported a problem.")

    if signed is False:
        health = "Problem"
        reasons.append("Driver is reported as unsigned.")

    if health != "Problem" and age is not None and age >= OLD_DRIVER_YEARS:
        health = "Potentially Old"
        reasons.append(f"Driver is about {age:.1f} years old.")

    if not reasons:
        reasons.append("No obvious issue detected from available Windows driver metadata.")

    return {
        "health": health,
        "age_years": age,
        "reason": " ".join(reasons),
    }
