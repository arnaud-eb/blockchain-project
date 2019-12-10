from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain
from block import Block

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def get_node_ui():
    return send_from_directory('ui', 'node.html')


@app.route('/network', methods=['GET'])
def get_network():
    return send_from_directory('ui', 'network.html')


@app.route('/wallet', methods=['POST'])
def create_keys():
    if wallet.create_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': round(blockchain.get_balance(), 2)
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Saving the keys failed.'
        }
        return jsonify(response), 500


@app.route('/wallet', methods=['GET'])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': round(blockchain.get_balance(), 2)
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'Loading the keys failed'
        }
        return jsonify(response), 500


@app.route('/balance', methods=['GET'])
def get_balance():
    balance = blockchain.get_balance()
    if balance is not None:
        response = {
            'message': 'Fetched balance successfully.',
            'funds': round(balance, 2)
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'Loading balance failed.',
            'wallet_set_up': wallet.public_key is not None
        }
        return jsonify(response), 500


@app.route('/broadcast-transaction', methods=['POST'])
def broadcast_transaction():
    values = request.get_json()
    if not values:
        response = {'message': 'No data found.'}
        return jsonify(response), 400
    required_fields = ['sender', 'recipient', 'signature', 'amount']
    if not all([field in values for field in required_fields]):
        response = {'message': 'Required data is missing'}
        return jsonify(response), 400
    success = blockchain.add_transaction(
        values['recipient'],
        values['sender'],
        values['signature'],
        values['amount'],
        True)
    if success is not None:
        response = {
            'message': 'Transaction added successfully.',
            'transaction': success.__dict__
        }
        return jsonify(response), 201
    else:
        response = {'message': 'Adding a transaction failed.'}
        return jsonify(response), 500


@app.route('/broadcast-block', methods=['POST'])
def broadcast_block():
    values = request.get_json()
    if not values:
        response = {'message': 'No data found.'}
        return jsonify(response), 400
    if 'block' not in values:
        response = {'message': 'Required data is missing'}
        return jsonify(response), 400
    block = values['block']
    if block['index'] == blockchain.chain[-1].index + 1:
        if blockchain.add_block(block):
            response = {'message': 'Block added successfully.'}
            return jsonify(response), 201
        else:
            response = {'message': 'Adding a block failed.'}
            return jsonify(response), 409
    elif block['index'] > blockchain.chain[-1].index:
        response = {
            'message': 'Blockchain seems to differ from local blockchain.'}
        blockchain.resolve_conflicts = True
        return jsonify(response), 200
    else:
        response = {
            'message': 'Blockchain seems to be shorter, block not added.'}
        return jsonify(response), 409


@app.route('/transaction', methods=['POST'])
def add_transaction():
    if wallet.public_key is None:
        response = {
            'message': 'No wallet set up.'
        }
        return jsonify(response), 400
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found.'
        }
        return jsonify(response), 400
    required_fields = ['recipient', 'amount']
    if not all([field in values for field in required_fields]):
        response = {
            'message': 'Required data is missing'
        }
        return jsonify(response), 400
    signature = wallet.sign_transaction(
        wallet.public_key, values['recipient'], values['amount'])
    transaction = blockchain.add_transaction(
        values['recipient'], wallet.public_key, signature, values['amount'])
    if transaction is None:
        response = {
            'message': 'Transaction added successfully.',
            'transaction': transaction.__dict__,
            'funds': round(blockchain.get_balance(), 2)
        }
        return jsonify(response), 201
    else:
        if values['amount'] > blockchain.get_balance():
            response = {
                'message': 'Insufficient funds.'
            }
            return jsonify(response), 500
        else:
            response = {
                'message': 'Creating a transaction failed.',
                'wallet_set_up': wallet.public_key is None
            }
            return jsonify(response), 500


@app.route('/mine', methods=['POST'])
def mine():
    if blockchain.resolve_conflicts:
        response = {'message': 'Resolve conflicts first, block not added!'}
        return jsonify(response), 409
    if blockchain.mine_block():
        block = blockchain.chain[-1]
        block_dict = block.__dict__.copy()
        block_dict['transactions'] = [
            tx.__dict__ for tx in block_dict['transactions']]
        response = {
            'message': 'Block added successfully.',
            'block': block_dict,
            'funds': round(blockchain.get_balance(), 2)
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Adding a block failed.',
            'wallet_set_up': wallet.public_key is None
        }
        return jsonify(response), 500


@app.route('/resolve-conflicts', methods=['POST'])
def resolve_conflicts():
    replaced = blockchain.resolve()
    if replaced:
        response = {'message': 'Chain was replaced.'}
    else:
        response = {'message': "Local chain kept."}
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = [
        block.__dict__.copy() for block in
        [
            Block(
                block.previous_hash,
                block.index,
                [tx.__dict__ for tx in block.transactions],
                block.proof
            ) for block in blockchain.chain
        ]
    ]
    return jsonify(chain_snapshot), 200


@app.route('/transactions', methods=['GET'])
def get_open_transactions():
    transactions_snapshot = [
        tx.__dict__ for tx in blockchain.get_open_transactions()]
    return jsonify(transactions_snapshot), 200


@app.route('/node', methods=['POST'])
def add_peer_node():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found.'
        }
        return jsonify(response), 400
    if 'node' not in values:
        response = {
            'message': 'Required data is missing'
        }
        return jsonify(response), 400
    if blockchain.add_peer_node(values['node']):
        response = {
            'message': 'Node added successfully.',
            'all_nodes': blockchain.print_nodes()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Adding a node failed.'
        }
        return jsonify(response), 500


@app.route('/node/<node_url>', methods=['DELETE'])
def remove_peer_node(node_url):
    if node_url == '' or node_url is None:
        response = {
            'message': 'No node found.'
        }
        return jsonify(response), 400
    if blockchain.remove_peer_node(node_url):
        response = {
            'message': 'Node removed',
            'all_nodes': blockchain.print_nodes()
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'Removing the node failed.'
        }
        return jsonify(response), 500


@app.route('/nodes', methods=['GET'])
def get_peer_nodes():
    peer_nodes = blockchain.print_nodes()
    if len(peer_nodes) > 0:
        response = {
            'message': 'Fetched nodes successfully.',
            'all_nodes': peer_nodes
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'No recorded node.'
        }
        return jsonify(response), 500


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000)
    args = parser.parse_args()
    port = args.port
    wallet = Wallet(port)
    blockchain = Blockchain(wallet.public_key, port)
    app.run(host='0.0.0.0', port=port)
