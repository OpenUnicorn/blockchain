
class Blockchain:
	def __init__(self):
		self.chain = [] #store the blockchain
		self.transactions = [] # list of dictionary elements to store the transactons
	def new_block(self):
		#ToDO: Create a new block and add it to the chain
		pass
	def new_transaction(self):
		'''
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
		#TODO: Hash the block
		pass
	
	@property
	def last_block(self):
		#return the last block on the chain
		pass
