import hashlib
import time

BlockchainDataFilePath = "Python/52Coin/BlockchainData.txt"
CurrentTransactionsFilePath = "Python/52Coin/CurrentTransactions.txt"

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
        self.Difficulty = 5
        self.MiningReward = 1

    def CreateNode(self, Address):
        self.Nodes.add(Address)

    def AddBlock(self, block):
        self.CurrentTransactions = []
        self.AllBlocks.append(block)
        
    @staticmethod
    def CheckValidity(block, PrevBlock):
        if PrevBlock.Index + 1 != block.Index: return False
        if PrevBlock.CalculateHash != block.PrevHash: return False
        if not BlockChain.VerifyProof(block): return False
        if block.Timestamp <= PrevBlock.Timestamp: return False
        return True
        
    def NewTransaction(self, Sender, Recipient, Quantity):
        if BlockChain.CheckTransactionValidity(Sender, Recipient, Quantity):
            self.CurrentTransactions.append({"Sender": Sender, "Recipient": Recipient, "Quantity": Quantity})
    
    @staticmethod
    def CheckTransactionValidity(Sender, Recipient, Quantity):
        if not (type(Sender) is str and type(Recipient) is str and (type(Quantity) is float or type(Quantity) is int)): return False
        if Sender == Recipient: return False
        if Quantity <= 0: return False
        if Sender == "Source" or Recipient == "Source": return False
        return True

    def ProofOfWork(self, block):
        block.Nonce = 0
        while self.VerifyProof(block) == False:
            block.Nonce += 1
        return block
        
    def VerifyProof(self, block):
        Hash = block.CalculateHash()
        return Hash.startswith(self.Difficulty * "0")
        
    def BlockMining(self, Miner):
        if not type(Miner) is str: return
        self.CurrentTransactions.append({"Sender": "Source", "Recipient": Miner, "Quantity": self.MiningReward})
        PrevHash = 0
        if len(self.AllBlocks) > 0: PrevHash = self.AllBlocks[-1].CalculateHash()
        NewBlock = Block(len(self.AllBlocks), self.CurrentTransactions, PrevHash, 0)
        NewBlock = self.ProofOfWork(NewBlock)
        self.AddBlock(NewBlock)

    def LoadBlocks(self):
        with open(BlockchainDataFilePath, "r") as File:
            for Line in File:
                BlockInfo = Line.split(" | ")
                for i in range(len(BlockInfo)):
                    if (i == 1): BlockInfo[i] = BlockInfo[i].strip("Transactions: ")
                    else: BlockInfo[i] = BlockInfo[i].split(": ")[1]
                ReadedBlock = Block(int(BlockInfo[0]), eval(BlockInfo[1]), BlockInfo[2], int(BlockInfo[3]), float(BlockInfo[4]))
                self.AllBlocks.append(ReadedBlock)

    def SaveBlocks(self):
        with open(BlockchainDataFilePath, "w") as File:
            for i in range(len(self.AllBlocks)):
                File.write(self.AllBlocks[i].GetString() + "\n")
    
    def LoadCurrentTransactions(self):
        with open(CurrentTransactionsFilePath, "r") as File:
            for Line in File:
                self.CurrentTransactions.append(eval(Line))
        with open(CurrentTransactionsFilePath, "w") as File:
            File.write("")

    def SaveCurrentTransactions(self):
        with open(CurrentTransactionsFilePath, "w") as File:
            for i in range(len(self.CurrentTransactions)):
                File.write(str(self.CurrentTransactions[i]) + "\n")