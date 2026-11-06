"""
display.py
Terminal display helpers using the `rich` library for polished output (O4).
Falls back to plain print if rich is not installed.
Author: Student
"""

try:
    from rich.console import Console
    from rich.table import Table
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

console = Console() if RICH_AVAILABLE else None


def print_header(title: str) -> None:
    """Print a styled section header."""
    if RICH_AVAILABLE:
        console.rule(f"[bold cyan]{title}[/bold cyan]")
    else:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")


def print_success(message: str) -> None:
    if RICH_AVAILABLE:
        rprint(f"[bold green]  ✓ {message}[/bold green]")
    else:
        print(f"  [OK] {message}")


def print_error(message: str) -> None:
    if RICH_AVAILABLE:
        rprint(f"[bold red]  ✗ {message}[/bold red]")
    else:
        print(f"  [ERROR] {message}")


def print_warning(message: str) -> None:
    if RICH_AVAILABLE:
        rprint(f"[bold yellow]  ⚠ {message}[/bold yellow]")
    else:
        print(f"  [WARN] {message}")


def print_table(rows: list, title: str = "") -> None:
    """
    Render a list of dicts as a formatted table.
    Uses rich.Table if available; falls back to plain columns.
    """
    if not rows:
        print_warning("No records found.")
        return

    headers = list(rows[0].keys())

    if RICH_AVAILABLE:
        table = Table(title=title, show_header=True, header_style="bold magenta")
        for h in headers:
            table.add_column(str(h).replace("_", " ").title(), style="cyan")
        for row in rows:
            table.add_row(*[str(v) if v is not None else "—" for v in row.values()])
        console.print(table)
    else:
        # Plain fallback
        col_widths = [
            max(len(str(h)), max((len(str(r.get(h, ""))) for r in rows), default=0))
            for h in headers
        ]
        sep = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
        header_row = "|" + "|".join(
            f" {h:<{w}} " for h, w in zip(headers, col_widths)
        ) + "|"
        if title:
            print(f"\n  {title}")
        print(sep)
        print(header_row)
        print(sep)
        for row in rows:
            data_row = "|" + "|".join(
                f" {str(row.get(h, '')):<{w}} " for h, w in zip(headers, col_widths)
            ) + "|"
            print(data_row)
        print(sep)
        print(f"  {len(rows)} record(s) found.\n")
