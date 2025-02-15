# pragma version ^0.4.0

# Event for tracking donations
event Donation:
    sender: address
    amount: uint256

# Storage for tracking donors
donations: public(HashMap[address, uint256])
owner: public(address)
recipient: public(address)
name: public(String[24])

@deploy
def __init__(owner: address, recipient: address, name: String[24]):
    self.owner = owner

    # NOTE: Recipient cannot be changed for a cause.
    self.recipient = recipient

    self.name = name

@external
@payable
def donate():
    """
    Function to receive donations and track the sender.
    """
    self.donations[msg.sender] += msg.value
    log Donation(msg.sender, msg.value)

@external
def withdraw(amount: uint256):
    assert msg.sender == self.owner, "!authorized"
    assert amount <= self.balance, "Insufficient balance"
    send(self.recipient, amount)

@external
def change_owner(new_owner: address):
    assert msg.sender == self.owner, "!authorized"
    self.owner = new_owner

@external
@payable
def __default__():
    log Donation(msg.sender, msg.value)
