# pragma version ^0.4.0

# Event for tracking donations
event Donation:
    sender: address
    amount: uint256

# Storage for tracking donors
donations: public(HashMap[address, uint256])
owner: public(address)
deposit_address: public(address)
cause_name: public(String[24])

@deploy
def __init__(owner: address, deposit_address: address, cause_name: String[24]):
    self.owner = msg.sender
    self.deposit_address = deposit_address
    self.cause_name = cause_name

@external
@payable
def donate():
    """
    Function to receive donations and track the sender.
    """
    self.donations[msg.sender] += msg.value
    log Donation(msg.sender, msg.value)

@external
@nonreentrant
def withdraw(amount: uint256):
    assert msg.sender == self.owner, "!authorized"
    assert amount <= self.balance, "Insufficient balance"
    send(self.deposit_address, amount)

@external
@payable
def __default__():
    log Donation(msg.sender, msg.value)
