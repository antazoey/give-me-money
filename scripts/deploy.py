import click
from ape import project
from ape.cli import ConnectedProviderCommand, account_option


@click.command(cls=ConnectedProviderCommand)
@account_option()
def cli(account):
    """
    Deploy the FundMe script.
    """
    contract = project.FundMe
    click.echo(f"Deploying '{contract.name}' using '{account.alias}'...'")
