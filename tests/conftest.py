import pytest


@pytest.fixture(scope="session")
def me(accounts):
    return accounts[0]


@pytest.fixture(scope="session")
def kind_soul(accounts):
    return accounts[1]


@pytest.fixture(scope="session")
def sneaky_mf(accounts):
    return accounts[2]


@pytest.fixture(scope="session")
def fundme(me, project):
    return me.deploy(project.FundMe)
