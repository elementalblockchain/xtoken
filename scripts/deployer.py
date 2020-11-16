# ganache-cli --port 8546 --hostname 192.168.1.200 --gasLimit 12000000 --accounts 10 --hardfork istanbul --mnemonic brownie --fork http://192.168.1.4:3334
# brownie run deployer.py --network forkd
import json
from brownie import TokenERC20, Contract, accounts, MultiSigWallet, UpgradeabilityProxy
from web3 import Web3
	
def createnew():
	owners = [accounts[0], accounts[1], accounts[2]]
	multisig = MultiSigWallet.deploy(owners, 2,  {'from':accounts[0]})

	implementation = TokenERC20.deploy({'from':accounts[0]})
	proxy = UpgradeabilityProxy.deploy(implementation.address, "", {'from':accounts[0]})
	upgradable = Contract.from_abi('TokenERC20', proxy.address, TokenERC20.abi)

	upgradable.initialize(multisig.address, 100, 'xToken', 'XTK', {'from':accounts[0]})
	upgradable.balanceOf(multisig)	
	return((multisig.address, upgradable.address))


def sendTokens(multisig, token):

	web3 = Web3(Web3.HTTPProvider('http://192.168.1.200:8546'))

	ADDRESS = '0x66aB6D9362d4F35596279692F0251Db635165871'
	PRIVATE_KEY = '0xbbfbee4961061d506ffbb11dfea64eba16355cbf1d9c29613126ba7fec0aed5d'

	ADDRESS2 = '0x33A4622B82D4c04a53e170c638B944ce27cffce3'
	PRIVATE_KEY2 = '0x804365e293b9fab9bd11bddd39082396d56d30779efbb3ffb0a6089027902c4a'

	ABI = json.load(open('scripts/TokenERC20.json','r'))
	contractaddress = Web3.toChecksumAddress(token)
	token = web3.eth.contract(abi=ABI, address=contractaddress)
	ABI = json.load(open('scripts/MultiSigWallet.json','r'))
	contractaddress = Web3.toChecksumAddress(multisig)
	multisig = web3.eth.contract(abi=ABI, address=contractaddress)


	gasMultiplier = int(round(web3.eth.gasPrice*1,0))
	gasPrice = web3.toHex(gasMultiplier)
	gas = web3.toHex(10000000)

	data = token.encodeABI(fn_name='transfer',args=[ADDRESS, 5])

	transaction = multisig.functions.submitTransaction(token.address, 0, data).buildTransaction({'chainId': 1, 'gas': gas,'gasPrice': gasPrice,'nonce': web3.toHex(web3.eth.getTransactionCount(ADDRESS)), 'from': ADDRESS})
	signedTx = web3.eth.account.signTransaction(transaction, PRIVATE_KEY)
	txhash = web3.eth.sendRawTransaction(signedTx.rawTransaction)
	print(txhash.hex())

	transaction = multisig.functions.confirmTransaction(0).buildTransaction({'chainId': 1, 'gas': gas,'gasPrice': gasPrice,'nonce': web3.toHex(web3.eth.getTransactionCount(ADDRESS2)), 'from': ADDRESS2})
	signedTx = web3.eth.account.signTransaction(transaction, PRIVATE_KEY2)
	txhash = web3.eth.sendRawTransaction(signedTx.rawTransaction)
	print(txhash.hex())


	data = token.encodeABI(fn_name='transfer',args=[ADDRESS2, 5])

	transaction = multisig.functions.submitTransaction(token.address, 0, data).buildTransaction({'chainId': 1, 'gas': gas,'gasPrice': gasPrice,'nonce': web3.toHex(web3.eth.getTransactionCount(ADDRESS)), 'from': ADDRESS})
	signedTx = web3.eth.account.signTransaction(transaction, PRIVATE_KEY)
	txhash = web3.eth.sendRawTransaction(signedTx.rawTransaction)
	print(txhash.hex())

	transaction = multisig.functions.confirmTransaction(1).buildTransaction({'chainId': 1, 'gas': gas,'gasPrice': gasPrice,'nonce': web3.toHex(web3.eth.getTransactionCount(ADDRESS2)), 'from': ADDRESS2})
	signedTx = web3.eth.account.signTransaction(transaction, PRIVATE_KEY2)
	txhash = web3.eth.sendRawTransaction(signedTx.rawTransaction)
	print(txhash.hex())
	

def main():
	addresses = createnew()
	sendTokens(addresses[0], addresses[1])
	

