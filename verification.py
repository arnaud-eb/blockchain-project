from hash_util import hash_string_256, hash_block


class Verification:

    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        guess = (str([tx.to_ordered_dict() for tx in transactions]
                     ) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_string_256(guess)
        return guess_hash[:2] == '00'

    @staticmethod
    def verify_transaction(transaction, get_balance):
        return get_balance() >= transaction.amount

    @classmethod
    def verify_transactions(cls, get_balance, open_transactions):
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transactions])

    @classmethod
    def verify_blockchain(cls, blockchain):
        for block_index, block in enumerate(blockchain):
            if block_index == 0:
                continue
            if hash_block(blockchain[block_index-1]) != block.previous_hash:
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print('Proof of work is invalid')
                return False
        return True