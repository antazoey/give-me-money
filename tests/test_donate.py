from ape import convert, reverts


def test_owner(fundme, me):
    assert fundme.owner() == me


def test_donate(fundme, kind_soul):
    tx = fundme.donate(sender=kind_soul, value="100 ETH")
    assert not tx.failed

    # Ensure donation appears in total donations.
    expected = convert("100 ETH", int)
    actual = fundme.total_donations()
    assert actual == expected

    # Ensure the donation is present.
    donation = fundme.donations(kind_soul)
    assert donation == convert("100 ETH", int)


def test_donate_anonymously(fundme, kind_soul):
    tx = fundme.donate(True, sender=kind_soul, value="100 ETH")
    assert not tx.failed

    # Ensure donation appears in total donations.
    expected = convert("100 ETH", int)
    actual = fundme.total_donations()
    assert actual == expected

    # Ensure the donation is present.
    donation = fundme.donations(kind_soul)
    assert donation == 0  # Was donated anonymously.


def test_withdraw_not_owner(fundme, sneaky_mf):
    with reverts("!authorized"):
        fundme.withdraw("100 ETH", sender=sneaky_mf)


def test_withdraw_insufficient_balance(fundme, me):
    with reverts("Insufficient balance"):
        fundme.withdraw("100 ETH", sender=me)


def test_withdraw(fundme, me, kind_soul):
    balance_at_start = me.balance
    fundme.donate(sender=kind_soul, value="100 ETH")
    tx = fundme.withdraw("100 ETH", sender=me)
    assert not tx.failed

    expected_balance = balance_at_start + convert("100 ETH", int) - tx.total_fees_paid
    assert me.balance == expected_balance
