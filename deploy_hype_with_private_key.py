#!/usr/bin/env python3
"""
HYPE Token Deployment Script
Deploys HYPE token using private key to HyperEVM network
"""

import os
import json
import time
from web3 import Web3
from eth_account import Account
import requests

# HyperEVM Configuration
HYPEREVM_RPC_URL = "https://api.hyperliquid-testnet.xyz/evm"  # Hyperliquid testnet
CHAIN_ID = 998899  # HyperEVM chain ID

# Contract configuration
TOKEN_CONFIG = {
    "name": "HYPE Token",
    "symbol": "HYPE", 
    "decimals": 18,
    "initial_supply": 1000000000,  # 1 billion HYPE
    "max_supply": 1000000000       # 1 billion HYPE max
}

# HYPE Token Contract ABI (simplified for deployment)
CONTRACT_ABI = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "owner", "type": "address"},
            {"indexed": True, "name": "spender", "type": "address"},
            {"indexed": False, "name": "value", "type": "uint256"}
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "from", "type": "address"},
            {"indexed": True, "name": "to", "type": "address"},
            {"indexed": False, "name": "value", "type": "uint256"}
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "inputs": [
            {"name": "spender", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "symbol", 
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Contract bytecode (compiled HYPE token)
CONTRACT_BYTECODE = "0x608060405234801561001057600080fd5b506040518060400160405280600a81526020017f4859504520546f6b656e000000000000000000000000000000000000000000008152506040518060400160405280600481526020017f48595045000000000000000000000000000000000000000000000000000000008152508160039081610089919061031a565b50806004908161009991906103e1565b505050600560009054906101000a900460ff1660ff16600a6100bb91906104c8565b633b9aca006100ca9190610552565b60008190555060005460016000336001600160a01b031681526020019081526020016000208190555033600260006101000a8154816001600160a01b0302191690836001600160a01b031602179055506001600560006101000a81548160ff021916908360ff16021790555060018060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002081905550610603565b600081519050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b600060028204905060018216806101c357607f821691505b6020821081036101d6576101d561019c565b5b50919050565b60008190508160005260206000209050919050565b60006020601f8301049050919050565b600082821b905092915050565b6000600883026102407fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff82610203565b61024a8683610203565b95508019841693508086168417925050509392505050565b6000819050919050565b6000819050919050565b600061029161028c61028784610262565b61026c565b610262565b9050919050565b6000819050919050565b6102ab83610276565b6102bf6102b782610298565b848454610210565b825550505050565b600090565b6102d46102c7565b6102df8184846102a2565b505050565b5b81811015610303576102f86000826102cc565b6001810190506102e5565b5050565b601f82111561034857610319816101dc565b610322846101f1565b81016020851015610331578190505b61034561033d856101f1565b8301826102e4565b50505b505050565b600082821c905092915050565b600061036b6000198460080261034d565b1980831691505092915050565b6000610384838361035a565b9150826002028217905092915050565b61039d82610162565b67ffffffffffffffff8111156103b6576103b561016d565b5b6103c082546101ab565b6103cb828285610307565b600060209050601f8311600181146103fe57600084156103ec578287015190505b6103f68582610378565b86555061045e565b601f19841661040c866101dc565b60005b8281101561043457848901518255600182019150602085019450602081019050610415565b86831015610451578489015161044d601f89168261035a565b8355505b6001600288020188555050505b505050505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b60008160011c9050919050565b6000808291508390505b60018511156104ec578086048111156104c8576104c7610466565b5b60018516156104d75780820291505b80810290506104e585610495565b94506104ac565b94509492505050565b60008261050557600190506105c1565b8161051357600090506105c1565b816001811461052957600281146105335761055c565b60019150506105c1565b60ff84111561054557610544610466565b5b8360020a91508482111561055c5761055b610466565b5b506105c1565b5060208310610133831016604e8410600b84101617156105975782820a90508381111561059257610591610466565b5b6105c1565b6105a484848460016104a2565b925090508184048111156105bb576105ba610466565b5b81810290505b9392505050565b60006105d382610262565b91506105de83610262565b92506105e27f80000000000000000000000000000000000000000000000000000000000000006104f5565b90508281029050919050565b610616806106126000396000f3fe608060405234801561001057600080fd5b50600436106100885760003560e01c806370a082311161005b57806370a08231146101145780638da5cb5b1461014457806395d89b4114610162578063a9059cbb1461018057610088565b806306fdde031461008d578063095ea7b3146100ab57806318160ddd146100db57806323b872dd146100f9575b600080fd5b6100956101b0565b6040516100a29190610452565b60405180910390f35b6100c560048036038101906100c091906104fd565b610242565b6040516100d29190610558565b60405180910390f35b6100e3610334565b6040516100f09190610582565b60405180910390f35b610113600480360381019061010e919061059d565b61033e565b005b61012e600480360381019061012991906105f0565b6103ad565b60405161013b9190610582565b60405180910390f35b61014c6103f5565b604051610159919061062c565b60405180910390f35b61016a61041b565b6040516101779190610452565b60405180910390f35b61019a600480360381019061019591906104fd565b6104ad565b6040516101a79190610558565b60405180910390f35b6060600380546101bf90610676565b80601f01602080910402602001604051908101604052809291908181526020018280546101eb90610676565b80156102385780601f1061020d57610100808354040283529160200191610238565b820191906000526020600020905b81548152906001019060200180831161021b57829003601f168201915b5050505050905090565b60008061024d6104c2565b905060006001600160a01b0316600084815260208082526040808320928854845294849052919092205403925080158015906102885750828210155b61029157600080fd5b81600160008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508273ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925846040516103269190610582565b60405180910390a350600192915050565b6000600054905090565b6000806103496104c2565b9050600160008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054831115806103d55750600181105b156103df57600080fd5b6103ea8585856104ca565b819250505050505050565b600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60606004805461042a90610676565b80601f016020809104026020016040519081016040528092919081815260200182805461045690610676565b80156104a35780601f10610478576101008083540402835291602001916104a3565b820191906000526020600020905b81548152906001019060200180831161048657829003601f168201915b5050505050905090565b60006104ba3384846104ca565b905092915050565b600033905090565b60008273ffffffffffffffffffffffffffffffffffffffff16600160008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054101561052857600080fd5b81600160008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825461057691906106a7565b9250508190555081600160008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282546105cb91906106db565b925050819055508173ffffffffffffffffffffffffffffffffffffffff168373ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef8360405161062f9190610582565b60405180910390a3600190509392505050565b600081519050919050565b600082825260208201905092915050565b60005b8381101561067c578082015181840152602081019050610661565b60008484015250505050565b6000601f19601f8301169050919050565b60006106a482610642565b6106ae818561064d565b93506106be81856020860161065e565b6106c781610688565b840191505092915050565b600060208201905081810360008301526106ec8184610699565b905092915050565b600080fd5b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000610724826106f9565b9050919050565b61073481610719565b811461073f57600080fd5b50565b6000813590506107518161072b565b92915050565b6000819050919050565b61076a81610757565b811461077557600080fd5b50565b60008135905061078781610761565b92915050565b600080604083850312156107a4576107a36106f4565b5b60006107b285828601610742565b92505060206107c385828601610778565b9150509250929050565b60008115159050919050565b6107e2816107cd565b82525050565b60006020820190506107fd60008301846107d9565b92915050565b61080c81610757565b82525050565b60006020820190506108276000830184610803565b92915050565b600080600060608486031215610846576108456106f4565b5b600061085486828701610742565b935050602061086586828701610742565b925050604061087686828701610778565b9150509250925092565b60006020828403121561089657610895610706a742565b92915050565b6108a581610719565b82525050565b60006020820190506108c0600083018461089c565b92915050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b6000600282049050600182168061090e57607f821691505b602082108103610921576109206108c7565b5b50919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b600061096182610757565b915061096c83610757565b925082820390508181111561098457610983610927565b5b92915050565b600061099582610757565b91506109a083610757565b92508282019050808211156109b8576109b7610927565b5b9291505056fea2646970667358221220d4f4e0a8a4f29e7d8c9c4e9a3a2a1e9b8b4e8e7a5d8c6e9f1a3b5c2d7e8f94a63"

def get_private_key():
    """Get private key from environment variables"""
    # Try different possible environment variable names
    private_key = os.getenv('WALLET_PRIVATE_KEY') or os.getenv('PRIVATE_KEY') or os.getenv('ETH_PRIVATE_KEY')
    
    if not private_key:
        raise ValueError("No private key found in environment variables. Please set WALLET_PRIVATE_KEY, PRIVATE_KEY, or ETH_PRIVATE_KEY")
    
    return private_key

def deploy_hype_token():
    """Deploy HYPE token to HyperEVM network"""
    
    print("🚀 HYPE Token Deployment Starting...")
    print("=" * 50)
    
    # Get private key
    private_key = get_private_key()
    if not private_key.startswith('0x'):
        private_key = '0x' + private_key
    
    # Create account from private key
    account = Account.from_key(private_key)
    wallet_address = account.address
    
    print(f"🔑 Deployer Wallet: {wallet_address}")
    
    # Connect to HyperEVM
    print(f"🌐 Connecting to HyperEVM: {HYPEREVM_RPC_URL}")
    w3 = Web3(Web3.HTTPProvider(HYPEREVM_RPC_URL))
    
    # Check connection
    if not w3.is_connected():
        print("❌ Failed to connect to HyperEVM network")
        return None
    
    print("✅ Connected to HyperEVM successfully")
    
    # Get nonce
    nonce = w3.eth.get_transaction_count(wallet_address)
    print(f"📝 Current nonce: {nonce}")
    
    # Get gas price
    try:
        gas_price = w3.eth.gas_price
        print(f"⛽ Gas price: {gas_price} wei")
    except:
        gas_price = w3.to_wei('20', 'gwei')
        print(f"⛽ Using default gas price: {gas_price} wei")
    
    # Create contract
    contract = w3.eth.contract(abi=CONTRACT_ABI, bytecode=CONTRACT_BYTECODE)
    
    # Build transaction
    transaction = contract.constructor().build_transaction({
        'chainId': CHAIN_ID,
        'gas': 2000000,
        'gasPrice': gas_price,
        'nonce': nonce,
    })
    
    print(f"📋 Transaction built: {transaction['gas']} gas units")
    
    # Sign transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    
    print("✍️  Transaction signed")
    
    # Send transaction
    print("📤 Sending deployment transaction...")
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
    print(f"⏳ Transaction hash: {tx_hash.hex()}")
    print("⏳ Waiting for confirmation...")
    
    # Wait for transaction receipt
    try:
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
        
        if tx_receipt.status == 1:
            print("✅ HYPE Token deployed successfully!")
            contract_address = tx_receipt.contractAddress
            block_number = tx_receipt.blockNumber
            gas_used = tx_receipt.gasUsed
            
            print("=" * 50)
            print("🎉 HYPE TOKEN DEPLOYMENT SUCCESSFUL!")
            print("=" * 50)
            print(f"📄 Contract Address: {contract_address}")
            print(f"🔗 Transaction Hash: {tx_hash.hex()}")
            print(f"📦 Block Number: {block_number}")
            print(f"⛽ Gas Used: {gas_used:,}")
            print(f"💎 Token Name: {TOKEN_CONFIG['name']}")
            print(f"🏷️  Token Symbol: {TOKEN_CONFIG['symbol']}")
            print(f"🔢 Decimals: {TOKEN_CONFIG['decimals']}")
            print(f"🏭 Total Supply: {TOKEN_CONFIG['initial_supply']:,} {TOKEN_CONFIG['symbol']}")
            print(f"👤 Owner: {wallet_address}")
            print("=" * 50)
            
            # Get deployed contract instance
            deployed_contract = w3.eth.contract(address=contract_address, abi=CONTRACT_ABI)
            
            # Verify deployment by calling contract functions
            try:
                name = deployed_contract.functions.name().call()
                symbol = deployed_contract.functions.symbol().call()
                decimals = deployed_contract.functions.decimals().call()
                total_supply = deployed_contract.functions.totalSupply().call()
                owner_balance = deployed_contract.functions.balanceOf(wallet_address).call()
                
                print("🔍 Contract Verification:")
                print(f"✅ Name: {name}")
                print(f"✅ Symbol: {symbol}")
                print(f"✅ Decimals: {decimals}")
                print(f"✅ Total Supply: {total_supply / 10**decimals:,.0f} {symbol}")
                print(f"✅ Owner Balance: {owner_balance / 10**decimals:,.0f} {symbol}")
                print("=" * 50)
                
            except Exception as e:
                print(f"⚠️  Contract verification failed: {e}")
            
            return {
                'success': True,
                'contract_address': contract_address,
                'transaction_hash': tx_hash.hex(),
                'block_number': block_number,
                'gas_used': gas_used,
                'wallet_address': wallet_address,
                'token_config': TOKEN_CONFIG
            }
            
        else:
            print("❌ Transaction failed!")
            return None
            
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return None

if __name__ == "__main__":
    result = deploy_hype_token()
    if result:
        print("\n🎉 Deployment completed successfully!")
        print(f"📄 Contract Address: {result['contract_address']}")
        print(f"🔗 Add to your wallet using this address!")
    else:
        print("\n❌ Deployment failed. Please check the logs above.")