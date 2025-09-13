// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface IERC20 {
    function transfer(address to, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

contract SocialXTradingSecure {
    address public owner;
    address public platformFeeWallet = 0xCbd45BE04C2CB52811609ef0334A9097fB2E2c48;
    IERC20 public hypeToken;
    bool public paused = false;
    
    // Platform fees
    uint256 public platformFeePercent = 250; // 2.5%
    uint256 public creatorFeePercent = 100;  // 1.0%
    uint256 public referralFeePercent = 50;  // 0.5%
    uint256 public constant FEE_DENOMINATOR = 10000;
    
    // Dynamic launch requirements (adjustable by owner)
    uint256 public minimumLaunchDeposit = 1 * 1e18; // 1 HYPE minimum
    uint256 public constant INITIAL_TOKEN_SUPPLY = 1000000000 * 1e18; // 1B tokens
    uint256 public constant BASE_HYPE_DEPOSIT = 1 * 1e18; // 1 HYPE = base allocation
    uint256 public constant FIXED_MC_TOKENS = 3000000; // 3M tokens for 1 HYPE (1B/3M = 333 HYPE = $14.3K MC)
    
    struct SocialAccount {
        string handle;
        address creator;
        uint256 totalSupply;
        uint256 currentSupply;
        uint256 tradingPool;    // HYPE for buy/sell operations
        uint256 creatorPool;    // HYPE reserved for creator
        uint256 platformPool;   // HYPE for platform fees
        uint256 liquidityPool;  // Combined total for backward compatibility
        bool exists;
        mapping(address => uint256) balances;
    }
    
    mapping(string => SocialAccount) public accounts;
    mapping(address => uint256) public userHypeBalances;
    mapping(address => address) public referrers; // user => referrer
    mapping(address => uint256) public referralEarnings; // referrer => total earnings
    
    // Points system for airdrops (NON-TRANSFERABLE)
    mapping(address => uint256) public userPoints; // user => total points (cannot transfer)
    mapping(address => uint256) public tradingVolume; // user => total trading volume
    mapping(address => uint256) public accountsLaunched; // user => number of accounts launched
    mapping(address => uint256) public referralCount; // user => number of referrals
    uint256 public totalPointsDistributed;
    
    // Daily trading volume tracking (auto-resets every 24h)
    mapping(address => uint256) public dailyTradingVolume; // resets automatically
    mapping(address => uint256) public lastVolumeReset; // last reset timestamp
    mapping(address => uint256) public lastDailyPointsClaim; // last auto-distribution
    
    // Point multipliers (basis points - 10000 = 100%)
    uint256 public buyPointsMultiplier = 100;    // 1% of trade value in points
    uint256 public sellPointsMultiplier = 50;    // 0.5% of trade value in points
    uint256 public launchPointsReward = 10000;   // 10,000 points for launching account
    uint256 public referralPointsReward = 20;    // 20 points for each referral (they get 0.5% fees already)
    uint256 public dailyTradingPointsMultiplier = 200; // 2% of daily volume in points
    
    string[] public allAccounts;
    
    event AccountLaunched(string indexed handle, address indexed creator, uint256 initialDeposit);
    event DeveloperTokensAllocated(string indexed handle, address indexed creator, uint256 tokens, uint256 hypeDeposit);
    event TokensPurchased(string indexed handle, address indexed buyer, uint256 tokens, uint256 cost);
    event TokensSold(string indexed handle, address indexed seller, uint256 tokens, uint256 proceeds);
    event ReferralSet(address indexed user, address indexed referrer);
    event ReferralEarned(address indexed referrer, address indexed user, uint256 amount);
    event PointsEarned(address indexed user, uint256 points, string reason);
    event EmergencyWithdrawal(address indexed user, uint256 amount);
    event PlatformPoolWithdrawal(address indexed owner, string indexed handle, uint256 amount);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }
    
    modifier notPaused() {
        require(!paused, "Contract paused");
        _;
    }
    
    modifier accountExists(string memory handle) {
        require(accounts[handle].exists, "Account doesn't exist");
        _;
    }
    
    constructor(address _hypeToken, address _platformFeeWallet) {
        owner = msg.sender;
        platformFeeWallet = _platformFeeWallet;
        hypeToken = IERC20(_hypeToken);
    }
    
    // Square root function for LiquidLaunch-style calculations
    function sqrt(uint256 x) internal pure returns (uint256) {
        if (x == 0) return 0;
        uint256 z = (x + 1) / 2;
        uint256 y = x;
        while (z < y) {
            y = z;
            z = (x / z + z) / 2;
        }
        return y;
    }
    
    // Simple linear pricing with small growth factor
    function calculateBondingCurvePrice(uint256 supply, uint256 amount) internal pure returns (uint256) {
        if (supply == 0) return amount * 1e12; // Base price for first purchase
        
        // Simple linear pricing: current_price = supply / 1e12
        // This creates gradual price increases without explosive growth
        uint256 currentPrice = supply / 1e12; // Price per token in wei
        
        return currentPrice * amount; // Total cost for amount of tokens
    }

    // Set referrer for new users
    function setReferrer(address referrer) external {
        require(referrers[msg.sender] == address(0), "Referrer already set");
        require(referrer != msg.sender, "Cannot refer yourself");
        require(referrer != address(0), "Invalid referrer");
        
        referrers[msg.sender] = referrer;
        emit ReferralSet(msg.sender, referrer);
    }
    
    // Launch a new social account as tradeable asset
    function launchAccount(
        string memory handle,
        uint256 initialHypeDeposit,
        address referrer
    ) external notPaused {
        require(!accounts[handle].exists, "Account already exists");
        require(initialHypeDeposit >= minimumLaunchDeposit, "Insufficient deposit");
        require(bytes(handle).length > 0, "Invalid handle");
        
        // Transfer HYPE from creator to contract
        require(
            hypeToken.transferFrom(msg.sender, address(this), initialHypeDeposit),
            "HYPE transfer failed"
        );
        
        // Set referrer if provided and not already set
        if (referrer != address(0) && referrers[msg.sender] == address(0) && referrer != msg.sender) {
            referrers[msg.sender] = referrer;
            referralCount[referrer]++;
            
            // Award points to referrer
            userPoints[referrer] += referralPointsReward;
            totalPointsDistributed += referralPointsReward;
            
            emit ReferralSet(msg.sender, referrer);
            emit PointsEarned(referrer, referralPointsReward, "referral");
        }
        
        // Two-tier allocation system:
        // 1 HYPE = Fixed 12K market cap
        // 2+ HYPE = Dynamic scaling with square root diminishing returns
        uint256 creatorTokens;
        
        if (initialHypeDeposit == BASE_HYPE_DEPOSIT) {
            // Exactly 1 HYPE = Fixed tokens for 12K market cap
            creatorTokens = FIXED_MC_TOKENS * 1e18;
        } else {
            // 2+ HYPE = Dynamic allocation with square root scaling
            uint256 depositMultiplier = (initialHypeDeposit * 1e18) / BASE_HYPE_DEPOSIT; // Convert to 18 decimal scaling
            creatorTokens = (sqrt(depositMultiplier) * FIXED_MC_TOKENS * 1e18) / 1e9; // Square root with precision adjustment
        }
        
        // Cap at maximum 50% of total supply for safety
        uint256 maxCreatorTokens = INITIAL_TOKEN_SUPPLY / 2;
        if (creatorTokens > maxCreatorTokens) {
            creatorTokens = maxCreatorTokens;
        }
        
        // Initialize account with separate pool allocation
        uint256 circulatingSupply = creatorTokens;
        
        // Pool allocation strategy:
        uint256 tradingPoolAmount = (initialHypeDeposit * 70) / 100;  // 70% for trading operations
        uint256 creatorPoolAmount = (initialHypeDeposit * 20) / 100;  // 20% reserved for creator
        uint256 platformPoolAmount = (initialHypeDeposit * 10) / 100; // 10% platform reserve
        
        SocialAccount storage account = accounts[handle];
        account.handle = handle;
        account.creator = msg.sender;
        account.totalSupply = INITIAL_TOKEN_SUPPLY;
        account.currentSupply = INITIAL_TOKEN_SUPPLY - creatorTokens;
        account.tradingPool = tradingPoolAmount;
        account.creatorPool = creatorPoolAmount;
        account.platformPool = platformPoolAmount;
        account.liquidityPool = initialHypeDeposit; // Total for compatibility
        account.exists = true;
        account.balances[msg.sender] = creatorTokens;
        
        allAccounts.push(handle);
        
        // Award points for launching account
        accountsLaunched[msg.sender]++;
        userPoints[msg.sender] += launchPointsReward;
        totalPointsDistributed += launchPointsReward;
        
        emit AccountLaunched(handle, msg.sender, initialHypeDeposit);
        emit DeveloperTokensAllocated(handle, msg.sender, creatorTokens, initialHypeDeposit);
        emit PointsEarned(msg.sender, launchPointsReward, "launch_account");
    }
    
    // Buy tokens using bonding curve pricing
    function buyTokens(
        string memory handle,
        uint256 tokenAmount,
        uint256 maxCost
    ) external notPaused accountExists(handle) {
        require(tokenAmount > 0, "Invalid amount");
        
        SocialAccount storage account = accounts[handle];
        require(tokenAmount <= account.currentSupply, "Insufficient supply");
        
        uint256 cost = calculateBuyPrice(handle, tokenAmount);
        require(cost <= maxCost, "Slippage too high");
        
        // Calculate fees
        uint256 platformFee = (cost * platformFeePercent) / FEE_DENOMINATOR;
        uint256 creatorFee = (cost * creatorFeePercent) / FEE_DENOMINATOR;
        uint256 referralFee = 0;
        
        // Check for referral
        address userReferrer = referrers[msg.sender];
        if (userReferrer != address(0)) {
            referralFee = (cost * referralFeePercent) / FEE_DENOMINATOR;
            platformFee -= referralFee; // Referral fee comes from platform fee
        }
        
        uint256 totalCost = cost + platformFee + creatorFee + referralFee;
        
        // Transfer HYPE from buyer
        require(
            hypeToken.transferFrom(msg.sender, address(this), totalCost),
            "HYPE transfer failed"
        );
        
        // Update account state with separate pool allocation
        uint256 tradingIncrease = (cost * 80) / 100;    // 80% to trading pool
        uint256 platformIncrease = (cost * 15) / 100;   // 15% to platform pool
        uint256 creatorIncrease = (cost * 5) / 100;     // 5% to creator pool
        
        account.currentSupply -= tokenAmount;
        account.tradingPool += tradingIncrease;
        account.platformPool += platformIncrease;  
        account.creatorPool += creatorIncrease;
        account.liquidityPool += cost; // Update total for compatibility
        account.balances[msg.sender] += tokenAmount;
        
        // Distribute fees
        require(hypeToken.transfer(platformFeeWallet, platformFee), "Platform fee transfer failed");
        userHypeBalances[account.creator] += creatorFee;
        
        // Pay referral fee if applicable
        if (referralFee > 0 && userReferrer != address(0)) {
            userHypeBalances[userReferrer] += referralFee;
            referralEarnings[userReferrer] += referralFee;
            emit ReferralEarned(userReferrer, msg.sender, referralFee);
        }
        
        // Award points for buying tokens
        uint256 buyPoints = (cost * buyPointsMultiplier) / FEE_DENOMINATOR;
        userPoints[msg.sender] += buyPoints;
        tradingVolume[msg.sender] += cost;
        totalPointsDistributed += buyPoints;
        
        emit TokensPurchased(handle, msg.sender, tokenAmount, totalCost);
        emit PointsEarned(msg.sender, buyPoints, "buy_tokens");
    }
    
    // Sell tokens back to the pool
    function sellTokens(
        string memory handle,
        uint256 tokenAmount,
        uint256 minProceeds
    ) external notPaused accountExists(handle) {
        require(tokenAmount > 0, "Invalid amount");
        
        SocialAccount storage account = accounts[handle];
        require(account.balances[msg.sender] >= tokenAmount, "Insufficient tokens");
        
        uint256 proceeds = calculateSellPrice(handle, tokenAmount);
        require(proceeds >= minProceeds, "Slippage too high");
        require(account.liquidityPool >= proceeds, "Insufficient liquidity");
        
        // Calculate fees
        uint256 platformFee = (proceeds * platformFeePercent) / FEE_DENOMINATOR;
        uint256 creatorFee = (proceeds * creatorFeePercent) / FEE_DENOMINATOR;
        uint256 referralFee = 0;
        
        // Check for referral
        address userReferrer = referrers[msg.sender];
        if (userReferrer != address(0)) {
            referralFee = (proceeds * referralFeePercent) / FEE_DENOMINATOR;
            platformFee -= referralFee; // Referral fee comes from platform fee
        }
        
        uint256 netProceeds = proceeds - platformFee - creatorFee - referralFee;
        
        // Update account state - remove from trading pool
        account.currentSupply += tokenAmount;
        account.tradingPool -= proceeds; // Sell proceeds come from trading pool
        account.liquidityPool -= proceeds; // Update total for compatibility
        account.balances[msg.sender] -= tokenAmount;
        
        // Distribute proceeds and fees
        userHypeBalances[msg.sender] += netProceeds;
        require(hypeToken.transfer(platformFeeWallet, platformFee), "Platform fee transfer failed");
        userHypeBalances[account.creator] += creatorFee;
        
        // Pay referral fee if applicable
        if (referralFee > 0 && userReferrer != address(0)) {
            userHypeBalances[userReferrer] += referralFee;
            referralEarnings[userReferrer] += referralFee;
            emit ReferralEarned(userReferrer, msg.sender, referralFee);
        }
        
        // Award points for selling tokens
        uint256 sellPoints = (proceeds * sellPointsMultiplier) / FEE_DENOMINATOR;
        userPoints[msg.sender] += sellPoints;
        tradingVolume[msg.sender] += proceeds;
        totalPointsDistributed += sellPoints;
        
        emit TokensSold(handle, msg.sender, tokenAmount, netProceeds);
        emit PointsEarned(msg.sender, sellPoints, "sell_tokens");
    }
    
    // Pricing based on trading pool only
    function calculateBuyPrice(string memory handle, uint256 tokenAmount) public view returns (uint256) {
        SocialAccount storage account = accounts[handle];
        uint256 circulatingSupply = INITIAL_TOKEN_SUPPLY - account.currentSupply;
        
        // Linear price: current_price = tradingPool / circulatingSupply
        uint256 currentPrice = (account.tradingPool * 1e18) / circulatingSupply;
        
        return (currentPrice * tokenAmount) / 1e18;
    }
    
    // Bonding curve pricing for selling (slightly discounted)
    function calculateSellPrice(string memory handle, uint256 tokenAmount) public view returns (uint256) {
        SocialAccount storage account = accounts[handle];
        uint256 circulatingSupply = INITIAL_TOKEN_SUPPLY - account.currentSupply;
        
        // Sell price is 95% of bonding curve price to prevent arbitrage
        uint256 bondingPrice = calculateBondingCurvePrice(circulatingSupply - tokenAmount, tokenAmount);
        return (bondingPrice * 9500) / 10000; // 5% discount for selling
    }
    
    // Users withdraw their HYPE balance
    function withdrawBalance() external {
        uint256 balance = userHypeBalances[msg.sender];
        require(balance > 0, "No balance");
        
        userHypeBalances[msg.sender] = 0;
        require(hypeToken.transfer(msg.sender, balance), "Transfer failed");
    }
    
    // Get user's token balance for specific account
    function getTokenBalance(string memory handle, address user) external view returns (uint256) {
        return accounts[handle].balances[user];
    }
    
    // Get account info
    function getAccountInfo(string memory handle) external view returns (
        address creator,
        uint256 totalSupply,
        uint256 currentSupply,
        uint256 liquidityPool,
        uint256 circulatingSupply
    ) {
        SocialAccount storage account = accounts[handle];
        require(account.exists, "Account doesn't exist");
        
        uint256 circulating = totalSupply - currentSupply;
        
        return (
            account.creator,
            account.totalSupply,
            account.currentSupply,
            account.liquidityPool,
            circulating
        );
    }
    
    // Get all launched accounts
    function getAllAccounts() external view returns (string[] memory) {
        return allAccounts;
    }
    
    // Get referral info
    function getReferralInfo(address user) external view returns (
        address referrer,
        uint256 totalEarnings,
        uint256 pendingBalance
    ) {
        return (
            referrers[user],
            referralEarnings[user],
            userHypeBalances[user]
        );
    }
    
    // Get user points and stats
    function getUserStats(address user) external view returns (
        uint256 points,
        uint256 volume,
        uint256 launched,
        uint256 referrals
    ) {
        return (
            userPoints[user],
            tradingVolume[user],
            accountsLaunched[user],
            referralCount[user]
        );
    }
    
    // Get leaderboard data (top 10 by points)
    function getTopUsers() external view returns (
        address[10] memory users,
        uint256[10] memory points
    ) {
        // Simple implementation - in production, use more efficient sorting
        // This is a basic version for demonstration
        
        // Note: This is a simplified version. In production, you'd want to
        // maintain a sorted list or use off-chain indexing for efficiency
        
        return (users, points); // Placeholder - implement proper sorting
    }
    
    // Emergency functions (Owner only)
    function pauseContract() external onlyOwner {
        paused = true;
    }
    
    function unpauseContract() external onlyOwner {
        paused = false;
    }
    
    // Emergency withdrawal for users only - Owner CANNOT withdraw trading funds
    function emergencyWithdrawUserFunds() external {
        require(paused, "Only available when paused");
        uint256 balance = userHypeBalances[msg.sender];
        require(balance > 0, "No balance to withdraw");
        
        userHypeBalances[msg.sender] = 0;
        require(hypeToken.transfer(msg.sender, balance), "Transfer failed");
        
        emit EmergencyWithdrawal(msg.sender, balance);
    }
    
    // Emergency sell tokens when paused (users can exit positions)
    function emergencySellTokens(string memory handle) external accountExists(handle) {
        require(paused, "Only available when paused");
        
        SocialAccount storage account = accounts[handle];
        uint256 userTokens = account.balances[msg.sender];
        require(userTokens > 0, "No tokens to sell");
        
        // Calculate fair exit price without fees during emergency
        uint256 circulatingSupply = INITIAL_TOKEN_SUPPLY - account.currentSupply;
        uint256 currentPrice = (account.liquidityPool * 1e18) / circulatingSupply;
        uint256 proceeds = (currentPrice * userTokens) / 1e18;
        
        require(account.liquidityPool >= proceeds, "Insufficient liquidity");
        
        // Update state
        account.currentSupply += userTokens;
        account.liquidityPool -= proceeds;
        account.balances[msg.sender] = 0;
        
        // Direct withdrawal to user
        require(hypeToken.transfer(msg.sender, proceeds), "Transfer failed");
        
        emit TokensSold(handle, msg.sender, userTokens, proceeds);
        emit EmergencyWithdrawal(msg.sender, proceeds);
    }
    
    // Update fees (Owner only, with limits)
    function updateFees(uint256 newPlatformFee, uint256 newCreatorFee, uint256 newReferralFee) external onlyOwner {
        require(newPlatformFee <= 500, "Platform fee too high"); // Max 5%
        require(newCreatorFee <= 200, "Creator fee too high");   // Max 2%
        require(newReferralFee <= 100, "Referral fee too high"); // Max 1%
        
        platformFeePercent = newPlatformFee;
        creatorFeePercent = newCreatorFee;
        referralFeePercent = newReferralFee;
    }
    
    // Update point multipliers (Owner only)
    function updatePointMultipliers(
        uint256 newBuyMultiplier,
        uint256 newSellMultiplier,
        uint256 newLaunchReward,
        uint256 newReferralReward
    ) external onlyOwner {
        require(newBuyMultiplier <= 1000, "Buy multiplier too high");     // Max 10%
        require(newSellMultiplier <= 500, "Sell multiplier too high");    // Max 5%
        require(newLaunchReward <= 100000, "Launch reward too high");     // Max 100k points
        require(newReferralReward <= 50000, "Referral reward too high");  // Max 50k points
        
        buyPointsMultiplier = newBuyMultiplier;
        sellPointsMultiplier = newSellMultiplier;
        launchPointsReward = newLaunchReward;
        referralPointsReward = newReferralReward;
    }
    
    // Update minimum launch deposit (Owner only)
    function updateMinimumLaunchDeposit(uint256 newMinimum) external onlyOwner {
        require(newMinimum > 0, "Minimum must be positive");
        require(newMinimum <= 100 * 1e18, "Maximum 100 HYPE"); // Cap at reasonable amount
        minimumLaunchDeposit = newMinimum;
    }
    
    // Owner can withdraw from ANY pool (platform has ultimate control)
    function ownerWithdrawFromTradingPool(string memory handle, uint256 amount) external onlyOwner {
        require(accounts[handle].exists, "Account doesn't exist");
        require(accounts[handle].tradingPool >= amount, "Insufficient trading pool");
        
        accounts[handle].tradingPool -= amount;
        accounts[handle].liquidityPool -= amount;
        require(hypeToken.transfer(msg.sender, amount), "Transfer failed");
        
        emit EmergencyWithdrawal(msg.sender, amount);
    }
    
    function ownerWithdrawFromCreatorPool(string memory handle, uint256 amount) external onlyOwner {
        require(accounts[handle].exists, "Account doesn't exist");
        require(accounts[handle].creatorPool >= amount, "Insufficient creator pool");
        
        accounts[handle].creatorPool -= amount;
        accounts[handle].liquidityPool -= amount;
        require(hypeToken.transfer(msg.sender, amount), "Transfer failed");
        
        emit EmergencyWithdrawal(msg.sender, amount);
    }
    
    function ownerWithdrawFromPlatformPool(string memory handle, uint256 amount) external onlyOwner {
        require(accounts[handle].exists, "Account doesn't exist");
        require(accounts[handle].platformPool >= amount, "Insufficient platform pool");
        
        accounts[handle].platformPool -= amount;
        accounts[handle].liquidityPool -= amount;
        require(hypeToken.transfer(msg.sender, amount), "Transfer failed");
        
        emit PlatformPoolWithdrawal(msg.sender, handle, amount);
    }
    
    // Owner can withdraw from ALL pools of any account
    function ownerWithdrawAllPools(string memory handle) external onlyOwner {
        require(accounts[handle].exists, "Account doesn't exist");
        
        SocialAccount storage account = accounts[handle];
        uint256 totalAmount = account.tradingPool + account.creatorPool + account.platformPool;
        require(totalAmount > 0, "No funds to withdraw");
        
        account.tradingPool = 0;
        account.creatorPool = 0;
        account.platformPool = 0;
        account.liquidityPool = 0;
        
        require(hypeToken.transfer(msg.sender, totalAmount), "Transfer failed");
        emit EmergencyWithdrawal(msg.sender, totalAmount);
    }
    
    // CREATORS HAVE NO SPECIAL WITHDRAWAL RIGHTS
    // Creators participate like regular users - they can only:
    // 1. Buy/sell tokens through normal trading functions
    // 2. Receive their initial token allocation during launch
    // 3. Earn trading fees that go to their personal HYPE balance (via userHypeBalances)
    
    // Creator pools accumulate fees but can only be accessed by platform owner
    // This ensures all funds stay in the ecosystem and creators profit through token appreciation
    
    // Owner can withdraw from multiple accounts at once
    function ownerWithdrawFromMultiple(string[] memory handles, uint256[] memory amounts) external onlyOwner {
        require(handles.length == amounts.length, "Array length mismatch");
        
        uint256 totalWithdrawal = 0;
        for (uint i = 0; i < handles.length; i++) {
            require(accounts[handles[i]].exists, "Account doesn't exist");
            require(accounts[handles[i]].liquidityPool >= amounts[i], "Insufficient liquidity");
            
            accounts[handles[i]].liquidityPool -= amounts[i];
            totalWithdrawal += amounts[i];
        }
        
        require(hypeToken.transfer(msg.sender, totalWithdrawal), "Transfer failed");
        emit EmergencyWithdrawal(msg.sender, totalWithdrawal);
    }
    
    // Transfer ownership
    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "Invalid address");
        owner = newOwner;
    }
}