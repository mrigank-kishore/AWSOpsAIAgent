from __future__ import annotations

import json
from pathlib import Path

import typer

from aiops_agent.common.config import get_settings
from aiops_agent.common.logging import configure_logging, get_logger
from aiops_agent.orchestration.workflow import build_workflow_summary

app = typer.Typer(help="AWS-first AIOps agent CLI")


@app.callback()
def main() -> None:
    """Initialize CLI context."""
    settings = get_settings()
    configure_logging(settings.log_level)


@app.command()
def doctor() -> None:
    """Show the current project configuration."""
    settings = get_settings()
    typer.echo(json.dumps(settings.model_dump(), indent=2))


@app.command()
def workflow() -> None:
    """Print the intended incident workflow."""
    summary = build_workflow_summary()
    typer.echo(json.dumps(summary, indent=2))


@app.command()
def seed_check() -> None:
    """Verify seed data path wiring."""
    settings = get_settings()
    seed_path = Path(settings.seed_data_path)
    logger = get_logger(__name__)
    logger.info("seed_check", seed_path=str(seed_path), exists=seed_path.exists())
    typer.echo(f"Seed data path: {seed_path} | exists={seed_path.exists()}")


if __name__ == "__main__":
    app()
