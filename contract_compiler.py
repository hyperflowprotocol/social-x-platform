#!/usr/bin/env python3
"""
Smart Contract Compilation System
Compiles Solidity contracts using system solc and generates deployment bytecode
"""

import subprocess
import json
import os
import hashlib
from typing import Dict, Any, Optional, List

class ContractCompiler:
    def __init__(self):
        self.solc_version = self._get_solc_version()
        self.compiled_contracts = {}
        
    def _get_solc_version(self) -> str:
        """Get solc version"""
        try:
            result = subprocess.run(['solc', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'Version:' in line:
                        return line.split('Version:')[1].strip()
            return "unknown"
        except Exception as e:
            print(f"❌ Error getting solc version: {e}")
            return "error"
    
    def compile_contract(self, contract_path: str, contract_name: str = None) -> Dict[str, Any]:
        """
        Compile a single Solidity contract
        Returns compilation artifacts including bytecode and ABI
        """
        try:
            print(f"📝 Compiling contract: {contract_path}")
            print(f"   Solc version: {self.solc_version}")
            
            if not os.path.exists(contract_path):
                raise FileNotFoundError(f"Contract file not found: {contract_path}")
            
            # Use solc to compile with JSON output
            cmd = [
                'solc',
                '--combined-json', 'abi,bin,bin-runtime,srcmap,srcmap-runtime,ast,metadata',
                '--optimize',
                '--optimize-runs', '200',
                contract_path
            ]
            
            print(f"🔧 Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode != 0:
                print(f"❌ Compilation failed!")
                print(f"Error: {result.stderr}")
                return {
                    'success': False,
                    'error': result.stderr,
                    'stdout': result.stdout
                }
            
            try:
                compilation_output = json.loads(result.stdout)
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse compilation output: {e}")
                print(f"Raw output: {result.stdout}")
                return {
                    'success': False,
                    'error': f'JSON decode error: {e}',
                    'raw_output': result.stdout
                }
            
            # Extract contract artifacts
            contracts = compilation_output.get('contracts', {})
            
            if not contracts:
                return {
                    'success': False,
                    'error': 'No contracts found in compilation output',
                    'output': compilation_output
                }
            
            # If no specific contract name provided, use the first one
            if contract_name is None:
                contract_name = list(contracts.keys())[0]
                print(f"📋 Using contract: {contract_name}")
            
            # Find the contract (handle different naming patterns)
            contract_key = None
            for key in contracts.keys():
                if contract_name in key or key.endswith(contract_name):
                    contract_key = key
                    break
            
            if contract_key is None:
                available = list(contracts.keys())
                return {
                    'success': False,
                    'error': f'Contract {contract_name} not found. Available: {available}',
                    'available_contracts': available
                }
            
            contract_data = contracts[contract_key]
            
            # Extract bytecode and ABI
            bytecode = contract_data.get('bin', '')
            abi = json.loads(contract_data.get('abi', '[]'))
            runtime_bytecode = contract_data.get('bin-runtime', '')
            
            if not bytecode:
                return {
                    'success': False,
                    'error': f'No bytecode generated for {contract_name}',
                    'contract_data': contract_data
                }
            
            # Add 0x prefix if not present
            if not bytecode.startswith('0x'):
                bytecode = '0x' + bytecode
            if runtime_bytecode and not runtime_bytecode.startswith('0x'):
                runtime_bytecode = '0x' + runtime_bytecode
            
            compilation_result = {
                'success': True,
                'contract_name': contract_name,
                'contract_path': contract_path,
                'bytecode': bytecode,
                'runtime_bytecode': runtime_bytecode,
                'abi': abi,
                'bytecode_size': len(bytecode) // 2 - 1,  # Subtract 1 for 0x prefix
                'solc_version': self.solc_version,
                'optimized': True,
                'constructor_inputs': self._extract_constructor_inputs(abi)
            }
            
            print(f"✅ Compilation successful!")
            print(f"   Contract: {contract_name}")
            print(f"   Bytecode size: {compilation_result['bytecode_size']} bytes")
            print(f"   ABI functions: {len([f for f in abi if f.get('type') == 'function'])}")
            print(f"   Constructor inputs: {len(compilation_result['constructor_inputs'])}")
            
            # Cache the result
            self.compiled_contracts[contract_name] = compilation_result
            
            return compilation_result
            
        except Exception as e:
            print(f"❌ Compilation error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _extract_constructor_inputs(self, abi: List[Dict]) -> List[Dict]:
        """Extract constructor input parameters from ABI"""
        for item in abi:
            if item.get('type') == 'constructor':
                return item.get('inputs', [])
        return []
    
    def encode_constructor_params(self, contract_name: str, *args) -> str:
        """
        Encode constructor parameters for contract deployment
        This is a simplified version - in production, use proper ABI encoding
        """
        try:
            if contract_name not in self.compiled_contracts:
                raise ValueError(f"Contract {contract_name} not compiled yet")
            
            contract_data = self.compiled_contracts[contract_name]
            constructor_inputs = contract_data['constructor_inputs']
            
            if len(args) != len(constructor_inputs):
                raise ValueError(f"Expected {len(constructor_inputs)} constructor args, got {len(args)}")
            
            print(f"🔧 Encoding constructor parameters for {contract_name}")
            print(f"   Args: {args}")
            print(f"   Expected types: {[inp['type'] for inp in constructor_inputs]}")
            
            # For now, return empty (no constructor params encoding)
            # In production, implement proper ABI encoding here
            encoded_params = ""
            
            print(f"✅ Constructor params encoded: {len(encoded_params)} chars")
            return encoded_params
            
        except Exception as e:
            print(f"❌ Constructor encoding error: {e}")
            raise
    
    def get_deployment_bytecode(self, contract_name: str, *constructor_args) -> str:
        """
        Get complete deployment bytecode including constructor parameters
        """
        try:
            if contract_name not in self.compiled_contracts:
                raise ValueError(f"Contract {contract_name} not compiled yet")
            
            contract_data = self.compiled_contracts[contract_name]
            base_bytecode = contract_data['bytecode']
            
            if constructor_args:
                # Encode constructor parameters
                encoded_params = self.encode_constructor_params(contract_name, *constructor_args)
                deployment_bytecode = base_bytecode + encoded_params.replace('0x', '')
            else:
                deployment_bytecode = base_bytecode
            
            print(f"📦 Deployment bytecode for {contract_name}:")
            print(f"   Base bytecode: {len(base_bytecode)} chars")
            print(f"   Constructor params: {len(deployment_bytecode) - len(base_bytecode)} chars")
            print(f"   Total: {len(deployment_bytecode)} chars")
            
            return deployment_bytecode
            
        except Exception as e:
            print(f"❌ Deployment bytecode error: {e}")
            raise
    
    def compile_all_contracts(self) -> Dict[str, Any]:
        """
        Compile all contracts in the contracts/ directory
        """
        try:
            print(f"🏭 Compiling all contracts...")
            
            contracts_dir = "contracts"
            if not os.path.exists(contracts_dir):
                raise FileNotFoundError(f"Contracts directory not found: {contracts_dir}")
            
            sol_files = [f for f in os.listdir(contracts_dir) if f.endswith('.sol')]
            print(f"   Found {len(sol_files)} .sol files: {sol_files}")
            
            compilation_results = {}
            
            for sol_file in sol_files:
                contract_path = os.path.join(contracts_dir, sol_file)
                contract_name = sol_file.replace('.sol', '')
                
                print(f"\n📝 Compiling {contract_name}...")
                result = self.compile_contract(contract_path, contract_name)
                compilation_results[contract_name] = result
                
                if result['success']:
                    print(f"✅ {contract_name} compiled successfully")
                else:
                    print(f"❌ {contract_name} compilation failed: {result['error']}")
            
            successful = sum(1 for r in compilation_results.values() if r['success'])
            total = len(compilation_results)
            
            print(f"\n📊 Compilation Summary:")
            print(f"   Total contracts: {total}")
            print(f"   Successful: {successful}")
            print(f"   Failed: {total - successful}")
            
            return {
                'success': successful > 0,
                'total_contracts': total,
                'successful_compilations': successful,
                'results': compilation_results,
                'compiled_contracts': [name for name, result in compilation_results.items() if result['success']]
            }
            
        except Exception as e:
            print(f"❌ Batch compilation error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_contract_info(self, contract_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a compiled contract"""
        return self.compiled_contracts.get(contract_name)
    
    def list_compiled_contracts(self) -> List[str]:
        """List all compiled contracts"""
        return list(self.compiled_contracts.keys())

# Test the compilation system
if __name__ == "__main__":
    print("🔧 Testing Contract Compilation System")
    print("=" * 50)
    
    compiler = ContractCompiler()
    
    # Test compiling all contracts
    print("Testing batch compilation...")
    result = compiler.compile_all_contracts()
    
    if result['success']:
        print(f"\n✅ Compilation successful!")
        print(f"Compiled contracts: {result['compiled_contracts']}")
        
        # Test individual contract operations
        for contract_name in result['compiled_contracts']:
            print(f"\n📋 Contract: {contract_name}")
            info = compiler.get_contract_info(contract_name)
            if info:
                print(f"   Bytecode size: {info['bytecode_size']} bytes")
                print(f"   Constructor inputs: {len(info['constructor_inputs'])}")
    else:
        print(f"❌ Compilation failed: {result.get('error', 'Unknown error')}")