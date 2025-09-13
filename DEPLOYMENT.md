# Social X Platform - Vercel Deployment Guide

## Quick Deploy to Vercel

### 1. Deploy Frontend
1. Go to [Vercel](https://vercel.com)
2. Import this repository
3. Configure:
   - Framework Preset: **Vite**
   - Root Directory: **`frontend`**
   - Build Command: **`npm run build`**
   - Output Directory: **`dist`**

### 2. Environment Variables
Add these in Vercel dashboard:
```
VITE_PRIVY_APP_ID=cmf0n2ra100qzl20b4gxr8ql0
```

### 3. Configure Privy Dashboard
1. Go to [Privy Dashboard](https://dashboard.privy.io)
2. Add your Vercel URL as allowed origin
3. Set OAuth redirect URL: `https://your-app.vercel.app/auth/privy-callback`
4. Enable Twitter/X login method

## Features
- ✅ X (Twitter) Authentication via Privy
- ✅ Wallet Connection (MetaMask, WalletConnect)
- ✅ Token Launch with HyperEVM
- ✅ 100M Token Supply with Tokenomics
- ✅ Presale (1 HYPE = 20,000 SOCIALX)
- ✅ 2.5M Beta Tester Airdrop

## Privy App ID
```
cmf0n2ra100qzl20b4gxr8ql0
```

## Support
For issues, check the browser console for errors and ensure:
1. Privy App ID is correctly set
2. Your domain is whitelisted in Privy Dashboard
3. OAuth callback URL matches exactly