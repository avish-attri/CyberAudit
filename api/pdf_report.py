import os
from datetime import datetime
from pathlib import Path

from fpdf import FPDF

REPORT_FILENAME = "Security-audit-report.pdf"
BRAND_NAME = "CyberAudit"
BRAND_TAGLINE = "Scan · Analyze · Secure"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOGO_CANDIDATES = (
    PROJECT_ROOT / "frontend" / "assets" / "CyberAudit-logo.png",
)
LOGO_HEIGHT_MM = 20


def _resolve_logo_path() -> Path | None:
    for candidate in LOGO_CANDIDATES:
        if candidate.is_file():
            return candidate
    return None

STATUS_ORDER = {"FAIL": 1, "WARNING": 2, "ERROR": 3, "PASS": 4}


def _safe_text(value) -> str:
    if value is None:
        return ""
    text = str(value).replace("\r\n", "\n").replace("\r", "\n")
    return text.encode("latin-1", errors="replace").decode("latin-1")


def _sort_results(results: list) -> list:
    def sort_key(item):
        status = (item.get("status") or "ERROR").upper()
        return STATUS_ORDER.get(status, 99)

    return sorted(results, key=sort_key)


def get_desktop_dir() -> Path:
    home = Path.home()
    for candidate in (
        home / "Desktop",
        home / "OneDrive" / "Desktop",
    ):
        if candidate.is_dir():
            return candidate

    desktop = Path(os.environ.get("USERPROFILE", home)) / "Desktop"
    desktop.mkdir(parents=True, exist_ok=True)
    return desktop


class AuditReportPDF(FPDF):
    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, _safe_text(f"{BRAND_NAME}  |  {BRAND_TAGLINE}"), align="C")
        self.set_text_color(0, 0, 0)


def _draw_brand_header(pdf: FPDF) -> None:
    y0 = pdf.get_y()
    text_x = pdf.l_margin
    logo_bottom = y0

    logo_path = _resolve_logo_path()
    if logo_path:
        try:
            pdf.image(str(logo_path), x=pdf.l_margin, y=y0, h=LOGO_HEIGHT_MM)
            text_x = pdf.l_margin + LOGO_HEIGHT_MM + 5
            logo_bottom = y0 + LOGO_HEIGHT_MM
        except Exception:
            pass

    pdf.set_xy(text_x, y0)
    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 10, _safe_text(BRAND_NAME), ln=True)
    pdf.set_x(text_x)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 7, _safe_text("Security Audit Report"), ln=True)
    pdf.set_x(text_x)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 5, _safe_text(BRAND_TAGLINE), ln=True)

    pdf.set_y(max(logo_bottom, pdf.get_y()) + 6)
    pdf.set_draw_color(56, 189, 248)
    pdf.set_line_width(0.4)
    content_width = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + content_width, pdf.get_y())
    pdf.ln(6)


def _count_statuses(results: list) -> dict:
    counts = {"PASS": 0, "WARNING": 0, "FAIL": 0, "ERROR": 0}
    for item in results:
        status = (item.get("status") or "ERROR").upper()
        if status in counts:
            counts[status] += 1
        else:
            counts["ERROR"] += 1
    return counts


def save_scan_pdf(report: dict) -> Path:
    output_path = get_desktop_dir() / REPORT_FILENAME

    results = _sort_results(report.get("results") or [])
    counts = _count_statuses(results)

    pdf = AuditReportPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    content_width = pdf.w - pdf.l_margin - pdf.r_margin

    _draw_brand_header(pdf)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, _safe_text(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"), ln=True)
    pdf.cell(0, 7, _safe_text(f"Security Score: {report.get('score', 0)}%"), ln=True)
    pdf.cell(0, 7, _safe_text(f"Host IP: {report.get('host_ip', '-')}"), ln=True)
    pdf.cell(0, 7, _safe_text(f"MAC Address: {report.get('host_mac', '-')}"), ln=True)
    duration = report.get("duration_seconds")
    if duration is not None:
        pdf.cell(0, 7, _safe_text(f"Scan Duration: {duration}s"), ln=True)

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Summary", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(
        0,
        7,
        _safe_text(
            f"PASS: {counts['PASS']}  |  WARNING: {counts['WARNING']}  |  "
            f"FAIL: {counts['FAIL']}  |  UNAVAILABLE: {counts['ERROR']}"
        ),
        ln=True,
    )
    pdf.cell(0, 7, _safe_text(f"Total Checks: {len(results)}"), ln=True)

    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "All Checks", ln=True)

    for index, item in enumerate(results, start=1):
        if pdf.get_y() > 250:
            pdf.add_page()

        name = _safe_text(item.get("name") or "Unnamed Check")
        status = _safe_text((item.get("status") or "ERROR").upper())
        risk = _safe_text(item.get("risk") or "Unknown")
        details = _safe_text(item.get("details") or "No details provided")
        recommendation = _safe_text(
            item.get("recommendation") or "No recommendation provided"
        )

        pdf.ln(3)
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(content_width, 6, f"{index}. {name}")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(content_width, 5, f"Status: {status}  |  Risk: {risk}")
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(content_width, 5, f"Details: {details}")
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(content_width, 5, f"Recommendation: {recommendation}")

    pdf.output(str(output_path))
    return output_path
