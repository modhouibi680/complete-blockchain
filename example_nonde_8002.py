#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from general_blockchain import GeneralBlockchain
from uuid import uuid4
import requests
#Web app
app = Flask(__name__)

#uid node address
uid_nnode_address = str(uuid4()).replace('-', '')
#Create blockchain
general_blockchain = GeneralBlockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    last_block =general_blockchain.get_last_block()
    last_nonce = last_block['nonce']
    
    new_nonce = general_blockchain.proof_of_work(last_nonce)
    prev_hash = general_blockchain.hash_block(last_block)
    general_blockchain.add_transaction(sender = uid_nnode_address, receiver = 'Person_One', amount = 50)
    new_block = general_blockchain.gen_block(new_nonce, prev_hash)
    
    
    response = {
        'message': 'New block mined',
        'index': new_block['index'],
        'timestamp': new_block['timestamp'],
        'nonce': new_block['nonce'],
        'prev_hash': new_block['prev_hash'],
        'transactions': new_block['transactions']
        
        }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    response = {
        'chain': general_blockchain.chain,
        'length': len(general_blockchain.chain)
                }
    return jsonify(response), 200

@app.route('/validate_chain', methods=['GET'])
def is_valid_chain():
    is_valid = general_blockchain.is_valid_chain(general_blockchain.chain)
    if is_valid:
        response = {'message': 'Blockchain is valid', 'valid_chain': is_valid}
    else:
        response = {'message': 'Blockchain is Not valid', 'valid_chain': is_valid}
        
    return jsonify(response), 200    

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    payload = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all (key in payload for key in transaction_keys ):
        return 'Invalid transaction', 400
    index_bolock = general_blockchain.add_transaction(payload['sender'], payload['receiver'], payload['amount'])
    
    response = {'message': f'Transaction will be added to Block {index_bolock}'}
    return jsonify(response), 201   

@app.route('/connect_node', methods=['POST'])
def connect_node():
    payload = request.get_json()      
    nodes = payload.get ('nodes')
    if nodes is None:
        return "No node is running"  , 400
    for node in nodes:
        general_blockchain.add_node(node)
    response = {'message': 'All nodes are connected', 'total nodes': list(general_blockchain.nodes)}
    return jsonify(response), 201      

@app.route('/replace_chain', methods=['GET'])
def consensus_replace_chain():
    to_replace_chain = general_blockchain.replace_chain()
    if to_replace_chain:
        response = {'message': 'Chain was replaced with the longest chain', 'correct_chain': general_blockchain.chain}
    else:
        response = {'message': 'Chain is the longest',  'correct_chain': general_blockchain.chain}
        
    return jsonify(response), 200  
    
        

#run App
app.run(host = '0.0.0.0', port = 8002)
    
    
    
