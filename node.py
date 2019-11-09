from verification import Verification
from uuid import uuid4
from blockchain import Blockchain

class Node:

    def __init__(self):
        # self.id=str(uuid4())
        self.id='Arnaud'
        self.blockchain=Blockchain(self.id)

    def get_user_choice(self):
        print("Please choose")
        print("1: Add a new transaction value")
        print("2: Mine a new block")
        print("3: Output the blockchain blocks")
        print("4: Check transaction validity")
        print("q: Quit")
        return input("Your choice: ")

    def get_transaction_value(self):
        new_recipient = input("Enter the recipient of the transaction: ")
        new_amount = float(input("Your transaction amount please: "))
        return new_recipient, new_amount

    def print_blockchain_elements(self):
        for block in self.blockchain.chain:    
            print('Outputting Block')
            print(block)

    def listening_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            choice = self.get_user_choice()
            if choice == '1':
                new_recipient, new_amount = self.get_transaction_value()
                if self.blockchain.add_transaction(new_recipient, self.id, new_amount):
                    print('Added transaction!')
                else:
                    print('Transaction failed!')
            elif choice == '2':
                self.blockchain.mine_block()
            elif choice == '3':
                self.print_blockchain_elements()
            elif choice == '4':
                if Verification.verify_transactions(self.blockchain.get_balance,self.blockchain.get_open_transactions()):
                    print('All transactions are valid')
                else:
                    print('There are invalid transactions')
                print(self.blockchain.get_open_transactions())
            elif choice == 'q':
                waiting_for_input = False
            else:
                print('Input was invalid, please pick a value from the list!')
            if not Verification.verify_blockchain(self.blockchain.chain):
                print('Invalid blockchain!')
                break
            print(f"Balance of {self.id}: {self.blockchain.get_balance():6.2f}")
        else:
            print('User left!')

        print("Done!")

node=Node()
node.listening_for_input()