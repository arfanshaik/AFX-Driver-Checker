import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import psutil

from app.scanner import scan_drivers
from app.analyzer import analyze_driver
from app.exporter import export_csv, export_json
from app.windows_tools import open_device_manager, open_windows_update

class DriverCheckerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AFX Driver Checker")
        self.root.geometry("1180x700")
        self.root.minsize(900, 600)

        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="All")
        self.status_var = tk.StringVar(value="Ready. Click Scan Drivers.")
        self.drivers = []
        self.analyzed = []

        self._build()

    def _build(self):
        try:
            ttk.Style(self.root).theme_use("clam")
        except Exception:
            pass

        page = ttk.Frame(self.root, padding=16)
        page.pack(fill="both", expand=True)

        title_row = ttk.Frame(page)
        title_row.pack(fill="x")
        ttk.Label(title_row, text="AFX Driver Checker", font=("Segoe UI", 22, "bold")).pack(side="left")
        ttk.Button(title_row, text="Scan Drivers", command=self._scan).pack(side="right")

        ttk.Label(
            page,
            text="Inspect installed Windows drivers safely — no random driver downloads.",
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(4, 6))

        memory = psutil.virtual_memory()
        system_text = (
            f"CPU threads: {psutil.cpu_count(logical=True) or 0}   •   "
            f"RAM: {memory.total / (1024 ** 3):.1f} GB   •   "
            f"Memory usage: {memory.percent:.0f}%"
        )
        ttk.Label(page, text=system_text, font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 12))

        controls = ttk.Frame(page)
        controls.pack(fill="x", pady=(0, 10))

        ttk.Label(controls, text="Search").pack(side="left")
        search = ttk.Entry(controls, textvariable=self.search_var, width=38)
        search.pack(side="left", padx=(6, 12))
        search.bind("<KeyRelease>", lambda _e: self._refresh())

        ttk.Label(controls, text="Filter").pack(side="left")
        filter_box = ttk.Combobox(
            controls,
            textvariable=self.filter_var,
            values=["All", "OK", "Potentially Old", "Problem"],
            state="readonly",
            width=18
        )
        filter_box.pack(side="left", padx=(6, 12))
        filter_box.bind("<<ComboboxSelected>>", lambda _e: self._refresh())

        ttk.Button(controls, text="Export CSV", command=self._export_csv).pack(side="right")
        ttk.Button(controls, text="Export JSON", command=self._export_json).pack(side="right", padx=(0, 8))

        columns = ("device", "version", "provider", "date", "class", "signed", "health")
        self.tree = ttk.Treeview(page, columns=columns, show="headings", height=22)

        headings = {
            "device": "Device",
            "version": "Version",
            "provider": "Provider",
            "date": "Driver Date",
            "class": "Class",
            "signed": "Signed",
            "health": "Health",
        }
        widths = {
            "device": 300,
            "version": 130,
            "provider": 180,
            "date": 105,
            "class": 110,
            "signed": 75,
            "health": 120,
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="w")

        scroll_y = ttk.Scrollbar(page, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(page, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        table_wrap = ttk.Frame(page)
        table_wrap.pack(fill="both", expand=True)
        self.tree.pack(in_=table_wrap, side="left", fill="both", expand=True)
        scroll_y.pack(in_=table_wrap, side="right", fill="y")
        scroll_x.pack(fill="x")

        actions = ttk.Frame(page)
        actions.pack(fill="x", pady=(12, 0))
        ttk.Button(actions, text="Open Device Manager", command=self._device_manager).pack(side="left")
        ttk.Button(actions, text="Open Windows Update", command=self._windows_update).pack(side="left", padx=8)

        ttk.Label(page, textvariable=self.status_var, wraplength=1100).pack(anchor="w", pady=(12, 0))

    def _scan(self):
        self.status_var.set("Scanning Windows drivers...")
        self.root.update_idletasks()

        self.drivers = scan_drivers()
        self.analyzed = []

        for driver in self.drivers:
            info = analyze_driver(driver)
            merged = dict(driver)
            merged.update(info)
            self.analyzed.append(merged)

        self._refresh()

        if not self.drivers:
            self.status_var.set(
                "No drivers were returned. This tool is designed for Windows 10/11 with PowerShell available."
            )
        else:
            counts = {}
            for item in self.analyzed:
                counts[item["health"]] = counts.get(item["health"], 0) + 1
            self.status_var.set(
                f"Scanned {len(self.analyzed)} drivers • "
                f"OK: {counts.get('OK', 0)} • "
                f"Potentially Old: {counts.get('Potentially Old', 0)} • "
                f"Problem: {counts.get('Problem', 0)}"
            )

    def _matches(self, item):
        query = self.search_var.get().strip().lower()
        selected = self.filter_var.get()

        haystack = " ".join([
            str(item.get("device_name", "")),
            str(item.get("version", "")),
            str(item.get("provider", "")),
            str(item.get("device_class", "")),
            str(item.get("manufacturer", "")),
        ]).lower()

        if query and query not in haystack:
            return False
        if selected != "All" and item.get("health") != selected:
            return False
        return True

    def _refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in self.analyzed:
            if not self._matches(item):
                continue
            signed = item.get("signed")
            signed_text = "Yes" if signed is True else "No" if signed is False else "Unknown"
            self.tree.insert("", "end", values=(
                item.get("device_name", ""),
                item.get("version", ""),
                item.get("provider", ""),
                item.get("driver_date", ""),
                item.get("device_class", ""),
                signed_text,
                item.get("health", ""),
            ))

    def _export_rows(self):
        return [item for item in self.analyzed if self._matches(item)]

    def _export_csv(self):
        rows = self._export_rows()
        if not rows:
            messagebox.showinfo("AFX Driver Checker", "Nothing to export.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            initialfile="afx-driver-report.csv"
        )
        if path:
            export_csv(rows, path)
            self.status_var.set(f"CSV exported to {Path(path).name}")

    def _export_json(self):
        rows = self._export_rows()
        if not rows:
            messagebox.showinfo("AFX Driver Checker", "Nothing to export.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
            initialfile="afx-driver-report.json"
        )
        if path:
            export_json(rows, path)
            self.status_var.set(f"JSON exported to {Path(path).name}")

    def _device_manager(self):
        ok, message = open_device_manager()
        self.status_var.set(message)
        if not ok:
            messagebox.showwarning("Device Manager", message)

    def _windows_update(self):
        ok, message = open_windows_update()
        self.status_var.set(message)
        if not ok:
            messagebox.showwarning("Windows Update", message)

    def run(self):
        self.root.mainloop()
