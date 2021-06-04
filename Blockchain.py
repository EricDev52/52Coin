import hashlib
import time

BlockchainDataFilePath = "BlockchainData/AllBlocks.txt"
CurrentTransactionsFilePath = "BlockchainData/CurrentTransactions.txt"

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
    
    def GetString(self): # Putting all block information in a string
        return "Index: " + str(self.Index) + " | Transactions: " + str(self.Transactions) + " | PrevHash: " + str(self.PrevHash) + " | Nonce: " + str(self.Nonce) + " | Timestamp: " + str(self.Timestamp) + " | Hash: " + str(self.CalculateHash())

class BlockChain:
    def __init__(self):
        self.AllBlocks = []
        self.CurrentTransactions = []
        self.Difficulty = 5 # The target amount of zeros at the beginning of the block hash
        self.MiningReward = 1 # The reward in the cryptocurrency for mining a new block

    def AddBlock(self, block): # Add new block to the blockchain if its valid
        BlockValid = False
        if (block.Index == 0): BlockValid = self.CheckBlockValidity(block, 0)
        else: BlockValid = self.CheckBlockValidity(block, self.AllBlocks[-1])
        if BlockValid:
            self.CurrentTransactions = []
            self.AllBlocks.append(block)
        else: print("Block " + Block.GetString(block) + " is not valid")
        
    def CheckBlockValidity(self, block, PrevBlock):
        if not self.VerifyProof(block): print("Block doesnt verifies proof"); return False
        for Transaction in block.Transactions[:-1]: # Dont check last transaction because its the miner reward
            Sender = Transaction["Sender"]
            Recipient = Transaction["Recipient"]
            Quantity = Transaction["Quantity"]
            if not BlockChain.CheckTransactionValidity(Sender, Recipient, Quantity): return False
        if block.Index == 0: return True
        if PrevBlock.Index + 1 != block.Index: print("Previous block index plus one doesnt match block index"); return False
        if PrevBlock.CalculateHash() != block.PrevHash: print("Previous block hash doesnt match saved previous block hash"); return False
        if block.Timestamp <= PrevBlock.Timestamp: print("Block timestamp cant be before previous block timestamp"); return False
        return True
        
    def NewTransaction(self, Sender, Recipient, Quantity): # Add to current (pending) transactions
        if BlockChain.CheckTransactionValidity(Sender, Recipient, Quantity):
            self.CurrentTransactions.append({"Sender": Sender, "Recipient": Recipient, "Quantity": Quantity})
        else: print("Transaction " + str({"Sender": Sender, "Recipient": Recipient, "Quantity": Quantity}) + " is not valid")
    
    @staticmethod
    def CheckTransactionValidity(Sender, Recipient, Quantity):
        if not (type(Sender) is str and type(Recipient) is str and (type(Quantity) is float or type(Quantity) is int)): print("Wrong transaction types"); return False
        if Sender == Recipient: print("Transaction sender cant be the recipient"); return False
        if Quantity <= 0: print("Transaction quantity cant be below zero"); return False
        if Sender == "Source" or Recipient == "Source": print("Transaction sender and recipient cant be 'Source'"); return False
        if BlockChain.GetUserBalance(Sender) - Quantity < 0: print("Transaction sender doesnt have enough money"); return False
        return True

    def ProofOfWork(self, block): # Create a proof of work for the block
        block.Nonce = 0
        while self.VerifyProof(block) == False:
            block.Nonce += 1
        return block
        
    def VerifyProof(self, block): # Check if the block start with the wanted amount of zeros
        Hash = block.CalculateHash()
        return Hash.startswith(self.Difficulty * "0")
        
    def BlockMining(self, Miner):
        if not type(Miner) is str: print("Miner name must be a string"); return
        self.CurrentTransactions.append({"Sender": "Source", "Recipient": Miner, "Quantity": self.MiningReward})
        PrevHash = 0
        if len(self.AllBlocks) > 0: PrevHash = self.AllBlocks[-1].CalculateHash()
        NewBlock = Block(len(self.AllBlocks), self.CurrentTransactions, PrevHash, 0)
        NewBlock = self.ProofOfWork(NewBlock)
        self.AddBlock(NewBlock)
    
    @staticmethod
    def GetAllWallets(): # Calculate the current balance for all wallets that are mentioned in the transaction
        Wallets = {}
        with open(BlockchainDataFilePath, "r") as File:
            for Line in File:
                Transactions = eval(Line.split(" | ")[1].strip("Transactions: "))
                for Transaction in Transactions:
                    if Transaction["Sender"] not in Wallets: Wallets[Transaction["Sender"]] = 0
                    if Transaction["Recipient"] not in Wallets: Wallets[Transaction["Recipient"]] = 0
                    Wallets[Transaction["Sender"]] -= float(Transaction["Quantity"])
                    Wallets[Transaction["Recipient"]] += float(Transaction["Quantity"])
        return Wallets

    @staticmethod
    def GetUserBalance(User):
        AllWallets = BlockChain.GetAllWallets()
        if User in AllWallets: return AllWallets[User]
        else: return 0

    def LoadBlocks(self): # Read the blockchain data file and save it into the blockchain all blocks variable
        with open(BlockchainDataFilePath, "r") as File:
            for Line in File:
                BlockInfo = Line.split(" | ")
                for i in range(len(BlockInfo)):
                    if (i == 1): BlockInfo[i] = BlockInfo[i].strip("Transactions: ")
                    else: BlockInfo[i] = BlockInfo[i].split(": ")[1]
                ReadedBlock = Block(int(BlockInfo[0]), eval(BlockInfo[1]), BlockInfo[2], int(BlockInfo[3]), float(BlockInfo[4]))
                self.AllBlocks.append(ReadedBlock)

    def SaveBlocks(self): # Write all blocks to file
        with open(BlockchainDataFilePath, "w") as File:
            for i in range(len(self.AllBlocks)):
                File.write(self.AllBlocks[i].GetString() + "\n")
    
    def LoadCurrentTransactions(self): # Read the current transactions file and save it into the blockchain current transactions variable
        with open(CurrentTransactionsFilePath, "r") as File:
            for Line in File:
                self.CurrentTransactions.append(eval(Line))
        with open(CurrentTransactionsFilePath, "w") as File:
            File.write("")

    def SaveCurrentTransactions(self): # Write current transactions to file
        with open(CurrentTransactionsFilePath, "w") as File:
            for i in range(len(self.CurrentTransactions)):
                File.write(str(self.CurrentTransactions[i]) + "\n")