from brownie import accounts, Contract, TokenERC20

def test__token():

        owners = [accounts[0], accounts[1], accounts[2]]
        multisig = MultiSigWallet.deploy(owners, 2,  {'from':accounts[0]})

        implementation = TokenERC20.deploy({'from':accounts[0]})
        proxy = UpgradeabilityProxy.deploy(implemenation.address, {'from':accounts[0]})
        upgradable = Contract.from_abi('TokenERC20', proxy.address, TokenERC20.abi)

        implementation.initialize(multisig.address, 100, 'xToken', 'XTK', {'from':accounts[0]})
        implementation.balanceOf(multisig)

            import json
            proxyABI = json.load(open("scripts/Proxy.json"))

            token = Contract.from_abi('TokenERC20', '0xE7eD6747FaC5360f88a2EFC03E00d25789F69291', TokenERC20.abi)
            proxy = Contract.from_abi('TokenERC20', '0xE7eD6747FaC5360f88a2EFC03E00d25789F69291', proxyABI)

            multisig = Contract.from_abi('MultiSigWallet', '0x3194cBDC3dbcd3E11a07892e7bA5c3394048Cc87', MultiSigWallet.abi)
