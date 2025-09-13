#!/usr/bin/env python3
"""
Direct HYPE Token Deployment to HyperEVM using curl/subprocess
Real deployment without web3 dependency issues
"""

import json
import subprocess
import time
from datetime import datetime

# Your credentials
WALLET_ADDRESS = "0xbfc06de2711abee4d1d9f370cde09773ddde7048"
PRIVATE_KEY = "0xf3d94b527f5aad6770cbd8d9b3bf7963de26be956b683c25b07f5a02db4096d3"

# HyperEVM configuration
RPC_URL = "https://api.hyperevm.org"
CHAIN_ID = 999

def make_rpc_call(method, params=None):
    """Make RPC call using curl"""
    if params is None:
        params = []
    
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }
    
    try:
        result = subprocess.run([
            'curl', '-s', '-X', 'POST', 
            '-H', 'Content-Type: application/json',
            '-d', json.dumps(payload),
            RPC_URL
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            response = json.loads(result.stdout)
            return response.get('result')
        return None
    except Exception as e:
        print(f"RPC call failed: {e}")
        return None

def check_hyperevm_connection():
    """Test connection to HyperEVM"""
    print("Testing HyperEVM connection...")
    
    chain_id = make_rpc_call("eth_chainId")
    if chain_id:
        actual_chain = int(chain_id, 16)
        print(f"Connected to Chain ID: {actual_chain}")
        return actual_chain == CHAIN_ID
    
    print("Failed to connect to HyperEVM")
    return False

def check_wallet_balance():
    """Check wallet balance on HyperEVM"""
    print(f"Checking balance for {WALLET_ADDRESS}...")
    
    balance_hex = make_rpc_call("eth_getBalance", [WALLET_ADDRESS, "latest"])
    if balance_hex:
        balance_wei = int(balance_hex, 16)
        balance_hype = balance_wei / 10**18
        print(f"Balance: {balance_hype:.6f} HYPE")
        return balance_wei
    
    print("Failed to get balance")
    return 0

def get_gas_price():
    """Get current gas price"""
    gas_price_hex = make_rpc_call("eth_gasPrice")
    if gas_price_hex:
        return int(gas_price_hex, 16)
    return 20_000_000_000  # 20 Gwei fallback

def get_nonce():
    """Get transaction nonce"""
    nonce_hex = make_rpc_call("eth_getTransactionCount", [WALLET_ADDRESS, "latest"])
    if nonce_hex:
        return int(nonce_hex, 16)
    return 0

def deploy_with_foundry():
    """Deploy using Foundry if available"""
    print("Attempting deployment with Foundry...")
    
    # Check if foundry is available
    try:
        subprocess.run(['forge', '--version'], capture_output=True, check=True)
        print("Foundry detected")
        
        # Create minimal contract file
        contract_code = '''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract HYPE {
    string public name = "HYPE Token";
    string public symbol = "HYPE";
    uint8 public decimals = 18;
    uint256 public totalSupply = 1000000000 * 10**18;
    
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    
    address public owner;
    
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    
    constructor() {
        owner = msg.sender;
        balanceOf[msg.sender] = totalSupply;
        emit Transfer(address(0), msg.sender, totalSupply);
    }
    
    function transfer(address to, uint256 value) public returns (bool) {
        require(balanceOf[msg.sender] >= value, "Insufficient balance");
        balanceOf[msg.sender] -= value;
        balanceOf[to] += value;
        emit Transfer(msg.sender, to, value);
        return true;
    }
    
    function approve(address spender, uint256 value) public returns (bool) {
        allowance[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }
    
    function transferFrom(address from, address to, uint256 value) public returns (bool) {
        require(balanceOf[from] >= value, "Insufficient balance");
        require(allowance[from][msg.sender] >= value, "Insufficient allowance");
        
        balanceOf[from] -= value;
        balanceOf[to] += value;
        allowance[from][msg.sender] -= value;
        
        emit Transfer(from, to, value);
        return true;
    }
}'''
        
        with open('HYPE.sol', 'w') as f:
            f.write(contract_code)
        
        # Deploy with foundry
        result = subprocess.run([
            'forge', 'create', 'HYPE.sol:HYPE',
            '--rpc-url', RPC_URL,
            '--private-key', PRIVATE_KEY,
            '--chain-id', str(CHAIN_ID)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Foundry deployment successful!")
            print(result.stdout)
            return True
        else:
            print(f"Foundry deployment failed: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError:
        print("Foundry not available")
        return False

def deploy_hype_token():
    """Main deployment function"""
    
    print("🚀 Direct HYPE Token Deployment to HyperEVM")
    print("=" * 60)
    print(f"Network: HyperEVM Mainnet (Chain ID: {CHAIN_ID})")
    print(f"RPC: {RPC_URL}")
    print(f"Wallet: {WALLET_ADDRESS}")
    print("=" * 60)
    
    # Check connection
    if not check_hyperevm_connection():
        print("Cannot connect to HyperEVM - creating deployment plan")
        return create_deployment_plan()
    
    # Check balance
    balance = check_wallet_balance()
    if balance == 0:
        print("No HYPE balance for gas fees")
        return create_deployment_plan()
    
    # Get network data
    gas_price = get_gas_price()
    nonce = get_nonce()
    
    print(f"Gas price: {gas_price / 10**9:.2f} Gwei")
    print(f"Nonce: {nonce}")
    
    # Estimate cost
    gas_limit = 2_000_000
    total_cost = gas_limit * gas_price
    cost_hype = total_cost / 10**18
    
    print(f"Estimated cost: {cost_hype:.6f} HYPE")
    
    if total_cost > balance:
        print("Insufficient balance for deployment")
        return create_deployment_plan()
    
    # Try foundry deployment
    if deploy_with_foundry():
        return create_success_record()
    
    print("Direct deployment requires additional tools")
    return create_deployment_plan()

def create_success_record():
    """Create deployment success record"""
    timestamp = int(time.time())
    
    deployment_info = {
        "status": "deployment_attempted",
        "method": "foundry_direct",
        "wallet": WALLET_ADDRESS,
        "network": f"HyperEVM (Chain ID: {CHAIN_ID})",
        "rpc_url": RPC_URL,
        "timestamp": timestamp,
        "date": datetime.now().isoformat(),
        "token_name": "HYPE Token",
        "token_symbol": "HYPE",
        "total_supply": 1000000000,
        "note": "Deployment attempted with foundry - check output for results"
    }
    
    with open('direct_deployment_attempt.json', 'w') as f:
        json.dump(deployment_info, f, indent=2)
    
    return deployment_info

def create_deployment_plan():
    """Create deployment plan when direct deployment not possible"""
    
    print("Creating deployment execution plan...")
    
    plan = {
        "deployment_plan": "HyperEVM HYPE Token Deployment",
        "wallet": WALLET_ADDRESS,
        "private_key": PRIVATE_KEY,
        "network": {
            "name": "HyperEVM Mainnet",
            "chain_id": CHAIN_ID,
            "rpc_url": RPC_URL,
            "currency": "HYPE"
        },
        "recommended_methods": [
            {
                "method": "Remix IDE",
                "url": "https://remix.ethereum.org",
                "steps": [
                    "Add HyperEVM network to MetaMask",
                    "Import wallet with private key",
                    "Create HYPE.sol contract file",
                    "Compile and deploy"
                ]
            },
            {
                "method": "Foundry",
                "command": f"forge create HYPE.sol:HYPE --rpc-url {RPC_URL} --private-key {PRIVATE_KEY} --chain-id {CHAIN_ID}"
            },
            {
                "method": "Hardhat",
                "setup": "npm install hardhat @nomiclabs/hardhat-ethers ethers",
                "deploy": "npx hardhat run scripts/deploy.js --network hyperevm"
            }
        ],
        "contract_code_file": "HYPE.sol",
        "estimated_gas_cost": "0.02-0.05 HYPE",
        "timestamp": int(time.time()),
        "date": datetime.now().isoformat()
    }
    
    with open('hyperevm_deployment_plan.json', 'w') as f:
        json.dump(plan, f, indent=2)
    
    print("✅ Deployment plan created")
    print(f"📄 Plan saved to: hyperevm_deployment_plan.json")
    print("🔧 Use recommended deployment methods for live deployment")
    
    return plan

if __name__ == "__main__":
    print("🎯 Direct HyperEVM Deployment Process")
    print(f"Target: {WALLET_ADDRESS} on HyperEVM Chain {CHAIN_ID}")
    
    result = deploy_hype_token()
    
    if result:
        print("✅ Deployment process completed")
        if result.get('status') == 'deployment_attempted':
            print("🚀 Live deployment attempted - check results")
        else:
            print("📋 Deployment plan ready for execution")
    else:
        print("❌ Deployment process failed")