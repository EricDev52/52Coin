BlockchainDataFilePath = "Python/52Coin/BlockchainData.txt"
Wallets = {}

with open(BlockchainDataFilePath, "r") as File: # Load all blocks from the file in the blockchain
    for Line in File:
        Transactions = eval(Line.split(" | ")[1].strip("Transactions: "))
        for Transaction in Transactions:
            if Transaction["Sender"] not in Wallets: Wallets[Transaction["Sender"]] = 0
            if Transaction["Recipient"] not in Wallets: Wallets[Transaction["Recipient"]] = 0
            Wallets[Transaction["Sender"]] -= float(Transaction["Quantity"])
            Wallets[Transaction["Recipient"]] += float(Transaction["Quantity"])

print(Wallets)