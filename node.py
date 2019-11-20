from utility.verification import Verification
from uuid import uuid4
from blockchain import Blockchain
from wallet import Wallet

class Node:

    def __init__(self):
        self.wallet=Wallet()
        self.blockchain=Blockchain(self.wallet.public_key)

    def get_user_choice(self):
        print("Please choose")
        print("1: Add a new transaction value")
        print("2: Mine a new block")
        print("3: Output the blockchain blocks")
        print("4: Check transaction validity")
        print("5: Create wallet")
        print("6: Load wallet")
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
                signature=self.wallet.sign_transaction(self.wallet.public_key,new_recipient,new_amount)
                if self.blockchain.add_transaction(new_recipient, self.wallet.public_key, signature, new_amount):
                    print('Added transaction!')
                else:
                    print('Transaction failed!')
            elif choice == '2':
                if not self.blockchain.mine_block():
                    print('Mining failed. Got no wallet?')
            elif choice == '3':
                self.print_blockchain_elements()
            elif choice == '4':
                if Verification.verify_transactions(self.blockchain.get_balance,self.blockchain.get_open_transactions()):
                    print('All transactions are valid')
                else:
                    print('There are invalid transactions')
                print(self.blockchain.get_open_transactions())
            elif choice == '5':
                self.wallet.create_keys()
                self.blockchain=Blockchain(self.wallet.public_key)
            elif choice == '6':
                self.wallet.load_keys()
                self.blockchain=Blockchain(self.wallet.public_key)
            elif choice == 'q':
                waiting_for_input = False
            else:
                print('Input was invalid, please pick a value from the list!')
            if not Verification.verify_blockchain(self.blockchain.chain):
                print('Invalid blockchain!')
                break
            print(f"Balance of {self.wallet.public_key}: {self.blockchain.get_balance():6.2f}")
        else:
            print('User left!')

        print("Done!")

if __name__ == '__main__':
    node=Node()
    node.listening_for_input()