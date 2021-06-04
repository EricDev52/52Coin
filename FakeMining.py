from Blockchain import *

Blockchain = BlockChain()
Blockchain.LoadBlocks()

def FakeMining(Miner): # Just for showing the validate blocks and transactions function
    Blockchain.CurrentTransactions.append({'Sender': 'Someone', 'Recipient': 'FakeMiner', 'Quantity': 1000})
    Blockchain.BlockMining(Miner)
    Blockchain.SaveBlocks()

FakeMining("FakeMiner")