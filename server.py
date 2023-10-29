#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from general_blockchain import GeneralBlockchain

#Web app
app = Flask(__name__)

#Create blockchain
general_blockchain = GeneralBlockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    last_block =general_blockchain.get_last_block()
    last_nonce = last_block['nonce']
    
    new_nonce = general_blockchain.proof_of_work(last_nonce)
    prev_hash = general_blockchain.hash_block(last_block)
    
    new_block = general_blockchain.gen_block(new_nonce, prev_hash)
    
    response = {
        'message': 'New block mined',
        'index': new_block['index'],
        'timestamp': new_block['timestamp'],
        'nonce': new_block['nonce'],
        'prev_hash': new_block['prev_hash']
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
        response = {'message': 'Blockchain is valid'}
    else:
        response = {'message': 'Blockchain is Not valid'}
        
    return jsonify(response), 200       
        

#run App
app.run(host = '0.0.0.0', port = 8001)
    
    
    
