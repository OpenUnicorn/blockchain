import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from flask import Flask,jsonify,request
from urllib.parse import urlparse
import requests

class Blockchain:
	def __init__(self):
		self.chain = [] #store the blockchain
		self.transactions = [] # list of dictionary elements to store the transactons
		self.nodes = set()
		
		#When we first initialize the blockchain we need to create the genesis block and show proof of work
		self.new_block(previous_hash=1,proof=100)
	
	def register_node(self,address):
		'''
		Add a new node to the list of nodes
		:param address <string> Address of the node(http://0.0.0.0:5000)
		'''
		
		
		parsed_url = urlparse(address)
		self.node.add(parsed_url.netloc)
	
	def valid_chain(self,chain):
		'''Determine is blockchain is valid
		:param chain: <list> The Blockchain
		:return <Boolean> True if valid, False if not
		'''
		last_block=chain[0]
		i = 1
		
		while i<len(chain):
			block = chain[current_index]
			print(f'{last_block}')
			print(f'{block}')
			print('\n------------------\n')
			
			if block['previous_hash'] !=self.hash(last_block):
				return False
			
			if not self.valid_proof(last_block['proof'],block['proof']):
				return False
			
			last_block = block
			i+=1
	
		return True
	
	def resolve_conflict(self):
		'''
		Resolve conflice by replacing the chain with the longest one in the network.
		:return <bool> True if our chain was replaced, False if not
		'''
		neighbours = self.nodes
		new_chain = None
		
		max_length = len(self.chain)
		
		for node in neighbours:
			response = requests.get(f'http://{node}/chain')
			
			if response.status_code == 200:
				length = response.json()['length']
				chain = response.json()['chain']
				
				if length>max_length and self.valid_chain(chain):
					max_length = length
					new_chain = chain
		
		if new_chain:
			self.chain = new_chain
			return True
		
		return False
		
	def new_block(self,proof,previous_hash=None):
		'''
		Create a new block in the blockchain
		
		:param proof: <int> The proof given by the Proof of work algorithm
		:param previous_has: (Optional)<string> Hash of the previous block
		:return: <dicttionary> New Block
		'''
		block = {
		'index':len(self.chain)+1, 
		'timestamp': time(),
		'transaction':self.transactions,
		'proof':proof,
		'previous_hash': previous_hash or self.hash(self.chain[-1])
		}
		
		self.transactions = []
		self.chain.append(block)
		return block
		
	def new_transaction(self,sender,recipient,amount):
		'''
		Create a new transaction
		
		:param sender: <string> Address of the sender
		:param recipient: <string> Address of the Recipient
		:param amount: <int> Amount
		:return: <int>The index of the block that will hold this transaction
		'''
		self.transactions.append({
		'sender': sender,
		'recipient': recipient,
		'amount': amount,
		})
		
		return self.last_block['index']+1
	
	@staticmethod
	def hash(block):
		'''
		Create a SHA-256 hash of the block
		
		:param block: <dictionary> Block
		:return <string> Hashed Blocked
		'''
		
		# If the dictionary is not ordered we get inconsistent hashes
		StringToEncode = json.dumps(block,sort_keys=True).encode()
		return hashlib.sha256(StringToEncode).hexdigest()
	
	@property
	def last_block(self):
		return self.chain[-1]
		
	
	def proof_of_work(self,last_proof):
		'''
		Simple Proof of Work Algorithm:
		-Find a number x such that hash(yx) contains 4 leading 0
		-We can increase the difficulty by adding more leading 0's
		-x is the new proof, y is the last proof
		
		:params last_proof: <int> Last Proof
		:return: <int>
		'''
		
		proof = 0
		while self.validate_proof(last_proof,proof) is False:
			proof +=1
		
		return proof
	
	@staticmethod
	def validate_proof(last_proof,proof):
		'''
		Validates the prooof
		:param last_proof: <int> Previous Proof
		:param proof: <int> Current Proof
		:return: <bool> True if has 4 leading 0, False if not.
		'''
		
		guess = f'{last_proof}{proof}'.encode()# using f strings to concatinate the proofs
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == '0000'




app = Flask(__name__)
node_identifier = str(uuid4()).replace('-','')


blockchain = Blockchain()

@app.route('/mine',methods = ['GET'])
def mine():
	last_block = blockchain.last_block
	last_proof = last_block['proof']
	proof = blockchain.proof_of_work(last_proof)
	
	#Sender is 0 to signify that the node has mined a new coin
	blockchain.new_transaction(
	sender='0',
	recipient = node_identifier,
	amount = 1
	)
	
	#Create a new block by adding it to the chain
	previous_hash = blockchain.hash(last_block)
	block = blockchain.new_block(proof,previous_hash)
	
	response = {
	'message': 'New Block Created',
	'index' :block['index'],
	'transaction':block['transaction'],
	'proof': block['proof'],
	'previous_hash': block['previous_hash']
	}
	return jsonify(response),200

@app.route('/transactions/new',methods = ['POST'])
def new_transaction():
	values = request.get_json()
	
	required = ['sender','recipient','amount']
	if not all(k in values for k in required):
		return 'Missing Values',400
		
		index = blockchain.new_transaction(values['sender'],values['recipient'],values['amount'])
		
		response = {'message':f'Transaction will be added to Block {index}'}
		return jsonify(response),201
	

@app.route('/chain',methods = ['GET'])
def full_chain():
	response = {
	'chain' :blockchain.chain,
	'length': len(blockchain.chain)
	}
	return jsonify(response),200

@app.route('/nodes/register',methods = ['POST'])
def register_nodes():
	values = request.get_json()
	
	nodes = values.get('nodes')
	if nodes is None:
		return 'Error: Please supply a valid list of nodes',400
	
	for node in nodes:
		blockchain.register_node(node)
	
	response = {
	'message': 'New Nodes Added',
	'total_nodes':list(blockchain.nodes),
	}
	
	return jsonify(response),201

@app.route('/nodes/resolve',methods=['GET']_
def consensus():
	replaced = blockchain.resolve_conflict()
	
	if replaced:
		 response = {
		 'message': 'Our Chain is authoritative',
		 'chain' : blockchain.chain
		 }
	else:
		response {
		'message' : 'Current chain is in control',
		'chain' : blockchain.chain
		}
	return jsonify(response),200

if __name__ == '__main__':
	app.run(host = '0.0.0.0',port=5000)
