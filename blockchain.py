
class Blockchain:
	def __init__(self):
		self.chain = [] #store the blockchain
		self.transactions = [] # to store the transactons
	def new_block(self):
		#ToDO: Create a new block and add it to the chain
		pass
	def new_transaction(self):
		#TODO: Add a new transaction to the list of transactions
		pass
	
	@staticmethod
	def hash(block):
		#TODO: Hash the block
		pass
	
	@property
	def last_block(self):
		#return the last block on the chain
		pass
