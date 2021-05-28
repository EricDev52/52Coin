from Blockchain import *
import time

Blockchain = BlockChain()
Blockchain.LoadBlocks()

while True:
    Blockchain.LoadCurrentTransactions()
    Blockchain.BlockMining("Miner")
    print("Added Block: " + str(len(Blockchain.AllBlocks)-1))
    Blockchain.SaveBlocks()