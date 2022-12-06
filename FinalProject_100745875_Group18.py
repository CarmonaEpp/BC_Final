# Alex Carmona-Epp 
# 100745875
# Project Group 18
# Blockchain Final Project 
# Blockchain integration with tracking



#################################################################################
# PS this is my own project code from assignment 1, I have refitted it to fit the use case of this project. 
#################################################################################


import sys
import json
import hashlib
from flask import Flask
from time import time
from uuid import uuid4
from urllib.parse import urlparse
from flask.globals import request
from flask.json import jsonify


class Blockchain(object):
    difficulty_level = "0000"
    def __init__(self):
        self.chain = []
        self.current_transaction = []
        genesis_Hash = self.Block_Hash("genesis_block")
        for x in range(0,1):
            self.append_block(
                Previous_block_hash = genesis_Hash,
                nonce = self.PoW(x,genesis_Hash, [])
                )
            x += 1 

    def Block_Hash(self,block):
        blockEncoder = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(blockEncoder).hexdigest()
    def PoW(self,index,Previous_block_hash,transactions):
        nonce=0
        while self.validate_Proof(index,Previous_block_hash,
                                  transactions, nonce) is False:
            nonce+=1
            print(nonce)
        print(nonce)
        return nonce
    def validate_Proof(self,index,Previous_block_hash,transactions,nonce):
        data = f'{index},{Previous_block_hash},{transactions},{nonce}'.encode()
        hash_data = hashlib.sha256(data).hexdigest()
        return hash_data[:len(self.difficulty_level)] == self.difficulty_level
        
### Main function for this assignment!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def append_block(self,nonce, Previous_block_hash):
        weightInput = input("What is the weight of the package in pounds?")
        sourceInput = input("What is the source address?")
        destInput = input("What is the destination address?")
        companyInput = input("What is the shipping company for this package?")

        block ={
            'index': len(self.chain),
            'transactions':self.current_transaction,
            'nonce' : nonce,
            'Previous_block_hash': Previous_block_hash,
            'timestamp': time(),
            'weight' : (weightInput, "lbs"),
            'source' : (sourceInput),
            'destination' : (destInput), 
            'shipping_company' : (companyInput)
        }
        self.current_transaction = []
        self.chain.append(block)
        return block
    def add_transaction(self, sender, receipient, amount):
        self.current_transaction.append({
            'amount':amount,
            'receipient':receipient,
            'sender':sender
            })
        return self.last_block['index']+1
    @property
    def last_block(self):
        return self.chain[-1]

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-',"")
blockchain = Blockchain()

@app.route('/blockchain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
        }
    return jsonify(response), 200

@app.route('/mine', methods=['GET'])
def mine_block():
    start = time()
    blockchain.add_transaction(
        sender = "0",
        receipient = node_identifier,
        amount = 1
        )
    last_block_hash = blockchain.Block_Hash(blockchain.last_block)
    index = len(blockchain.chain)
    nonce = blockchain.PoW(index,last_block_hash,blockchain.current_transaction)
    block = blockchain.append_block(nonce,last_block_hash)
    end = time()
    response = {
        'message': "new block has been added (mined)",
        'index': block['index'],
        'hash_of_previous_block': block['Previous_block_hash'],
        'nonce':block['nonce'],
        'transaction':block['transactions'], 
        'timeSpent':(end-start)
        }
    return jsonify(response), 200

@app.route('/transaction/new', methods=['POST'])
def new_transactions():
    values = request.get_json()
    required_fields = ['sender','receipient','amount']
    if not all (k in values for k in required_fields):
        return ('Missing Fields', 400)
    index = blockchain.add_transaction(
        values['sender'],
        values['receipient'],
        values['amount']
        )
    response = {'message': f'Transaction will be added to the block {index}'}
    return (jsonify(response),201)

@app.route('/transaction', methods=['GET'])
def transaction():
    response = {
        'current_transaction': blockchain.current_transaction
        }
    return (jsonify(response),201)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=80)
        
        



