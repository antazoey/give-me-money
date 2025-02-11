import click
from ape.cli import account_option, ConnectedProviderCommand
from ape import project


@click.command(cls=ConnectedProviderCommand)
@account_option()
def cli(account):
    """
    Deploy the FundMe script.
    """
    contract = project.FundMe
    click.echo(f"Deploying '{contract.name}' using '{account.alias}'...'")
