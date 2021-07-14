import functools
import hashlib as hl
from collections import OrderedDict
import json
import requests

from utility.hash_util import hash_block
from utility.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet

MINING_REWARD = 10


class Blockchain:
    def __init__(self, public_key, node_id):
        genesis_block = Block('', 0, [], 100)
        self.chain = [genesis_block]
        self.__open_transactions = []
        self.__peer_nodes = set()
        self.public_key = public_key
        self.node_id = node_id
        self.resolve_conflicts = False
        self.load_data()

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        try:
            with open(f'blockchain-{self.node_id}.txt', mode='r') as f:
                content = f.readlines()
                json_blockchain = json.loads(content[0][:-1])
                self.chain = [Block(
                    block['previous_hash'],
                    block['index'],
                    [Transaction(
                        tx['sender'],
                        tx['recipient'],
                        tx['signature'],
                        tx['amount'])
                        for tx in block['transactions']],
                    block['proof'])
                    for block in json_blockchain]
                json_open_transactions = json.loads(content[1][:-1])
                self.__open_transactions = [Transaction(
                    tx['sender'],
                    tx['recipient'],
                    tx['signature'],
                    tx['amount'])
                    for tx in json_open_transactions]
                self.__peer_nodes = set(json.loads(content[2]))
        except (IOError, IndexError):
            pass

    def save_data(self):
        try:
            with open(f'blockchain-{self.node_id}.txt', mode='w') as f:
                saveable_chain = [block.__dict__ for block in [Block(
                    block.previous_hash,
                    block.index,
                    [tx.__dict__ for tx in block.transactions],
                    block.proof)
                    for block in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [
                    transaction.__dict__
                    for transaction in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))
            return True
        except IOError:
            print('Saving failed!')
            return False

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(
                self.__open_transactions,
                last_hash,
                proof):
            proof += 1
        return proof

    def get_balance(self, sender=None):
        if sender is None:
            if self.public_key is None:
                return None
            participant = self.public_key
        else:
            participant = sender
        tx_sender = [[tx.amount
                     for tx in block.transactions
                     if tx.sender == participant]
                     for block in self.__chain]
        open_tx_sender = [
            tx.amount
            for tx in self.__open_transactions
            if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = functools.reduce(
            lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
            if len(tx_amt) > 0
            else tx_sum + 0, tx_sender, 0)
        tx_recipient = [[tx.amount
                        for tx in block.transactions
                        if tx.recipient == participant]
                        for block in self.__chain]
        amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(
            tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
        return amount_received-amount_sent

    def add_transaction(
            self,
            recipient,
            sender,
            signature,
            amount=1.0,
            is_receiving=False):
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            if not is_receiving:
                for node in self.__peer_nodes:
                    url = f"http://{node}/broadcast-transaction"
                    try:
                        response = requests.post(url, json={
                                                 'sender': sender,
                                                 'recipient': recipient,
                                                 'signature': signature,
                                                 'amount': amount})
                        if (response.status_code == 400
                                or response.status_code == 500):
                            print('Transaction declined, needs resolving')
                    except requests.exceptions.ConnectionError:
                        continue
            return True
        return False

    def mine_block(self):
        if self.public_key is None:
            return False
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction(
            'MINING', self.public_key, '', MINING_REWARD)
        copied_transactions = self.__open_transactions[:]
        for index, tx in enumerate(copied_transactions):
            if not Wallet.verify_transaction(tx):
                self.__open_transactions.pop(index)
                self.save_data()
                return False
        copied_transactions.append(reward_transaction)
        block = Block(hashed_block, len(self.__chain),
                      copied_transactions, proof)
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        converted_block = block.__dict__.copy()
        converted_block['transactions'] = [
            tx.__dict__ for tx in converted_block['transactions']]
        for node in self.__peer_nodes:
            url = f"http://{node}/broadcast-block"
            try:
                response = requests.post(url, json={'block': converted_block})
                if response.status_code == 400 or response.status_code == 500:
                    print('Block declined, needs resolving')
                if response.status_code == 409:
                    self.resolve_conflicts = True
            except requests.exceptions.ConnectionError:
                continue
        return True

    def add_block(self, block):
        block['transactions'] = [Transaction(
            tx['sender'],
            tx['recipient'],
            tx['signature'],
            tx['amount']) for tx in block['transactions']]
        block = Block(block['previous_hash'], block['index'],
                      block['transactions'], block['proof'])
        proof_is_valid = Verification.valid_proof(
            block.transactions[:-1], block.previous_hash, block.proof)
        hashes_match = hash_block(self.chain[-1]) == block.previous_hash
        if proof_is_valid and hashes_match:
            self.__chain.append(block)
            stored_transactions = self.__open_transactions[:]
            for itx in block.transactions:
                for opentx in stored_transactions:
                    if (
                            itx.sender == opentx.sender
                            and itx.recipient == opentx.recipient
                            and itx.signature == opentx.signature
                            and itx.amount == opentx.amount
                            ):
                        try:
                            self.__open_transactions.remove(opentx)
                        except ValueError:
                            print('Item was already removed.')
            self.save_data()
            return True
        else:
            return False

    def resolve(self):
        winner_chain = self.chain
        replace = False
        for node in self.__peer_nodes:
            url = f'http://{node}/chain'
            try:
                response = requests.get(url)
                node_chain = response.json()
                node_chain = [Block(
                    block['previous_hash'],
                    block['index'],
                    [Transaction(
                        tx['sender'],
                        tx['recipient'],
                        tx['signature'],
                        tx['amount'])
                        for tx in block['transactions']],
                    block['proof'])
                    for block in node_chain]
                node_chain_length = len(node_chain)
                winner_chain_length = len(winner_chain)
                if (
                        node_chain_length > winner_chain_length
                        and Verification.verify_blockchain(node_chain)
                        ):
                    winner_chain = node_chain
                    replace = True
            except requests.exceptions.ConnectionError:
                continue
        self.resolve_conflicts = False
        self.chain = winner_chain
        if replace:
            self.__open_transactions = []
        self.save_data()
        return replace

    def add_peer_node(self, node):
        '''
        Adds a new node to the peer node set.

        Argument:
            node: The node URL which should be added.
        '''
        self.__peer_nodes.add(node)
        return self.save_data()

    def remove_peer_node(self, node):
        '''
        Removes a node from the peer node set.

        Argument:
            node: The node URL which should be removed.
        '''
        self.__peer_nodes.discard(node)
        if node not in self.__peer_nodes:
            return self.save_data()
        return False

    def print_nodes(self):
        return list(self.__peer_nodes)
