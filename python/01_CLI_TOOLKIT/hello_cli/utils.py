import click

def greet_user(name, config):
    greeting = config.get("greeting", "Hello")
    click.echo(f"{greeting}, {name}!")
