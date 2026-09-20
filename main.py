import argparse
from app.scanner import scan_drivers
from app.analyzer import analyze_driver

def diagnose():
    print("AFX Driver Checker - Diagnostics")
    print("=" * 34)
    drivers = scan_drivers()
    print(f"Detected drivers: {len(drivers)}")
    counts = {"OK": 0, "Potentially Old": 0, "Problem": 0}
    for driver in drivers:
        status = analyze_driver(driver)["health"]
        counts[status] = counts.get(status, 0) + 1
    for key, value in counts.items():
        print(f"{key}: {value}")

def main():
    parser = argparse.ArgumentParser(description="AFX Driver Checker")
    parser.add_argument("--diagnose", action="store_true", help="Run driver diagnostics")
    args = parser.parse_args()

    if args.diagnose:
        diagnose()
        return

    from app.ui import DriverCheckerApp
    DriverCheckerApp().run()

if __name__ == "__main__":
    main()
