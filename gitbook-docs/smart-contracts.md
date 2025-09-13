# Smart Contracts Documentation 📝

## Overview

Social X smart contracts are designed with security, efficiency, and modularity in mind. All contracts are deployed on HyperEVM and undergo rigorous testing and auditing before mainnet deployment.

## 🏗️ Architecture

### Contract Structure

```
Social X Protocol
├── Core Contracts
│   ├── SocialXToken.sol
│   ├── TokenFactory.sol
│   └── TreasuryManager.sol
├── Trading Contracts
│   ├── BondingCurve.sol
│   ├── MarketMaker.sol
│   └── OrderBook.sol
├── Governance
│   ├── GovernanceToken.sol
│   ├── DAOVoting.sol
│   └── Timelock.sol
└── Utilities
    ├── PriceOracle.sol
    ├── RewardDistributor.sol
    └── SecurityModule.sol
```

## 📜 Core Contracts

### SocialXToken.sol

**Purpose**: Main protocol token implementation

| Feature | Details |
|---------|---------|
| **Standard** | ERC-20 Compliant |
| **Supply** | 100,000,000 fixed |
| **Decimals** | 18 |
| **Mintable** | No (fixed supply) |
| **Burnable** | Yes (deflationary) |
| **Pausable** | Emergency only |

**Key Functions**:
```solidity
// Transfer with fee
function transfer(address to, uint256 amount) returns (bool)

// Burn tokens
function burn(uint256 amount) external

// Emergency pause
function pause() external onlyOwner

// Unpause
function unpause() external onlyOwner
```

**Security Features**:
- ✅ Reentrancy guards
- ✅ Integer overflow protection
- ✅ Access control
- ✅ Emergency pause

### TokenFactory.sol

**Purpose**: Deploy new social tokens

| Feature | Details |
|---------|---------|
| **Token Type** | ERC-20 |
| **Deploy Cost** | 1,000 $SOCIALX |
| **Initial Supply** | Customizable |
| **Bonding Curve** | Automated |

**Key Functions**:
```solidity
// Create new token
function createToken(
    string name,
    string symbol,
    uint256 supply,
    uint256 initialPrice
) returns (address)

// Set trading parameters
function setTradingParams(
    address token,
    uint256 buyFee,
    uint256 sellFee
) external

// Emergency actions
function emergencyWithdraw(address token) external onlyOwner
```

### TreasuryManager.sol

**Purpose**: Protocol treasury management

| Feature | Details |
|---------|---------|
| **Multi-sig** | 3 of 5 required |
| **Timelock** | 48 hour delay |
| **Spending Limits** | Daily caps |
| **Transparency** | On-chain logs |

**Key Functions**:
```solidity
// Propose spending
function proposeSpending(
    address recipient,
    uint256 amount,
    string purpose
) returns (uint256 proposalId)

// Approve proposal
function approveProposal(uint256 proposalId) external

// Execute proposal
function executeProposal(uint256 proposalId) external
```

## 💱 Trading Contracts

### BondingCurve.sol

**Purpose**: Automated market making

**Curve Types**:
```solidity
enum CurveType {
    LINEAR,      // y = mx + b
    EXPONENTIAL, // y = a * e^(bx)
    SIGMOID,     // y = L / (1 + e^(-k(x-x0)))
    QUADRATIC    // y = ax^2 + bx + c
}
```

**Price Calculation**:
```solidity
function calculateBuyPrice(
    uint256 supply,
    uint256 amount
) public view returns (uint256)

function calculateSellPrice(
    uint256 supply,
    uint256 amount
) public view returns (uint256)
```

### MarketMaker.sol

**Purpose**: Liquidity provision and trading

**Features**:
- Instant buy/sell execution
- Slippage protection
- Front-running prevention
- MEV resistance

**Key Functions**:
```solidity
// Buy tokens
function buy(
    address token,
    uint256 minAmount,
    uint256 deadline
) external payable

// Sell tokens
function sell(
    address token,
    uint256 amount,
    uint256 minReceived,
    uint256 deadline
) external

// Add liquidity
function addLiquidity(
    address token,
    uint256 amount
) external payable
```

## 🗳️ Governance Contracts

### GovernanceToken.sol

**Purpose**: Voting power representation

**Voting Mechanism**:
```solidity
struct Proposal {
    uint256 id;
    address proposer;
    string description;
    uint256 forVotes;
    uint256 againstVotes;
    uint256 startBlock;
    uint256 endBlock;
    bool executed;
}
```

### DAOVoting.sol

**Purpose**: Decentralized decision making

**Voting Parameters**:
| Parameter | Value |
|-----------|-------|
| **Quorum** | 10% of supply |
| **Voting Period** | 3 days |
| **Execution Delay** | 2 days |
| **Proposal Threshold** | 1% of supply |

## 🔒 Security Features

### Access Control

**Role-Based Permissions**:
```solidity
bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");
```

### Reentrancy Protection

All contracts implement OpenZeppelin's ReentrancyGuard:
```solidity
modifier nonReentrant() {
    require(!locked, "Reentrant call");
    locked = true;
    _;
    locked = false;
}
```

### Emergency Functions

**Circuit Breakers**:
```solidity
// Global pause
function emergencyPause() external onlyOwner {
    _pause();
    emit EmergencyPause(msg.sender);
}

// Withdraw stuck funds
function emergencyWithdraw() external onlyOwner {
    // Implementation
}
```

## 📊 Contract Addresses

### Mainnet (HyperEVM - Chain ID: 999)

| Contract | Address | Status |
|----------|---------|--------|
| **$SOCIALX Token** | `0x...` | Pending deployment |
| **Token Factory** | `0x...` | Pending deployment |
| **Treasury** | `0x25B21833Aa899Bfc5FE6C145f42112b1D618e82a` | Pending deployment |
| **Market Maker** | `0x...` | Pending deployment |
| **Governance** | `0x...` | Pending deployment |

### Testnet (HyperEVM Testnet)

| Contract | Address | Status |
|----------|---------|--------|
| **$SOCIALX Token** | `0x1234...` | Deployed ✅ |
| **Token Factory** | `0x5678...` | Deployed ✅ |
| **Treasury** | `0x9012...` | Deployed ✅ |
| **Market Maker** | `0x3456...` | Deployed ✅ |
| **Governance** | `0x7890...` | Deployed ✅ |

## 🔍 Audit Status

### Security Audits

| Auditor | Date | Status | Report |
|---------|------|--------|--------|
| **CertiK** | Q1 2025 | Scheduled | Pending |
| **Quantstamp** | Q1 2025 | Scheduled | Pending |
| **Internal** | Jan 2025 | Complete ✅ | [View](https://docs.socialx.io/audits) |

### Audit Findings

**Internal Audit Results**:
- ✅ No critical issues
- ✅ 2 medium issues (fixed)
- ✅ 5 low issues (fixed)
- ✅ 8 informational (acknowledged)

## 🛠️ Integration Guide

### Connecting to Contracts

**Web3.js Example**:
```javascript
const Web3 = require('web3');
const web3 = new Web3('https://rpc.hyperevm.io');

// Contract ABI
const tokenABI = [...];

// Contract instance
const tokenContract = new web3.eth.Contract(
    tokenABI,
    '0x...' // Token address
);

// Call functions
const balance = await tokenContract.methods
    .balanceOf(address)
    .call();
```

**Ethers.js Example**:
```javascript
const { ethers } = require('ethers');

// Provider
const provider = new ethers.providers.JsonRpcProvider(
    'https://rpc.hyperevm.io'
);

// Contract
const tokenContract = new ethers.Contract(
    tokenAddress,
    tokenABI,
    provider
);

// Interact
const balance = await tokenContract.balanceOf(address);
```

## 📚 ABI Documentation

### Function Signatures

**Token Functions**:
```solidity
// ERC-20 Standard
balanceOf(address) → uint256
transfer(address, uint256) → bool
approve(address, uint256) → bool
transferFrom(address, address, uint256) → bool
allowance(address, address) → uint256
totalSupply() → uint256

// Extended Functions
burn(uint256)
pause()
unpause()
```

**Factory Functions**:
```solidity
createToken(string, string, uint256, uint256) → address
getTokenCount() → uint256
getTokenAt(uint256) → address
setFees(uint256, uint256)
```

## 🔧 Development Tools

### Testing Framework

**Hardhat Configuration**:
```javascript
module.exports = {
  solidity: "0.8.19",
  networks: {
    hyperevm: {
      url: "https://rpc.hyperevm.io",
      chainId: 999,
      accounts: [process.env.PRIVATE_KEY]
    }
  }
};
```

### Deployment Scripts

**Deploy Example**:
```javascript
async function main() {
  const Token = await ethers.getContractFactory("SocialXToken");
  const token = await Token.deploy();
  await token.deployed();
  
  console.log("Token deployed to:", token.address);
}

main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });
```

## 🔐 Best Practices

### Security Checklist

Before interacting with contracts:
- ✅ Verify contract address
- ✅ Check audit reports
- ✅ Test on testnet first
- ✅ Use appropriate gas limits
- ✅ Implement error handling

### Gas Optimization

**Tips for Lower Fees**:
1. Batch transactions when possible
2. Use optimal data types
3. Minimize storage operations
4. Avoid loops in contracts
5. Pack struct variables

## 📡 Network Details

### HyperEVM Configuration

| Parameter | Value |
|-----------|-------|
| **Network Name** | HyperEVM |
| **Chain ID** | 999 |
| **RPC URL** | https://rpc.hyperevm.io |
| **WebSocket** | wss://ws.hyperevm.io |
| **Explorer** | https://explorer.hyperevm.io |
| **Currency** | HYPE |
| **Block Time** | ~2 seconds |
| **Gas Price** | ~0.001 HYPE |

## 🚨 Emergency Procedures

### In Case of Issues

1. **Contract Bug**:
   - Pause affected contracts
   - Notify users immediately
   - Deploy fix after audit

2. **Security Breach**:
   - Emergency pause all contracts
   - Secure treasury funds
   - Investigate and patch

3. **Network Issues**:
   - Monitor alternative RPCs
   - Communicate via social channels
   - Prepare contingency plans

## 📞 Developer Support

### Resources

- 📚 **Documentation**: [docs.socialx.io](https://docs.socialx.io)
- 💻 **GitHub**: [github.com/socialx-protocol](https://github.com/socialx-protocol)
- 💬 **Discord**: [discord.gg/socialx-dev](https://discord.gg/socialx-dev)
- 📧 **Email**: dev@socialx.io

### Bug Bounty Program

| Severity | Reward |
|----------|--------|
| **Critical** | Up to $50,000 |
| **High** | Up to $10,000 |
| **Medium** | Up to $2,500 |
| **Low** | Up to $500 |

Report security issues to: security@socialx.io

---

**Building on Social X?** Join our developer community for support and resources!

*Secure. Efficient. Decentralized.* 🔒