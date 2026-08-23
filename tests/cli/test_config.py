from typer.testing import CliRunner

from weather.cli import app


def test_cli_config_path(runner: CliRunner) -> None:
    result = runner.invoke(app, ["config", "path"])
    assert result.exit_code == 0
    assert "config.toml" in result.stdout
