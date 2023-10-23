from rich import print
from datetime import datetime


__all__ = ["hello_printf", "iso_now"]

def hello_printf():
    print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())

def iso_now():
    current_time = datetime.now()
    print(current_time.isoformat())
    return current_time.isoformat()

