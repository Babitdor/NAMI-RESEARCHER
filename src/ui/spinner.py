import sys
import threading
import time

# ANSI color definitions
COLORS = {
    "orange": "\033[38;5;208m",
    "green": "\033[32m",
    "red": "\033[31m",
    "dim": "\033[2m",
    "bold": "\033[1m",
    "reset": "\033[0m",
}

FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

# Global lock to prevent multiple spinners from writing simultaneously
_spinner_lock = threading.Lock()


def _get_color(name: str) -> str:
    """Safely retrieve ANSI color code; fall back to orange if unknown."""
    return COLORS.get(name.lower(), COLORS["orange"])


class Spinner:
    """Lightweight terminal spinner with dynamic color support.

    Usage:
        s = Spinner("Running wiki_search…", icon="🦊 Agent | ", color="orange")
        s.start()
        try:
            ... work ...
            s.stop(success=True)
        except Exception:
            s.stop(success=False)
            raise
    """

    def __init__(self, text: str, icon: str = "🦊 Agent | ", color: str = "orange"):
        self.text = text
        self.icon = icon
        self.color = _get_color(color)
        self._stop = threading.Event()
        self._thread = None
        self._idx = 0
        self._start_time = None
        self._stopped = False

    def _render(self):
        while not self._stop.is_set():
            frame = FRAMES[self._idx % len(FRAMES)]
            self._idx += 1

            # Use lock to prevent multiple spinners from writing at once
            with _spinner_lock:
                if not self._stopped:  # Only write if not stopped
                    line = (
                        f"\r{self.color}{self.icon}{COLORS['reset']}"
                        f"{COLORS['bold']}{self.text}{COLORS['reset']} "
                        f"{COLORS['dim']}{frame}{COLORS['reset']}"
                    )
                    try:
                        sys.stdout.write(line)
                        sys.stdout.flush()
                    except UnicodeEncodeError:
                        # Fallback to ASCII-only output
                        ascii_line = f"\r{self.icon}{self.text} [...]"
                        sys.stdout.write(ascii_line.encode('ascii', errors='replace').decode('ascii'))
                        sys.stdout.flush()

            time.sleep(0.08)

    def start(self):
        if self._stopped:
            return  # Don't restart if already stopped

        self._start_time = time.time()
        self._thread = threading.Thread(target=self._render, daemon=True)
        self._thread.start()

    def stop(self, success: bool = True):
        if self._stopped:
            return  # Already stopped

        self._stopped = True
        self._stop.set()

        if self._thread is not None:
            self._thread.join(timeout=0.3)

        elapsed = time.time() - self._start_time if self._start_time else 0.0

        # Use lock for final output
        with _spinner_lock:
            # Clear the entire current line
            sys.stdout.write("\r\033[K")
            sys.stdout.flush()

            status_icon = (
                f"{COLORS['green']}[OK]{COLORS['reset']}"
                if success
                else f"{COLORS['red']}[X]{COLORS['reset']}"
            )
            final_line = (
                f"{self.color}{self.icon}{COLORS['reset']}"
                f"{COLORS['bold']}{self.text}{COLORS['reset']} "
                f"{status_icon} "
                f"{COLORS['dim']}({elapsed:.1f}s){COLORS['reset']}\n"
            )
            try:
                sys.stdout.write(final_line)
                sys.stdout.flush()
            except UnicodeEncodeError:
                # Fallback to ASCII-only output
                status_ascii = "[OK]" if success else "[FAIL]"
                ascii_final = f"\r{self.icon}{self.text} {status_ascii} ({elapsed:.1f}s)\n"
                sys.stdout.write(ascii_final.encode('ascii', errors='replace').decode('ascii'))
                sys.stdout.flush()


def run_with_spinner(label: str, fn, *args, color: str = "orange", **kwargs):
    """Run a callable with a spinner, supporting dynamic color.

    Args:
        label: Text to display next to the spinner.
        fn: Callable to execute.
        color: Color name for the icon (e.g., 'orange', 'green', 'red').
        *args, **kwargs: Passed to `fn`.

    Returns:
        Result of `fn(*args, **kwargs)`.

    Raises:
        Exception: Any exception raised by `fn` is re-raised after stopping the spinner.
    """
    s = Spinner(label, color=color)
    s.start()
    try:
        result = fn(*args, **kwargs)
        s.stop(success=True)
        return result
    except Exception:
        s.stop(success=False)
        raise
