import hashlib
import time

BlockchainDataFilePath = "Python/52Coin/BlockchainData.txt"
MiningReward = 1
PrefixZeros = 4

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
    
    def GetString(self):
        return "Index: " + str(self.Index) + " | Transactions: " + str(self.Transactions) + " | PrevHash: " + str(self.PrevHash) + " | Nonce: " + str(self.Nonce) + " | Timestamp: " + str(self.Timestamp) + " | Hash: " + str(self.CalculateHash())

class BlockChain:
    def __init__(self):
        self.AllBlocks = []
        self.CurrentTransactions = []
        self.Nodes = set()

    def CreateNode(self, Address):
        self.Nodes.add(Address)

    def AddBlock(self, Block: Block):
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
        if Sender == "Newly Generated Coins": raise Exception("Name cant be 'Newly Generated Coins'")
        self.CurrentTransactions.append({"Sender": Sender, "Recipient": Recipient, "Quantity": Quantity})
        
    @staticmethod
    def ProofOfWork(Block):
        Block.Nonce = 0
        while BlockChain.VerifyProof(Block) == False:
            Block.Nonce += 1
        return Block
        
    @staticmethod
    def VerifyProof(Block):
        Hash = Block.CalculateHash()
        return Hash.startswith(PrefixZeros * "0")
        
    def BlockMining(self, Miner):
        self.CurrentTransactions.append({"Sender": "Newly Generated Coins", "Recipient": Miner, "Quantity": MiningReward})
        PrevHash = 0
        if len(self.AllBlocks) > 0: PrevHash = self.AllBlocks[-1].CalculateHash()
        NewBlock = Block(len(self.AllBlocks), self.CurrentTransactions, PrevHash, 0)
        NewBlock = self.ProofOfWork(NewBlock)
        self.AddBlock(NewBlock)

Blockchain = BlockChain()

with open(BlockchainDataFilePath, "r") as File: # Load all blocks from the file in the blockchain
    for Line in File:
        BlockInfo = Line.split(" | ")
        for i in range(len(BlockInfo)):
            if (i == 1): BlockInfo[i] = BlockInfo[i].strip("Transactions: ")
            else: BlockInfo[i] = BlockInfo[i].split(": ")[1]
        ReadedBlock = Block(int(BlockInfo[0]), eval(BlockInfo[1]), BlockInfo[2], int(BlockInfo[3]), float(BlockInfo[4]))
        Blockchain.AllBlocks.append(ReadedBlock)

Blockchain.BlockMining("Miner")
Blockchain.NewTransaction("Me", "You", 100)
Blockchain.BlockMining("Miner")

with open(BlockchainDataFilePath, "w") as File: # Save all blocks in file
    for i in range(len(Blockchain.AllBlocks)):
        File.write(Blockchain.AllBlocks[i].GetString() + "\n")