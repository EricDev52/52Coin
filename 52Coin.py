import hashlib
import time

MiningReward = 1

class Block:
    def __init__(self, Index, Transactions, PrevHash, Nonce, Timestamp=None):
        self.Index = Index
        self.Transactions = Transactions
        self.PrevHash = PrevHash
        self.Nonce = Nonce
        self.Timestamp = Timestamp or time.time()
    
    def CalculateHash(self):
        BlockString = "{}{}{}{}{}".format(self.Index, self.Transactions, self.PrevHash, self.Nonce, self.Timestamp)
        return hashlib.sha256(BlockString.encode()).hexdigest()

class BlockChain:
    def __init__(self):
        self.AllBlocks = []
        self.CurrentTransactions = []
        self.Nodes = set()
        self.AddBlock(Block(0, [], 0, 0))

    def CreateNode(self, Address):
        self.Nodes.add(Address)

    def AddBlock(self, Block):
        self.CurrentTransactions = []
        self.AllBlocks.append(Block)
        
    @staticmethod
    def CheckValidity(Block, PrevBlock):
        if PrevBlock.Index + 1 != Block.Index: return False
        if PrevBlock.CalculateHash != Block.PrevHash: return False
        if not BlockChain.VerifyProof(Block): return False
        if Block.Timestamp <= PrevBlock.Timestamp: return False
        return True
        
    def NewTransaction(self, Sender, Recipient, Quantity):
        self.CurrentTransactions.append({"Sender": Sender, "Recipient": Recipient, "Quantity": Quantity})
        
    @staticmethod
    def ProofOfWork(Block):
        Block.Nonce = 0
        while BlockChain.VerifyProof(Block) == False:
            Block.Nonce += 1
        return Block
        
    @staticmethod
    def VerifyProof(Block):
        PrefixZeros = 4
        Hash = Block.CalculateHash()
        return Hash.startswith(PrefixZeros * "0")
        
    def BlockMining(self, MinerName):
        self.NewTransaction("0", MinerName, MiningReward)
        PrevBlock = self.AllBlocks[-1]
        PrevHash = PrevBlock.CalculateHash()
        Block = Block(len(self.AllBlocks), self.CurrentTransactions, PrevHash, 0)
        Block = self.ProofOfWork(Block)
        self.AddBlock(Block)

def PrintBlock(Block):
    print("Index: " + str(Block.Index) + " | Transactions: " + str(Block.Transactions) + " | PrevHash: " + str(Block.PrevHash) + " | Nonce: " + str(Block.Nonce) + " | Timestamp: " + str(Block.Timestamp))

blockchain = BlockChain()
PrintBlock(blockchain.AllBlocks[0])