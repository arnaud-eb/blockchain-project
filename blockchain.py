import functools
import hashlib as hl
from collections import OrderedDict
import json

from hash_util import hash_string_256, hash_block

MINING_REWARD=10
blockchain = []
open_transactions = []
owner = 'Arnaud'
participants={'Arnaud'}

def load_data():
    global blockchain
    global open_transactions
    try:
        with open('blockchain.txt',mode='r') as f:
            content=f.readlines()
            blockchain=json.loads(content[0][:-1])
            blockchain=[{'previous_hash': block['previous_hash'],'index': block['index'],'proof': block['proof'],'transactions':[OrderedDict([('sender',tx['sender']),('recipient',tx['recipient']),('amount',tx['amount'])]) for tx in block['transactions']]} for block in blockchain]
            open_transactions=json.loads(content[1])
            open_transactions=[OrderedDict([('sender',tx['sender']),('recipient',tx['recipient']),('amount',tx['amount'])]) for tx in open_transactions]
    except (IOError,IndexError):
        genesis_block = {
            'previous_hash': '',
            'index': 0,
            'transactions': [],
            'proof': 100
        }
        blockchain = [genesis_block]
        open_transactions = []

load_data()


def save_data():
    try:
        with open('blockchain.txt',mode='w') as f:
            f.write(json.dumps(blockchain))
            f.write('\n')
            f.write(json.dumps(open_transactions))
    except IOError:
        print('Saving failed!')


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    return guess_hash[:2]=='00'


def proof_of_work():
    last_block=blockchain[-1]
    last_hash=hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions,last_hash,proof):
        proof+=1
    return proof


def get_balance(participant):
    tx_sender=[[tx['amount'] for tx in block['transactions'] if tx['sender']==participant] for block in blockchain]
    open_tx_sender=[tx['amount'] for tx in open_transactions if tx['sender']==participant]
    tx_sender.append(open_tx_sender)
    amount_sent=functools.reduce(lambda tx_sum,tx_amt:tx_sum + sum(tx_amt) if len(tx_amt)>0 else tx_sum + 0,tx_sender,0)
    tx_recipient=[[tx['amount'] for tx in block['transactions'] if tx['recipient']==participant] for block in blockchain]
    amount_received=functools.reduce(lambda tx_sum,tx_amt:tx_sum + sum(tx_amt) if len(tx_amt)>0 else tx_sum + 0,tx_recipient,0)
    return amount_received-amount_sent


def verify_transaction(transaction):
    return get_balance(transaction['sender'])>=transaction['amount']


def add_transaction(recipient, sender=owner, amount=1.0):
    transaction=OrderedDict([('sender',sender),('recipient',recipient),('amount',amount)])
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    reward_transaction=OrderedDict([('sender','MINING'),('recipient',owner),('amount',MINING_REWARD)])
    copied_transactions=open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }
    blockchain.append(block)
    return True


def get_transaction_value():
    new_recipient = input("Enter the recipient of the transaction: ")
    new_amount = float(input("Your transaction amount please: "))
    return new_recipient, new_amount


def get_user_choice():
    print("Please choose")
    print("1: Add a new transaction value")
    print("2: Mine a new block")
    print("3: Output the blockchain blocks")
    print("4: Output participants")
    print("5: Check transaction validity")
    print("h: Manipulate the chain")
    print("q: Quit")
    return input("Your choice: ")


def print_blockchain_elements():
    for block in blockchain:
        print('Outputting Block')
        print(block)
    else:
        print('-'*20)
    print('Blockchain')
    print(blockchain)


def verify_blockchain():
    for block_index,block in enumerate (blockchain):
        if block_index==0:
            continue
        if hash_block(blockchain[block_index-1]) != block['previous_hash']:
            return False
        if not valid_proof(block['transactions'][:-1],block['previous_hash'],block['proof']):
            print('Proof of work is invalid')
            return False
    return True

def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


waiting_for_input = True

while waiting_for_input:
    choice = get_user_choice()
    if choice == '1':
        new_recipient, new_amount = get_transaction_value()
        if add_transaction(new_recipient, amount=new_amount):
            print('Added transaction!')
        else:
            print('Transaction failed!')
        print(open_transactions)
    elif choice == '2':
        if mine_block():
            open_transactions = []
            save_data()
    elif choice == '3':
        print_blockchain_elements()
    elif choice == '4':
        print(participants)
    elif choice == '5':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('There are invalid transactions')
    elif choice == 'q':
        waiting_for_input = False
    elif choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender':'Denise','recipient':'Arnaud','amount':100.0}]
            }
    else:
        print('Input was invalid, please pick a value from the list!')
    if not verify_blockchain():
        print('Invalid blockchain!')
        break
    print(f"Balance of {owner}: {get_balance(owner):6.2f}")
else:
    print('User left!')

print("Done!")
