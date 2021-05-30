from Blockchain import *

Blockchain = BlockChain()
Blockchain.LoadBlocks()

def Mining(Miner):
    while True:
        Blockchain.LoadCurrentTransactions()
        Blockchain.BlockMining(Miner)
        print("Added Block: " + str(len(Blockchain.AllBlocks)-1))
        Blockchain.SaveBlocks()

Mining("Miner")