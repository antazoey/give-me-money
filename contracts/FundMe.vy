# pragma version ^0.4.0

# Event for tracking donations
event Donation:
    sender: address
    amount: uint256

# Storage for tracking donors
donations: public(HashMap[address, uint256])
total_donations: public(uint256)
owner: public(address)

@deploy
def __init__():
    self.owner = msg.sender

@external
@payable
def donate(anon: bool = False):
    """
    Function to receive donations and track the sender.
    """
    if not anon:
        self.donations[msg.sender] += msg.value

    self.total_donations += msg.value
    log Donation(msg.sender, msg.value)


@external
def withdraw(amount: uint256):
    assert msg.sender == self.owner, "!authorized"
    assert amount <= self.balance, "Insufficient balance"
    send(msg.sender, amount)
