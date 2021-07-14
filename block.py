from utility.printable import Printable


class Block(Printable):
    def __init__(self, previous_hash, index, transactions, proof):
        self.previous_hash = previous_hash
        self.index = index
        self.transactions = transactions
        self.proof = proof
