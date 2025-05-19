import click
from pathlib import Path
import logging
import sys
from .server import serve

import signal
def signal_handler(sig, frame):
    print(f"Shutting down from signal {sig} received in {frame}", file=sys.stderr)
    sys.exit(0)

@click.command()
@click.option("--repository", "-r", type=Path, help="Git repository path")
@click.option("-v", "--verbose", count=True)
def main(repository: Path | None, verbose: bool) -> None:
    """MCP Git Server - Git functionality for MCP"""
    import asyncio

    # Register signal handlers
    signal.signal(signal.SIGTERM, signal_handler)  # Standard kill command
    signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
    signal.signal(signal.SIGHUP, signal_handler)   # Terminal closes

    logging_level = logging.WARN
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG

    logging.basicConfig(level=logging_level, stream=sys.stderr)
    asyncio.run(serve(repository))

if __name__ == "__main__":
    main()
