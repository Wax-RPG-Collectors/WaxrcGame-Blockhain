import click
import os
import signal
import sys
from main import run_daemon, main

@click.group()
def cli():
    pass

@cli.command()
def start():
    """Start the blockchain node."""
    click.echo("Starting the blockchain node...")
    run_daemon()

@cli.command()
def stop():
    """Stop the blockchain node."""
    click.echo("Stopping the blockchain node...")
    with open('node.pid', 'r') as f:
        pid = int(f.read().strip())
    os.kill(pid, signal.SIGTERM)
    os.remove('node.pid')
    click.echo("Blockchain node stopped.")

@cli.command()
def status():
    """Check the status of the blockchain node."""
    try:
        with open('node.pid', 'r') as f:
            pid = int(f.read().strip())
        os.kill(pid, 0)
        click.echo("Blockchain node is running.")
    except (OSError, FileNotFoundError):
        click.echo("Blockchain node is not running.")

if __name__ == "__main__":
    cli()