blockchain = []


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain"""
    if blockchain == []:
        return None
    return blockchain[-1]


def add_transaction(transaction_amount, last_transaction):
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])


def get_transaction_value():
    return float(input("What's the transaction amount please? "))


def get_user_choice():
    print("Please choose")
    print("1: Add a new transaction value")
    print("2: Output the blockchain blocks")
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
    for bc_index in range(1, len(blockchain)):
        if blockchain[bc_index-1] == blockchain[bc_index][0]:
            continue
        else:
            return False
    return True

waiting_for_input=True

while waiting_for_input:
    choice = get_user_choice()
    if choice == '1':
        add_transaction(get_transaction_value(), get_last_blockchain_value())
    elif choice == '2':
        print_blockchain_elements()
    elif choice == 'q':
        waiting_for_input=False
    elif choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    else:
        print('Input was invalid, please pick a value from the list!')
    if not verify_blockchain():
        print('Invalid blockchain!')
        break
else:
    print('User left!')

print("Done!")
