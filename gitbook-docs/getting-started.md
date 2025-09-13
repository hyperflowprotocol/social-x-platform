# Getting Started 🚀

Welcome to Social X! This guide will walk you through everything you need to know to start trading social tokens and launching your own.

## 📋 Prerequisites

Before you begin, make sure you have:

- ✅ A Web3 wallet (MetaMask, Rabby, or WalletConnect compatible)
- ✅ Some $HYPE tokens for gas fees
- ✅ A Twitter/X account (for social features)
- ✅ Basic understanding of DeFi and trading

## 🔗 Step 1: Connect Your Wallet

### Supported Wallets

| Wallet | Desktop | Mobile | WalletConnect |
|--------|---------|--------|---------------|
| **MetaMask** | ✅ | ✅ | ✅ |
| **Rabby** | ✅ | ❌ | ✅ |
| **Trust Wallet** | ❌ | ✅ | ✅ |
| **Coinbase Wallet** | ✅ | ✅ | ✅ |
| **Rainbow** | ✅ | ✅ | ✅ |

### Connection Steps

1. **Click "Connect Wallet"** in the top-right corner
2. **Select your wallet** from the list
3. **Approve the connection** in your wallet
4. **Select the network**:
   - HyperEVM (Chain ID: 999) - Primary
   - Base (Chain ID: 8453) - Secondary

### Adding HyperEVM Network

If HyperEVM isn't in your wallet, add it manually:

```javascript
Network Name: HyperEVM
Chain ID: 999
RPC URL: https://rpc.hyperevm.io
Currency Symbol: HYPE
Block Explorer: https://explorer.hyperevm.io
```

## 🐦 Step 2: Connect Twitter/X Account

### Why Connect Twitter?

- 🎯 Verify your identity
- 📊 Track social metrics
- 🏆 Earn engagement rewards
- 🔐 Secure your social tokens

### OAuth Authentication Process

1. **Navigate to Profile** → Click your wallet address
2. **Click "Connect Twitter"** button
3. **Authorize Social X** on Twitter's OAuth page
4. **Confirm connection** back on Social X
5. **Verification complete** - Your profile is now linked!

### Privacy & Permissions

We only request:
- ✅ Read your profile information
- ✅ View your public tweets
- ✅ Check follower count
- ❌ We NEVER post on your behalf
- ❌ We NEVER access DMs

## 🪙 Step 3: Launch Your Token

### Token Creation Process

#### 1. Access Token Launcher
```
Dashboard → Create → Launch Token
```

#### 2. Configure Token Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| **Token Name** | Full name of your token | "Creator Coin" |
| **Symbol** | 3-5 character ticker | "CREATE" |
| **Total Supply** | Maximum tokens | 1,000,000 |
| **Initial Price** | Starting price in $HYPE | 0.001 |
| **Description** | Token purpose | "Community token for..." |

#### 3. Set Trading Parameters

**Bonding Curve Options:**
- **Linear**: Steady price increase
- **Exponential**: Rapid price growth
- **Sigmoid**: S-curve pricing

**Fee Structure:**
| Fee Type | Creator | Protocol | LP |
|----------|---------|----------|-----|
| **Buy** | 5% | 1% | 4% |
| **Sell** | 5% | 1% | 4% |

#### 4. Deploy Contract

1. **Review all parameters** carefully
2. **Approve $SOCIALX spend** (1,000 tokens)
3. **Confirm deployment** transaction
4. **Wait for confirmation** (~15 seconds)
5. **Token live!** Share with your community

### Post-Launch Checklist

- [ ] Share token address with community
- [ ] Add initial liquidity
- [ ] Set up token socials
- [ ] Create holder rewards
- [ ] Monitor trading activity

## 💱 Step 4: Start Trading

### Finding Tokens to Trade

#### Browse Methods

1. **Trending** - Most active tokens
2. **New Launches** - Recently created
3. **Top Gainers** - Best performers
4. **Search** - Find specific tokens

#### Token Information

Each token page shows:
- 📊 **Price Chart** - Historical performance
- 📈 **Market Cap** - Total value
- 💧 **Liquidity** - Available for trading
- 👥 **Holders** - Number of owners
- 🔄 **24h Volume** - Trading activity
- 🐦 **Social Metrics** - Twitter engagement

### Executing a Trade

#### Buy Process

1. **Select token** from marketplace
2. **Enter amount** in $HYPE or tokens
3. **Review details**:
   - Price impact
   - Fees
   - Minimum received
4. **Click "Buy"** button
5. **Confirm** in wallet
6. **Success!** Tokens in wallet

#### Sell Process

1. **Go to portfolio** or token page
2. **Click "Sell"** button
3. **Enter amount** to sell
4. **Review details**:
   - Expected $HYPE
   - Price impact
   - Fees
5. **Approve & Sell**
6. **Receive $HYPE** in wallet

### Trading Best Practices

| Do's | Don'ts |
|------|--------|
| ✅ Check liquidity before trading | ❌ FOMO into pumps |
| ✅ Set slippage appropriately | ❌ Ignore price impact |
| ✅ Verify contract address | ❌ Trade more than you can afford |
| ✅ Monitor gas prices | ❌ Neglect security |
| ✅ Take profits gradually | ❌ Panic sell |

## 🌐 Supported Networks

### Primary Network: HyperEVM

| Feature | Details |
|---------|---------|
| **Chain ID** | 999 |
| **Native Token** | $HYPE |
| **Block Time** | ~2 seconds |
| **Gas Fees** | ~$0.001 |
| **Finality** | Instant |

### Secondary Network: Base

| Feature | Details |
|---------|---------|
| **Chain ID** | 8453 |
| **Native Token** | $ETH |
| **Block Time** | ~2 seconds |
| **Gas Fees** | ~$0.01 |
| **Bridge** | Coming Q3 2025 |

## 📱 Mobile Experience

### Progressive Web App (PWA)

1. **Open Social X** in mobile browser
2. **Click "Add to Home Screen"**
3. **Install PWA** for app-like experience
4. **Enable notifications** for trade alerts

### Native Apps (Coming Q3 2025)

- 📱 iOS App Store
- 🤖 Google Play Store
- 🔔 Push notifications
- 👆 Touch-optimized UI

## 🛡️ Security Tips

### Wallet Security

1. **Never share** your seed phrase
2. **Verify URLs** - Always use socialx.io
3. **Check transactions** before signing
4. **Use hardware wallets** for large amounts
5. **Enable 2FA** where possible

### Trading Security

- ⚠️ **Verify token contracts** on explorer
- ⚠️ **Check liquidity locks** before buying
- ⚠️ **Beware of honeypots** - Can't sell
- ⚠️ **Watch for rugs** - Sudden liquidity removal
- ⚠️ **DYOR** - Do Your Own Research

## 🆘 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **Wallet won't connect** | Clear cache, try different browser |
| **Transaction stuck** | Increase gas, cancel & retry |
| **Can't see tokens** | Add token address to wallet |
| **Twitter auth fails** | Clear cookies, re-authenticate |
| **High slippage error** | Increase slippage to 5-10% |

## 📚 Additional Resources

### Tutorials & Guides

- 📹 [Video: How to Trade](https://youtube.com/socialx)
- 📝 [Blog: Token Creation Guide](https://blog.socialx.io)
- 🎓 [Academy: DeFi Basics](https://academy.socialx.io)

### Get Help

- 💬 [Discord Support](https://discord.gg/socialx)
- 📧 [Email Support](mailto:support@socialx.io)
- 🐦 [Twitter Support](https://twitter.com/socialx)
- 📖 [Knowledge Base](https://help.socialx.io)

## 🎯 Next Steps

Now that you're set up:

1. 💰 **Join the Presale** - Get $SOCIALX early
2. 🎁 **Claim Airdrop** - If eligible
3. 🌟 **Launch a Token** - Build your community
4. 📊 **Start Trading** - Grow your portfolio
5. 🏆 **Earn Rewards** - Stake and provide liquidity

---

**Need more help?** Join our [Discord](https://discord.gg/socialx) and ask our community!

*Happy Trading! 🚀*