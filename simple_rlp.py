#!/usr/bin/env python3
"""
Simple RLP encoding for Ethereum transactions
Using only built-in Python libraries
"""

def encode_length(length, offset):
    """Encode length according to RLP rules"""
    if length < 56:
        return bytes([length + offset])
    elif length < 256**8:
        bl = (length.bit_length() + 7) // 8
        return bytes([bl + offset + 55]) + length.to_bytes(bl, 'big')
    else:
        raise ValueError("Length too large")

def encode_item(item):
    """Encode a single item"""
    if isinstance(item, bytes):
        if len(item) == 1 and item[0] < 128:
            return item
        else:
            return encode_length(len(item), 128) + item
    elif isinstance(item, int):
        if item == 0:
            return b'\x80'
        else:
            return encode_item(item.to_bytes((item.bit_length() + 7) // 8, 'big'))
    elif isinstance(item, str):
        if item.startswith('0x'):
            return encode_item(bytes.fromhex(item[2:]))
        else:
            return encode_item(item.encode('utf-8'))
    else:
        raise ValueError(f"Cannot encode {type(item)}")

def rlp_encode(data):
    """RLP encode a list of items"""
    if isinstance(data, list):
        output = b''.join(encode_item(item) for item in data)
        return encode_length(len(output), 192) + output
    else:
        return encode_item(data)

def create_transaction_rlp(nonce, gas_price, gas_limit, to, value, data, v, r, s):
    """Create RLP-encoded transaction"""
    # Convert to appropriate format
    transaction = [
        nonce,
        gas_price, 
        gas_limit,
        bytes.fromhex(to[2:]) if to and to.startswith('0x') else b'',  # Empty for contract deployment
        value,
        bytes.fromhex(data[2:]) if data and data.startswith('0x') and all(c in '0123456789abcdefABCDEF' for c in data[2:]) else b'',
        v,
        r,
        s
    ]
    
    return rlp_encode(transaction)

if __name__ == "__main__":
    # Test RLP encoding
    tx_rlp = create_transaction_rlp(
        nonce=0,
        gas_price=20000000000,
        gas_limit=3000000,
        to='',  # Contract deployment
        value=0,
        data='0x608060405234801561001057600080fd5b50',  # Sample bytecode
        v=2037,  # Chain ID 999 * 2 + 35
        r=0x1111111111111111111111111111111111111111111111111111111111111111,
        s=0x2222222222222222222222222222222222222222222222222222222222222222
    )
    
    print(f"RLP encoded: 0x{tx_rlp.hex()}")
    print(f"Length: {len(tx_rlp)} bytes")