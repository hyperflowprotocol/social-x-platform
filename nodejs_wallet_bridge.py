#!/usr/bin/env python3
"""
Node.js Bridge for Ethereum Wallet Generation
Bypasses Python dependency issues by using Node.js ethers.js
"""

import subprocess
import json
import os

class NodeJSWalletBridge:
    def __init__(self):
        self.node_script = 'ethereum_wallet_node.js'
    
    def generate_compatible_wallet(self):
        """Generate wallet using Node.js ethers.js - bypasses Python dependency issues"""
        try:
            # Run Node.js script to generate wallet
            result = subprocess.run(
                ['node', self.node_script, 'generate'],
                capture_output=True,
                text=True,
                cwd='/home/runner/workspace'
            )
            
            if result.returncode == 0:
                wallet_data = json.loads(result.stdout.strip())
                print(f"✅ Generated compatible wallet: {wallet_data['address']}")
                return wallet_data
            else:
                print(f"❌ Node.js wallet generation failed: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Error calling Node.js wallet generator: {e}")
            return None
    
    def verify_private_key(self, private_key):
        """Verify private key generates expected address"""
        try:
            result = subprocess.run(
                ['node', self.node_script, 'verify', private_key],
                capture_output=True,
                text=True,
                cwd='/home/runner/workspace'
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Error: {result.stderr}"
                
        except Exception as e:
            return f"Error: {e}"
    
    def deploy_contract(self, private_key, contract_bytecode, rpc_url, chain_id, account_handle):
        """Deploy contract using Node.js ethers.js for proper signing"""
        try:
            print(f"🔄 Node.js ethers.js contract deployment starting...")
            
            # Create Node.js script for contract deployment
            script = f'''
const ethers = require('ethers');

async function deployContract() {{
    try {{
        // Connect to provider
        const provider = new ethers.providers.JsonRpcProvider("{rpc_url}");
        
        // Create wallet from private key
        const wallet = new ethers.Wallet("{private_key}", provider);
        
        // Check balance
        const balance = await wallet.getBalance();
        console.log("Wallet balance: " + ethers.utils.formatEther(balance) + " HYPE");
        
        // Simple contract factory (basic ERC20-like)
        const contractFactory = new ethers.ContractFactory(
            [], // ABI (empty for now)
            "{contract_bytecode}", // Bytecode
            wallet
        );
        
        // Deploy with gas settings
        console.log("🚀 Deploying contract...");
        const contract = await contractFactory.deploy({{
            gasLimit: 800000,
            gasPrice: ethers.utils.parseUnits("5", "gwei")
        }});
        
        console.log("⏳ Waiting for deployment...");
        await contract.deployed();
        
        const deploymentInfo = {{
            "success": true,
            "contract_address": contract.address,
            "transaction_hash": contract.deployTransaction.hash,
            "block_number": contract.deployTransaction.blockNumber || 0,
            "deployer": wallet.address,
            "gas_used": contract.deployTransaction.gasLimit.toString(),
            "network": "HyperEVM Mainnet",
            "chain_id": {chain_id}
        }};
        
        console.log(JSON.stringify(deploymentInfo));
        
    }} catch (error) {{
        const errorInfo = {{
            "success": false,
            "error": error.message,
            "code": error.code || "UNKNOWN_ERROR"
        }};
        console.log(JSON.stringify(errorInfo));
    }}
}}

deployContract();
'''

            # Write to temporary file
            with open('temp_deploy.js', 'w') as f:
                f.write(script)
            
            # Execute Node.js script with timeout
            result = subprocess.run(['node', 'temp_deploy.js'], 
                                    capture_output=True, text=True, timeout=60)
            
            # Clean up
            os.remove('temp_deploy.js')
            
            if result.returncode == 0:
                # Parse the last JSON output (deployment result)
                lines = result.stdout.strip().split('\n')
                for line in reversed(lines):
                    if line.strip().startswith('{'):
                        try:
                            deployment_data = json.loads(line.strip())
                            if deployment_data.get('success'):
                                print(f"✅ ethers.js deployment successful: {deployment_data['contract_address']}")
                            else:
                                print(f"❌ ethers.js deployment failed: {deployment_data['error']}")
                            return deployment_data
                        except json.JSONDecodeError:
                            continue
                
                # Fallback if no JSON found
                return {'success': False, 'error': 'No deployment result found'}
            else:
                print(f"❌ Node.js deployment failed: {result.stderr}")
                return {'success': False, 'error': result.stderr}
            
        except Exception as e:
            print(f"❌ Deployment bridge error: {e}")
            return {'success': False, 'error': str(e)}

def test_nodejs_bridge():
    """Test the Node.js bridge"""
    print("Testing Node.js Wallet Bridge")
    print("=" * 50)
    
    bridge = NodeJSWalletBridge()
    
    # Generate test wallet
    wallet = bridge.generate_compatible_wallet()
    
    if wallet:
        print(f"Address: {wallet['address']}")
        print(f"Private Key: {wallet['privateKey']}")
        print(f"Compatible: {wallet['compatible']}")
        print("Compatible with:", ', '.join(wallet['compatible_with']))
        
        # Verify the private key generates same address
        print("\nVerifying private key compatibility...")
        verification = bridge.verify_private_key(wallet['privateKey'])
        print(verification)
        
    return wallet

if __name__ == "__main__":
    test_nodejs_bridge()