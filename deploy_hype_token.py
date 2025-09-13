#!/usr/bin/env python3
"""
Direct HYPE Token Deployment using raw transaction construction
Real deployment to HyperEVM Chain 999 with your wallet and private key
"""

import json
import subprocess
import binascii
from datetime import datetime

# Your credentials for HyperEVM deployment
WALLET_ADDRESS = "0xbfc06de2711abee4d1d9f370cde09773ddde7048"
PRIVATE_KEY = "0xf3d94b527f5aad6770cbd8d9b3bf7963de26be956b683c25b07f5a02db4096d3"

# HyperEVM Network Details
CHAIN_ID = 999
RPC_ENDPOINTS = [
    "https://api.hyperevm.org",
    "https://rpc.hyperevm.org", 
    "https://mainnet.hyperevm.org"
]

# HYPE Token Bytecode
CONTRACT_BYTECODE = "0x608060405234801561001057600080fd5b506040518060400160405280600a81526020017f4859504520546f6b656e000000000000000000000000000000000000000000008152506040518060400160405280600481526020017f48595045000000000000000000000000000000000000000000000000000000008152508160039081610089919061031a565b50806004908161009991906103e1565b505050600560009054906101000a900460ff1660ff16600a6100bb91906104c8565b633b9aca006100ca9190610552565b60008190555060005460016000336001600160a01b031681526020019081526020016000208190555033600260006101000a8154816001600160a01b0302191690836001600160a01b031602179055506001600560006101000a81548160ff021916908360ff16021790555060018060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002081905550610603565b600081519050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b600060028204905060018216806101c357607f821691505b6020821081036101d6576101d561019c565b5b50919050565b60008190508160005260206000209050919050565b60006020601f8301049050919050565b600082821b905092915050565b6000600883026102407fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff82610203565b61024a8683610203565b95508019841693508086168417925050509392505050565b6000819050919050565b6000819050919050565b600061029161028c61028784610262565b61026c565b610262565b9050919050565b6000819050919050565b6102ab83610276565b6102bf6102b782610298565b848454610210565b825550505050565b600090565b6102d46102c7565b6102df8184846102a2565b505050565b5b81811015610303576102f86000826102cc565b6001810190506102e5565b5050565b601f82111561034857610319816101dc565b610322846101f1565b81016020851015610331578190505b61034561033d856101f1565b8301826102e4565b50505b505050565b600082821c905092915050565b600061036b6000198460080261034d565b1980831691505092915050565b6000610384838361035a565b9150826002028217905092915050565b61039d82610162565b67ffffffffffffffff8111156103b6576103b561016d565b5b6103c082546101ab5b6103cb828285610307565b600060209050601f8311600181146103fe57600084156103ec578287015190505b6103f68582610378565b86555061045e565b601f19841661040c866101dc565b60005b8281101561043457848901518255600182019150602085019450602081019050610415565b86831015610451578489015161044d601f89168261035a565b8355505b6001600288020188555050505b505050505050"

def make_rpc_call(rpc_url, method, params=None):
    """Make RPC call to blockchain"""
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
            rpc_url
        ], capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            response = json.loads(result.stdout)
            if 'result' in response:
                return response['result']
            elif 'error' in response:
                print(f"RPC Error: {response['error']}")
        return None
    except Exception as e:
        print(f"RPC failed: {e}")
        return None

def find_working_rpc():
    """Find working HyperEVM RPC endpoint"""
    print("Finding working HyperEVM RPC endpoint...")
    
    for rpc_url in RPC_ENDPOINTS:
        print(f"Testing {rpc_url}...")
        chain_id = make_rpc_call(rpc_url, "eth_chainId")
        
        if chain_id:
            actual_chain = int(chain_id, 16)
            print(f"Connected to chain {actual_chain}")
            
            if actual_chain == CHAIN_ID:
                print(f"✅ Found working HyperEVM RPC: {rpc_url}")
                return rpc_url
            else:
                print(f"Wrong chain ID: expected {CHAIN_ID}, got {actual_chain}")
        else:
            print("No response")
    
    print("⚠️  No working RPC found - will attempt deployment anyway")
    return RPC_ENDPOINTS[0]

def deploy_hype_token():
    """Deploy HYPE token to HyperEVM"""
    
    print("🚀 HYPE Token Deployment to HyperEVM Mainnet")
    print("=" * 70)
    print(f"Target Chain: HyperEVM (Chain ID {CHAIN_ID})")
    print(f"Deployer: {WALLET_ADDRESS}")
    print(f"Token: HYPE (1 billion supply)")
    print("=" * 70)
    
    # Find working RPC
    rpc_url = find_working_rpc()
    
    # Check wallet balance
    print(f"Checking wallet balance...")
    balance = make_rpc_call(rpc_url, "eth_getBalance", [WALLET_ADDRESS, "latest"])
    
    if balance:
        balance_wei = int(balance, 16)
        balance_hype = balance_wei / 10**18
        print(f"💰 Balance: {balance_hype:.6f} HYPE")
        
        if balance_wei == 0:
            print("❌ No HYPE balance for gas fees")
            return create_manual_deployment_plan()
    else:
        print("⚠️  Cannot verify balance")
    
    # Get transaction data
    print("Getting network state...")
    nonce = make_rpc_call(rpc_url, "eth_getTransactionCount", [WALLET_ADDRESS, "latest"])
    gas_price = make_rpc_call(rpc_url, "eth_gasPrice")
    
    if nonce:
        nonce_int = int(nonce, 16)
        print(f"📝 Nonce: {nonce_int}")
    else:
        nonce_int = 0
        print("Using default nonce: 0")
    
    if gas_price:
        gas_price_int = int(gas_price, 16)
        gas_price_gwei = gas_price_int / 10**9
        print(f"⛽ Gas Price: {gas_price_gwei:.2f} Gwei")
    else:
        gas_price_int = 20_000_000_000  # 20 Gwei
        print("Using default gas price: 20 Gwei")
    
    # Estimate cost
    gas_limit = 2_000_000
    total_cost = gas_limit * gas_price_int
    cost_hype = total_cost / 10**18
    
    print(f"📊 Deployment cost estimate: {cost_hype:.6f} HYPE")
    
    # Create deployment transaction using curl + ethers
    print("Creating deployment transaction...")
    
    deploy_script = f"""
const {{ ethers }} = require('ethers');

async function deployDirect() {{
    console.log('Creating direct deployment transaction...');
    
    // Create provider without auto-detection
    const provider = new ethers.providers.StaticJsonRpcProvider({{
        url: '{rpc_url}',
        network: {{
            name: 'hyperevm',
            chainId: {CHAIN_ID}
        }}
    }});
    
    const wallet = new ethers.Wallet('{PRIVATE_KEY}', provider);
    console.log('Wallet:', wallet.address);
    
    try {{
        // Manual transaction construction
        const tx = {{
            data: '{CONTRACT_BYTECODE}',
            gasLimit: {gas_limit},
            gasPrice: {gas_price_int},
            nonce: {nonce_int},
            chainId: {CHAIN_ID}
        }};
        
        console.log('Sending deployment transaction...');
        const response = await wallet.sendTransaction(tx);
        
        console.log('Transaction Hash:', response.hash);
        console.log('Waiting for confirmation...');
        
        const receipt = await response.wait();
        
        console.log('✅ DEPLOYMENT SUCCESSFUL!');
        console.log('Contract Address:', receipt.contractAddress);
        console.log('Block Number:', receipt.blockNumber);
        console.log('Gas Used:', receipt.gasUsed.toString());
        
        // Save deployment data
        const deploymentData = {{
            contract_address: receipt.contractAddress,
            transaction_hash: receipt.transactionHash,
            block_number: receipt.blockNumber,
            gas_used: receipt.gasUsed.toString(),
            deployer: wallet.address,
            network: 'HyperEVM',
            chain_id: {CHAIN_ID},
            rpc_url: '{rpc_url}',
            token_name: 'HYPE Token',
            token_symbol: 'HYPE',
            total_supply: 1000000000,
            deployment_date: new Date().toISOString(),
            deployment_type: 'direct_hyperevm',
            confirmed: true
        }};
        
        require('fs').writeFileSync('hyperevm_deployment_success.json', JSON.stringify(deploymentData, null, 2));
        console.log('Deployment data saved!');
        
    }} catch (error) {{
        console.log('Deployment error:', error.message);
        
        if (error.code === 'INSUFFICIENT_FUNDS') {{
            console.log('Need more HYPE for gas fees');
        }} else if (error.code === 'NONCE_EXPIRED') {{
            console.log('Nonce issue - transaction may have been processed');
        }} else {{
            console.log('Full error:', error);
        }}
    }}
}}

deployDirect().catch(console.error);
"""
    
    with open('direct_deploy.js', 'w') as f:
        f.write(deploy_script)
    
    print("🔐 Executing deployment...")
    try:
        result = subprocess.run(['node', 'direct_deploy.js'], capture_output=True, text=True, timeout=180)
        
        print("Deployment output:")
        print(result.stdout)
        
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        # Check for success
        try:
            with open('hyperevm_deployment_success.json', 'r') as f:
                deployment_data = json.load(f)
            
            print("\n🎉 HYPE TOKEN SUCCESSFULLY DEPLOYED!")
            print("=" * 70)
            print(f"📄 Contract Address: {deployment_data['contract_address']}")
            print(f"🔗 Transaction Hash: {deployment_data['transaction_hash']}")
            print(f"📦 Block Number: {deployment_data['block_number']:,}")
            print(f"⛽ Gas Used: {deployment_data['gas_used']:,}")
            print(f"🌐 Network: {deployment_data['network']} (Chain {deployment_data['chain_id']})")
            print(f"👤 Owner: {deployment_data['deployer']}")
            print(f"💎 Total Supply: {deployment_data['total_supply']:,} HYPE")
            print(f"🕒 Deployed: {deployment_data['deployment_date']}")
            print("=" * 70)
            print("✅ Your HYPE token is now live on HyperEVM mainnet!")
            
            return deployment_data
            
        except FileNotFoundError:
            print("❌ Deployment may have failed - check output above")
            return {"status": "attempted", "output": result.stdout}
            
    except subprocess.TimeoutExpired:
        print("⏰ Deployment timeout - transaction may still be processing")
        return {"status": "timeout"}
    except Exception as e:
        print(f"Deployment execution error: {e}")
        return create_manual_deployment_plan()

def create_manual_deployment_plan():
    """Create manual deployment instructions"""
    
    plan = {
        "deployment_required": "Manual deployment using external tools",
        "target_network": f"HyperEVM Mainnet (Chain ID {CHAIN_ID})",
        "wallet_address": WALLET_ADDRESS,
        "private_key": PRIVATE_KEY,
        "contract_bytecode": CONTRACT_BYTECODE,
        "token_details": {
            "name": "HYPE Token",
            "symbol": "HYPE",
            "decimals": 18,
            "total_supply": 1000000000
        },
        "rpc_endpoints": RPC_ENDPOINTS,
        "deployment_options": [
            {
                "method": "Remix IDE",
                "url": "https://remix.ethereum.org",
                "instructions": [
                    "1. Add HyperEVM network to MetaMask",
                    "2. Import your private key to MetaMask",
                    "3. Create HYPE.sol file in Remix",
                    "4. Compile and deploy the contract",
                    "5. Confirm transaction with HYPE gas"
                ]
            },
            {
                "method": "Command Line",
                "script": "direct_deploy.js",
                "command": "node direct_deploy.js"
            }
        ],
        "estimated_gas_cost": "0.02-0.05 HYPE",
        "timestamp": int(datetime.now().timestamp()),
        "date": datetime.now().isoformat()
    }
    
    with open('deployment_plan.json', 'w') as f:
        json.dump(plan, f, indent=2)
    
    print("📋 Manual deployment plan created")
    print("Use Remix IDE or the generated script for deployment")
    
    return plan

if __name__ == "__main__":
    print("🎯 HyperEVM HYPE Token Live Deployment")
    print(f"Wallet: {WALLET_ADDRESS}")
    print(f"Target: Chain {CHAIN_ID}")
    
    result = deploy_hype_token()
    
    if result and result.get('contract_address'):
        print(f"\n🎉 SUCCESS! HYPE token deployed at: {result['contract_address']}")
        print("Your token is now live on HyperEVM mainnet!")
    elif result and result.get('status') == 'attempted':
        print("\n✅ Deployment attempted - check results above")
    else:
        print("\n📋 Use manual deployment methods if needed")