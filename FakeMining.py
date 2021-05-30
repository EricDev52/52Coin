from Blockchain import *

Blockchain = BlockChain()
Blockchain.LoadBlocks()

def FakeMining(Miner):
    Blockchain.CurrentTransactions.append({'Sender': 'Someone', 'Recipient': 'FakeMiner', 'Quantity': 1000})
    Blockchain.BlockMining(Miner)
    Blockchain.SaveBlocks()

FakeMining("FakeMiner")