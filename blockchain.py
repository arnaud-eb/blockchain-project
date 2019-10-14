import functools

MINING_REWARD=10
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Arnaud'
participants={'Arnaud'}

def hash_block(block):
    return "".join([str(value) for value in block.values()])


def get_balance(participant):
    tx_sender=[[tx['amount'] for tx in block['transactions'] if tx['sender']==participant] for block in blockchain]
    open_tx_sender=[tx['amount'] for tx in open_transactions if tx['sender']==participant]
    tx_sender.append(open_tx_sender)
    print(tx_sender)
    amount_sent=functools.reduce(lambda tx_sum,tx_amt:tx_sum + sum(tx_amt) if len(tx_amt)>0 else tx_sum + 0,tx_sender,0)
    tx_recipient=[[tx['amount'] for tx in block['transactions'] if tx['recipient']==participant] for block in blockchain]
    amount_received=functools.reduce(lambda tx_sum,tx_amt:tx_sum + sum(tx_amt) if len(tx_amt)>0 else tx_sum + 0,tx_recipient,0)
    print(tx_recipient)
    return amount_received-amount_sent


def verify_transaction(transaction):
    return get_balance(transaction['sender'])>=transaction['amount']


def add_transaction(recipient, sender=owner, amount=1.0):
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False

def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    copied_transactions=open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions
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
    print(f"Balance of {owner}: {get_balance('Arnaud'):6.2f}")
else:
    print('User left!')

print("Done!")
