from typing import Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.theme import Theme

    _RICH_AVAILABLE = True
except Exception:
    _RICH_AVAILABLE = False


def _get_console() -> Optional[Console]:  # type: ignore
    if not _RICH_AVAILABLE:
        return None
    theme = Theme(  # type: ignore
        {
            "markdown.h1": "bold red",
            "markdown.h2": "bold red",
            "markdown.h3": "bold red",
            "markdown.h4": "bold red",
            "markdown.h5": "red",
            "markdown.h6": "red",
            "markdown.code_block": "dim",
            "markdown.link": "bold cyan",
            "markdown.list_item_prefix": "red",
            "table.border": "red",
        }
    )
    return Console(theme=theme)  # type: ignore


def fix_markdown_hierarchy(markdown_text: str) -> str:
    """
    Ensure markdown starts with h1 and has proper hierarchy for PDF generation.
    """
    lines = markdown_text.split("\n")

    # Check if first heading is h1
    first_heading_found = False
    for i, line in enumerate(lines):
        if line.strip().startswith("#"):
            # Count the number of '#' characters
            heading_level = len(line) - len(line.lstrip("#"))

            if not first_heading_found:
                # First heading must be h1
                if heading_level > 1:
                    # Convert first heading to h1
                    lines[i] = "# " + line.lstrip("#").strip()
                first_heading_found = True
            break

    # If no heading found at all, add a title
    if not first_heading_found:
        lines.insert(0, "# Research Report\n")

    return "\n".join(lines)


def render_markdown(md_text: str, title: str = "Research Report"):
    """Render Markdown to the terminal with a red panel.

    Falls back to plain print if Rich is not available.
    """
    console = _get_console()
    if console is None:
        print("\n" + title + "\n")
        print(md_text)
        return

    md = Markdown(md_text, code_theme="monokai")  # type: ignore
    panel = Panel(  # type: ignore
        md,
        title=title,
        border_style="orange1",
        expand=True,
        padding=(1, 2),
    )
    console.print(panel)
