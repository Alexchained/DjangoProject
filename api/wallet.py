from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/eb3a91a1148846ec87666337161515be'))
account = w3.eth.account.create()
privateKey = account.privateKey.hex()
address = account.address

print (f"Your address: {address}\nYour key: {privateKey}")