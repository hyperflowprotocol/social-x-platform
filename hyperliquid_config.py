#!/usr/bin/env python3
"""
Hyperliquid Configuration for Social Trading Platform
Official RPC endpoints and chain configuration
"""

# Official Hyperliquid Configuration
HYPERLIQUID_CONFIG = {
    'mainnet': {
        'chain_id': 42161,  # 0xa4b1 in hex
        'chain_id_hex': '0xa4b1',
        'rpc_url': 'https://rpc.hyperliquid.xyz/evm',
        'api_url': 'https://api.hyperliquid.xyz',
        'network_name': 'Hyperliquid Mainnet',
        'native_currency': {
            'name': 'HYPE',
            'symbol': 'HYPE',
            'decimals': 18
        },
        'explorer_url': 'https://hyperliquid.xyz',
        'hyperevm_bridge': '0x2222222222222222222222222222222222222222'
    },
    'testnet': {
        'chain_id': 998,  # HyperEVM Testnet
        'chain_id_hex': '0x3e6',
        'rpc_url': 'https://rpc.hyperliquid-testnet.xyz/evm',
        'api_url': 'https://api.hyperliquid-testnet.xyz',
        'network_name': 'Hyperliquid Testnet',
        'native_currency': {
            'name': 'HYPE',
            'symbol': 'HYPE',
            'decimals': 18
        },
        'explorer_url': 'https://testnet.hyperliquid.xyz',
        'hyperevm_bridge': '0x2222222222222222222222222222222222222222'
    }
}

# Default to mainnet
DEFAULT_NETWORK = 'mainnet'
CURRENT_CONFIG = HYPERLIQUID_CONFIG[DEFAULT_NETWORK]

# RPC Methods supported by Hyperliquid
SUPPORTED_RPC_METHODS = [
    'net_version',
    'web3_clientVersion',
    'eth_blockNumber',
    'eth_call',
    'eth_chainId',
    'eth_estimateGas',
    'eth_getBalance',
    'eth_getTransactionCount',
    'eth_sendRawTransaction',
    'eth_getTransactionReceipt'
]

def get_chain_config(network='mainnet'):
    """Get chain configuration for wallet connection"""
    config = HYPERLIQUID_CONFIG.get(network, HYPERLIQUID_CONFIG['mainnet'])
    
    return {
        'chainId': config['chain_id_hex'],
        'chainName': config['network_name'],
        'nativeCurrency': config['native_currency'],
        'rpcUrls': [config['rpc_url']],
        'blockExplorerUrls': [config['explorer_url']]
    }

def get_deposit_instructions():
    """Get instructions for depositing HYPE tokens"""
    return {
        'bridge_address': CURRENT_CONFIG['hyperevm_bridge'],
        'instructions': [
            'Send HYPE tokens to the HyperEVM bridge address',
            f'Bridge address: {CURRENT_CONFIG["hyperevm_bridge"]}',
            'Tokens will appear in your HyperEVM wallet within 1-2 blocks',
            'Minimum deposit: 10 HYPE',
            'Network fee: ~0.001 HYPE'
        ],
        'warning': 'Double-check the bridge address before sending tokens'
    }