from ape import convert, reverts


def test_owner(cause, owner, kind_souls_cause):
    assert cause.owner() == owner
    assert kind_souls_cause.owner() == owner


def test_owner_different_than_sender(project, owner, kind_soul):
    # The owner deploys a cause-account for someone else.
    cause = project.CauseAccount.deploy(kind_soul, kind_soul, "DifferentOwner", sender=owner)
    assert cause.owner() == kind_soul


def test_recipient(cause, owner, project, kind_soul):
    assert cause.recipient() == owner

    # Show it can be different.
    new_cause = project.CauseAccount.deploy(owner, kind_soul, "Kind Soul", sender=owner)
    assert new_cause.recipient() == kind_soul


def test_donate(cause, kind_soul):
    tx = cause.donate(sender=kind_soul, value="100 ETH")
    assert not tx.failed

    # Ensure donation appears in total donations.
    expected = convert("100 ETH", int)
    actual = cause.balance
    assert actual == expected

    # Ensure the donation is present.
    donation = cause.donations(kind_soul)
    assert donation == convert("100 ETH", int)


def test_donate_anonymously(cause, kind_soul):
    tx = cause(sender=kind_soul, value="100 ETH")
    assert not tx.failed

    # Ensure donation appears in total donations.
    expected = convert("100 ETH", int)
    actual = cause.balance
    assert actual == expected

    # Ensure the donation is present.
    donation = cause.donations(kind_soul)
    assert donation == 0  # Was donated anonymously.


def test_withdraw_not_owner(cause, sneaky_mf):
    with reverts("!authorized"):
        cause.withdraw("100 ETH", sender=sneaky_mf)


def test_withdraw_insufficient_balance(cause, owner):
    with reverts("Insufficient balance"):
        cause.withdraw("100 ETH", sender=owner)


def test_withdraw(cause, owner, kind_soul, kind_souls_cause):
    HUNDRED_WEI = convert("100 ETH", int)
    my_starting_balance = owner.balance
    cause.donate(sender=kind_soul, value=HUNDRED_WEI)
    contract_starting_balance = cause.balance

    tx = cause.withdraw(HUNDRED_WEI, sender=owner)
    assert not tx.failed

    my_expected_balance = my_starting_balance + HUNDRED_WEI - tx.total_fees_paid
    contract_expected_balance = contract_starting_balance - HUNDRED_WEI
    assert owner.balance == my_expected_balance
    assert cause.balance == contract_expected_balance

    # Show it uses the given deposit address.
    kind_souls_cause.donate(value=HUNDRED_WEI, sender=kind_soul)
    kind_souls_balance = kind_soul.balance
    kind_souls_cause.withdraw(HUNDRED_WEI, sender=owner)
    assert kind_soul.balance == kind_souls_balance + HUNDRED_WEI


def test_change_owner(owner, kind_souls_cause, kind_soul):
    kind_souls_cause.change_owner(kind_soul, sender=owner)
    assert kind_souls_cause.owner() == kind_soul
