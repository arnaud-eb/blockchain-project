from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain
from block import Block

app = Flask(__name__)
wallet=Wallet()
blockchain=Blockchain(wallet.public_key)
CORS(app)

@app.route('/', methods=['GET'])
def get_ui():
    return send_from_directory('ui','node.html')


@app.route('/wallet', methods=['POST'])
def create_keys():
    if wallet.create_keys():
        global blockchain
        blockchain=Blockchain(wallet.public_key)
        response={
            'public_key':wallet.public_key,
            'private_key':wallet.private_key,
            'funds':round(blockchain.get_balance(),2)
        }
        return jsonify(response),201
    else:
        response={
            'message':'Saving the keys failed.'
        }
        return jsonify(response),500

@app.route('/wallet', methods=['GET'])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain=Blockchain(wallet.public_key)
        response={
            'public_key':wallet.public_key,
            'private_key':wallet.private_key,
            'funds':round(blockchain.get_balance(),2)
        }
        return jsonify(response),200
    else:
        response={
            'message':'Loading the keys failed'
        }
        return jsonify(response),500

@app.route('/balance', methods=['GET'])
def get_balance():
    balance=blockchain.get_balance()
    if balance!=None:
        response={
            'message':'Fetched balance successfully.',
            'funds':round(balance,2)
        }
        return jsonify(response),200
    else:
        response={
            'message':'Loading balance failed.',
            'wallet_set_up':wallet.public_key!=None
        }
        return jsonify(response),500


@app.route('/transaction', methods=['POST'])
def add_transaction():
    if wallet.public_key==None:
        response={
            'message':'No wallet set up.'
        }
        return jsonify(response),400
    values = request.get_json()
    if not values:
        response={
            'message':'No data found.'
        }
        return jsonify(response),400
    required_fields=['recipient','amount']
    if not all([field in values for field in required_fields]):
        response={
            'message':'Required data is missing'
        }
        return jsonify(response),400
    signature=wallet.sign_transaction(wallet.public_key,values['recipient'],values['amount'])
    transaction=blockchain.add_transaction(values['recipient'],wallet.public_key,signature,values['amount'])
    if transaction!=None:
        response={
            'message':'Transaction added successfully.',
            'transaction':transaction.__dict__,
            'funds':round(blockchain.get_balance(),2)
        }
        return jsonify(response),201
    else:
        if values['amount']>blockchain.get_balance():
            response={
            'message':'Insufficient funds.'
            }
            return jsonify(response),500
        else:
            response={
                'message':'Creating a transaction failed.',
                'wallet_set_up':wallet.public_key!=None
            }
            return jsonify(response),500


@app.route('/mine', methods=['POST'])
def mine():
    if blockchain.mine_block():
        block=blockchain.chain[-1]
        block_dict=block.__dict__.copy()
        block_dict['transactions']=[tx.__dict__ for tx in block_dict['transactions']]
        response={
            'message':'Block added successfully.',
            'block': block_dict,
            'funds':round(blockchain.get_balance(),2)
        }
        return jsonify(response),201
    else:
        response={
            'message':'Adding a block failed.',
            'wallet_set_up':wallet.public_key != None
        }
        return jsonify(response),500

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot=[block.__dict__.copy() for block in [Block(block.previous_hash,block.index,[tx.__dict__ for tx in block.transactions],block.proof) for block in blockchain.chain]]
    return jsonify(chain_snapshot),200

@app.route('/transactions', methods=['GET'])
def get_open_transactions():
    transactions_snapshot=[tx.__dict__ for tx in blockchain.get_open_transactions()]
    return jsonify(transactions_snapshot),200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

