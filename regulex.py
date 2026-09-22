import argparse
import re

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def highlight_matches(text: str, pattern: str) -> Text:
    """Highlights all regex matches in the text in color."""
    highlighted = Text()
    last_end = 0

    for match in re.finditer(pattern, text):
        start, end = match.span()
        # Add the text before the match (normal)
        highlighted.append(text[last_end:start], style="white")
        # Add the match (colored)
        highlighted.append(text[start:end], style="bold red")
        last_end = end

    # Add the remaining text
    highlighted.append(text[last_end:], style="white")
    return highlighted


def explain_pattern(pattern: str) -> str:
    """Attempts to explain the regex (simple version)."""
    explanations = {
        r"\d": "A digit (0-9)",
        r"\w": "A letter, digit, or underscore",
        r"\s": "A whitespace character (space, tab, newline)",
        r"\.": "Any character (except newline)",
        r"\*": "0 or more occurrences of the previous character",
        r"\+": "1 or more occurrences of the previous character",
        r"\?": "0 or 1 occurrence of the previous character",
        r"{n}": "Exactly {n} occurrences of the previous character",
        r"{n,m}": "Between {n} and {m} occurrences of the previous character",
        r"[abc]": "A character from the set (a, b, or c)",
        r"[^abc]": "A character not in the set (a, b, c)",
        r"(?:...)": "Non-capturing group",
        r"^": "Start of string",
        r"$": "End of string",
    }

    explanation = []
    for part, desc in explanations.items():
        if part in pattern:
            explanation.append(f"- `{part}`: {desc}")

    return "\n".join(explanation) if explanation else "No explanation available."


def check_regex(pattern: str, text: str) -> None:
    """Tests the regex and displays results."""
    console.print(Panel(f"[bold]Pattern:[/bold] {pattern}", title="Regex Tester", border_style="blue"))
    console.print(Panel(f"[bold]Text:[/bold] {text}", border_style="green"))

    try:
        matches = list(re.finditer(pattern, text))
        if not matches:
            console.print("[yellow]No matches found.[/yellow]")
        else:
            console.print(f"[bold green]Found Matches ({len(matches)}):[/bold green]")
            for i, match in enumerate(matches, 1):
                console.print(f"  {i}. Position {match.span()}: '{match.group()}'")

            console.print("\n[bold]Highlighted Text:[/bold]")
            console.print(highlight_matches(text, pattern))

        console.print("\n[bold]Pattern Explanation:[/bold]")
        console.print(explain_pattern(pattern))

    except re.error as e:
        console.print(f"[red]Regex Error:[/red] {e}")


def interactive_mode() -> None:
    """Interactive mode for live testing."""
    console.print(Panel("[bold]Interactive Regex Tester[/bold]\n"
                        "Type 'exit' or 'quit' to quit or 'help' for examples.",
                        title="Welcome", border_style="cyan"))

    while True:
        pattern = console.input("[bold]Regex-Pattern:[/bold] ")
        if pattern.lower() in ("exit", "quit"):
            break
        if pattern.lower() == "help":
            console.print(Panel(
                r"[bold]Regex Examples:[/bold]"+"\n"
                r"- \d{3}: three digits (e.g., 123)"+"\n"
                r"- [A-Za-z]+: one or more letters"+"\n"
                r"- \w{4}: four alphanumeric characters"+"\n"
                r"- ^\d+: string starts with one or more digits"+"\n"
                r"- \d{2}-\d{2}-\d{4}: date in format DD-MM-YYYY",
                title="Help", border_style="yellow"
            ))
            continue

        text = console.input("[bold]Text:[/bold] ")
        if text.lower() in ("exit", "quit"):
            break

        check_regex(pattern, text)
        console.print("\n" + "-" * 50 + "\n")


def main():
    print_banner()
    parser = argparse.ArgumentParser(
        description="Test regular expressions in the terminal.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=r"""
Examples:
  python regex.py -p "\d{3}" -t "ABC123XYZ"
  python regex.py --interactive
        """
    )
    parser.add_argument("-p", "--pattern", type=str, help="Regex pattern")
    parser.add_argument("-t", "--text", type=str, help="Text to test")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive mode")

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.pattern and args.text:
        check_regex(args.pattern, args.text)
    else:
        parser.print_help()


def print_banner():
    print(
        r"""
        ╔═══════════════════════════════╗
        ║                               ║
        ║      ███████████████████      ║
        ║      █     █     █     █      ║
        ║      █     █     ███████      ║
        ║      █     █     █     █      ║
        ║                               ║
        ╚═══════════════════════════════╝
        r e g u l e x
        """
    )


if __name__ == "__main__":
    main()
