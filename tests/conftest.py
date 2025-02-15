import pytest


@pytest.fixture(scope="session")
def owner(accounts):
    return accounts[0]


@pytest.fixture(scope="session")
def kind_soul(accounts):
    return accounts[1]


@pytest.fixture(scope="session")
def sneaky_mf(accounts):
    return accounts[2]


@pytest.fixture(scope="session")
def cause(owner, project):
    return owner.deploy(project.Cause, owner, owner, "Antazoey")


@pytest.fixture(scope="session")
def kind_souls_cause(owner, project, kind_soul):
    return owner.deploy(project.Cause, owner, kind_soul, "Kind Soul")
