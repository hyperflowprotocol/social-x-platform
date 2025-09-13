#!/usr/bin/env python3
"""
Real HYPE Token Deployment Script
Actually deploys HYPE token to HyperEVM blockchain using your wallet
"""

import os
import json
import time
from web3 import Web3
from eth_account import Account
from datetime import datetime

# Your actual wallet credentials
WALLET_ADDRESS = "0xbfc06de2711abee4d1d9f370cde09773ddde7048"
PRIVATE_KEY = "0xf3d94b527f5aad6770cbd8d9b3bf7963de26be956b683c25b07f5a02db4096d3"

# HyperEVM Network Configuration
NETWORKS = {
    "hyperliquid_testnet": {
        "rpc_url": "https://api.hyperliquid-testnet.xyz/evm",
        "chain_id": 998899,
        "name": "Hyperliquid Testnet"
    },
    "hyperevm_mainnet": {
        "rpc_url": "https://api.hyperliquid.xyz/evm", 
        "chain_id": 42161,
        "name": "HyperEVM Mainnet"
    }
}

# HYPE Token Smart Contract (Solidity bytecode)
HYPE_CONTRACT_BYTECODE = "0x608060405234801561001057600080fd5b506040518060400160405280600a81526020017f4859504520546f6b656e000000000000000000000000000000000000000000008152506040518060400160405280600481526020017f48595045000000000000000000000000000000000000000000000000000000008152508160039081610089919061031a565b50806004908161009991906103e1565b505050600560009054906101000a900460ff1660ff16600a6100bb91906104c8565b633b9aca006100ca9190610552565b60008190555060005460016000336001600160a01b031681526020019081526020016000208190555033600260006101000a8154816001600160a01b0302191690836001600160a01b031602179055506001600560006101000a81548160ff021916908360ff16021790555060018060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002081905550610603565b600081519050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b600060028204905060018216806101c357607f821691505b6020821081036101d6576101d561019c565b5b50919050565b60008190508160005260206000209050919050565b60006020601f8301049050919050565b600082821b905092915050565b6000600883026102407fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff82610203565b61024a8683610203565b95508019841693508086168417925050509392505050565b6000819050919050565b6000819050919050565b600061029161028c61028784610262565b61026c565b610262565b9050919050565b6000819050919050565b6102ab83610276565b6102bf6102b782610298565b848454610210565b825550505050565b600090565b6102d46102c7565b6102df8184846102a2565b505050565b5b81811015610303576102f86000826102cc565b6001810190506102e5565b5050565b601f82111561034857610319816101dc565b610322846101f1565b81016020851015610331578190505b61034561033d856101f1565b8301826102e4565b50505b505050565b600082821c905092915050565b600061036b6000198460080261034d565b1980831691505092915050565b6000610384838361035a565b9150826002028217905092915050565b61039d82610162565b67ffffffffffffffff8111156103b6576103b561016d565b5b6103c082546101ab565b6103cb828285610307565b600060209050601f8311600181146103fe57600084156103ec578287015190505b6103f68582610378565b86555061045e565b601f19841661040c866101dc565b60005b8281101561043457848901518255600182019150602085019450602081019050610415565b86831015610451578489015161044d601f89168261035a565b8355505b6001600288020188555050505b505050505050"

def real_deploy_hype_token(network="hyperliquid_testnet"):
    """Deploy HYPE token to actual blockchain"""
    
    print("🚀 REAL HYPE Token Deployment Starting...")
    print("=" * 60)
    
    # Get network configuration
    network_config = NETWORKS[network]
    print(f"🌐 Network: {network_config['name']}")
    print(f"🔗 RPC URL: {network_config['rpc_url']}")
    print(f"⚡ Chain ID: {network_config['chain_id']}")
    print(f"🔑 Wallet: {WALLET_ADDRESS}")
    
    try:
        # Connect to blockchain
        print("\n📡 Connecting to blockchain...")
        w3 = Web3(Web3.HTTPProvider(network_config['rpc_url']))
        
        if not w3.is_connected():
            print("❌ Failed to connect to blockchain")
            return None
        
        print("✅ Connected to blockchain successfully")
        
        # Verify wallet
        account = Account.from_key(PRIVATE_KEY)
        if account.address.lower() != WALLET_ADDRESS.lower():
            print(f"❌ Private key doesn't match wallet address")
            print(f"   Expected: {WALLET_ADDRESS}")
            print(f"   Got: {account.address}")
            return None
        
        print(f"✅ Wallet verified: {account.address}")
        
        # Check balance
        balance = w3.eth.get_balance(WALLET_ADDRESS)
        balance_eth = w3.from_wei(balance, 'ether')
        print(f"💰 Wallet balance: {balance_eth} ETH")
        
        if balance == 0:
            print("⚠️  Warning: Wallet has 0 ETH balance. You need ETH for gas fees.")
            return None
        
        # Get current nonce
        nonce = w3.eth.get_transaction_count(WALLET_ADDRESS)
        print(f"📝 Current nonce: {nonce}")
        
        # Estimate gas price
        try:
            gas_price = w3.eth.gas_price
            print(f"⛽ Gas price: {w3.from_wei(gas_price, 'gwei')} Gwei")
        except:
            gas_price = w3.to_wei(20, 'gwei')
            print(f"⛽ Using default gas price: 20 Gwei")
        
        # Build deployment transaction
        print("\n📋 Building deployment transaction...")
        
        transaction = {
            'to': None,  # Contract deployment
            'data': HYPE_CONTRACT_BYTECODE,
            'gas': 2000000,  # 2M gas limit
            'gasPrice': gas_price,
            'nonce': nonce,
            'chainId': network_config['chain_id'],
            'value': 0
        }
        
        print(f"   Gas limit: {transaction['gas']:,}")
        print(f"   Gas price: {w3.from_wei(transaction['gasPrice'], 'gwei')} Gwei")
        print(f"   Max cost: {w3.from_wei(transaction['gas'] * transaction['gasPrice'], 'ether')} ETH")
        
        # Sign transaction
        print("\n✍️  Signing transaction...")
        signed_txn = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
        
        # Send transaction
        print("📤 Broadcasting transaction to blockchain...")
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        print(f"🔗 Transaction hash: {tx_hash.hex()}")
        print("⏳ Waiting for confirmation...")
        
        # Wait for receipt
        try:
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
            
            if tx_receipt.status == 1:
                print("✅ Transaction confirmed!")
                
                contract_address = tx_receipt.contractAddress
                block_number = tx_receipt.blockNumber
                gas_used = tx_receipt.gasUsed
                
                print("\n" + "=" * 60)
                print("🎉 HYPE TOKEN DEPLOYED SUCCESSFULLY!")
                print("=" * 60)
                print(f"📄 Contract Address: {contract_address}")
                print(f"🔗 Transaction Hash: {tx_hash.hex()}")
                print(f"📦 Block Number: {block_number:,}")
                print(f"⛽ Gas Used: {gas_used:,}")
                print(f"💰 Gas Cost: {w3.from_wei(gas_used * gas_price, 'ether')} ETH")
                print(f"🌐 Network: {network_config['name']}")
                print(f"👤 Owner: {WALLET_ADDRESS}")
                print(f"🕒 Deployed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
                print("=" * 60)
                
                # Save real deployment info
                deployment_info = {
                    "contract_address": contract_address,
                    "transaction_hash": tx_hash.hex(),
                    "block_number": block_number,
                    "gas_used": gas_used,
                    "gas_price": gas_price,
                    "gas_cost_eth": float(w3.from_wei(gas_used * gas_price, 'ether')),
                    "deployer_wallet": WALLET_ADDRESS,
                    "token_name": "HYPE Token",
                    "token_symbol": "HYPE",
                    "decimals": 18,
                    "total_supply": 1000000000,
                    "chain_id": network_config['chain_id'],
                    "network": network_config['name'],
                    "rpc_url": network_config['rpc_url'],
                    "deployment_timestamp": int(time.time()),
                    "deployment_date": datetime.now().isoformat(),
                    "real_deployment": True
                }
                
                with open('real_hype_deployment.json', 'w') as f:
                    json.dump(deployment_info, f, indent=2)
                
                print(f"📄 Real deployment info saved to: real_hype_deployment.json")
                
                return deployment_info
                
            else:
                print("❌ Transaction failed!")
                return None
                
        except Exception as e:
            print(f"❌ Transaction failed: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return None

def verify_deployment(deployment_info):
    """Verify the deployed contract"""
    
    if not deployment_info:
        return
    
    print("\n🔍 Verifying deployed contract...")
    
    try:
        w3 = Web3(Web3.HTTPProvider(deployment_info['rpc_url']))
        
        # Check if contract exists
        code = w3.eth.get_code(deployment_info['contract_address'])
        
        if len(code) > 0:
            print(f"✅ Contract verified at: {deployment_info['contract_address']}")
            print(f"📏 Contract size: {len(code)} bytes")
        else:
            print(f"❌ No contract found at: {deployment_info['contract_address']}")
            
    except Exception as e:
        print(f"⚠️  Contract verification failed: {e}")

if __name__ == "__main__":
    print("🎯 Starting REAL HYPE Token Deployment")
    print(f"🔑 Your Wallet: {WALLET_ADDRESS}")
    print(f"🔐 Private Key: {PRIVATE_KEY[:10]}...{PRIVATE_KEY[-6:]}")
    print()
    
    # Choose network (testnet for safety)
    network = "hyperliquid_testnet"
    
    # Deploy token
    deployment_info = real_deploy_hype_token(network)
    
    if deployment_info:
        verify_deployment(deployment_info)
        print("\n🎉 REAL HYPE Token deployment completed successfully!")
        print(f"📄 Contract: {deployment_info['contract_address']}")
        print(f"💰 Gas cost: {deployment_info['gas_cost_eth']} ETH")
        print("✅ Your token is now live on the blockchain!")
    else:
        print("\n❌ Real deployment failed")