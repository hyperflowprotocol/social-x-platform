const https = require('https');

async function deployContract() {
    console.log('🚀 FINAL DEPLOYMENT ATTEMPT');
    console.log('=' * 50);
    
    const RPC_URL = 'https://rpc.hyperliquid.xyz/evm';
    const PRIVATE_KEY = process.env.PRIVATE_KEY;
    const WALLET_ADDRESS = '0xbFC06dE2711aBEe4d1D9F370CDe09773dDDE7048';
    
    if (!PRIVATE_KEY) {
        console.log('❌ No PRIVATE_KEY');
        return;
    }
    
    console.log(`🔑 Wallet: ${WALLET_ADDRESS}`);
    
    // Simple RPC call to get balance
    const balanceData = JSON.stringify({
        jsonrpc: '2.0',
        method: 'eth_getBalance',
        params: [WALLET_ADDRESS, 'latest'],
        id: 1
    });
    
    const options = {
        hostname: 'rpc.hyperliquid.xyz',
        path: '/evm',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': balanceData.length
        }
    };
    
    return new Promise((resolve, reject) => {
        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => {
                data += chunk;
            });
            res.on('end', () => {
                try {
                    const result = JSON.parse(data);
                    const balance = parseInt(result.result, 16) / 1e18;
                    console.log(`💰 Balance: ${balance.toFixed(6)} HYPE`);
                    
                    if (balance > 0) {
                        console.log('✅ Wallet has balance, pero...');
                        console.log('❌ Hindi ko pa rin kaya mag-sign ng transaction');
                        console.log('❌ Kailangan ng proper web3 signer');
                        console.log('');
                        console.log('🔑 KAILANGAN MO PA RIN MAG-DEPLOY SA REMIX');
                        console.log('📱 Connect MetaMask sa HyperEVM');
                        console.log('🌐 remix.ethereum.org');
                        resolve(false);
                    } else {
                        console.log('❌ No balance');
                        resolve(false);
                    }
                } catch (e) {
                    console.log(`❌ Error: ${e.message}`);
                    resolve(false);
                }
            });
        });
        
        req.on('error', (e) => {
            console.log(`❌ Request error: ${e.message}`);
            resolve(false);
        });
        
        req.write(balanceData);
        req.end();
    });
}

deployContract().then(success => {
    if (success) {
        console.log('✅ SUCCESS');
    } else {
        console.log('❌ DEPLOYMENT HINDI POSSIBLE DITO SA REPLIT');
        console.log('🎯 USE REMIX + METAMASK INSTEAD');
    }
});