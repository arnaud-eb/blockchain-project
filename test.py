blockchain = []

def get_last_blockchain_value():
    """ Returns the last value of the current blockchain"""
    if blockchain==[]:
        initial_transaction=float(input("What's the amount of the initial transaction? "))
        return initial_transaction
    else:
        return blockchain[-1]


def add_value(last_transaction,transaction_amount):
    blockchain.append([last_transaction,transaction_amount])


def get_transaction_value():
    return float(input("What's the transaction amount please? ")) 


def get_user_choice():
    print("Please choose")
    print("1: Add a new transaction value")
    print("2: Output the blockchain blocks")
    print("q: Quit")
    return input("Your choice: ")

def print_blockchain_elements():
    for block in blockchain:
            print('Outputting Block')
            print(block)
    print('Blockchain')
    print(blockchain)

while True:
    choice=get_user_choice()
    if choice=='1':
        add_value(get_last_blockchain_value(),get_transaction_value())
    elif choice=='2':
        print_blockchain_elements()
    elif choice=='q':
        break
    else:
        print('Input was invalid, please pick a value from the list!')

print("Done!")