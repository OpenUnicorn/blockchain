import hashlib
import json
from time import time

class Blockchain:
	def __init__(self):
		self.chain = [] #store the blockchain
		self.transactions = [] # list of dictionary elements to store the transactons
		
		#When we first initialize the blockchain we need to create the genesis block and show proof of work
		self.new_block(previous_hash=1,proof=100)
		
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
		self.transaction.append({
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
		block_string = json.dumps(block,sort_keys=True).encode()
	
	@property
	def last_block(self):
		return self.chain[-1]
