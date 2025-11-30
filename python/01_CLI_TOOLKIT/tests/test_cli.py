from click.testing import CliRunner
from hello_cli.cli import cli

def test_hello_command():
    runner = CliRunner()
    result = runner.invoke(cli, ["hello", "Arya"])
    assert result.exit_code == 0
    assert "Hello, Arya!" in result.output