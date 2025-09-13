// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "./SocialAccountToken.sol";

interface IERC20 {
    function transfer(address to, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

contract SocialTradingPlatform {
    address public owner;
    address public platformFeeWallet = 0xCbd45BE04C2CB52811609ef0334A9097fB2E2c48;
    IERC20 public hypeToken;
    bool public paused = false;
    
    // Fee percentages (basis points - 10000 = 100%)
    uint256 public platformFeePercent = 250;  // 2.5%
    uint256 public creatorFeePercent = 100;   // 1.0%
    uint256 public referralFeePercent = 50;   // 0.5%
    uint256 public constant FEE_DENOMINATOR = 10000;
    
    // Dynamic launch requirements
    uint256 public minimumLaunchDeposit = 1 * 1e16; // 0.01 HYPE
    uint256 public constant BASE_HYPE_DEPOSIT = 1 * 1e18; // 1 HYPE = base allocation
    uint256 public constant BASE_CREATOR_TOKENS = 3000000 * 1e18; // 3M tokens for 1 HYPE
    uint256 public constant TOTAL_SUPPLY = 1000000000 * 1e18; // 1B tokens
    
    mapping(string => address) public accountContracts; // handle => contract address
    mapping(address => uint256) public userHypeBalances;
    mapping(address => address) public referrers;
    
    // Points system (NON-TRANSFERABLE)
    mapping(address => uint256) public userPoints;
    mapping(address => uint256) public tradingVolume;
    mapping(address => uint256) public accountsLaunched;
    mapping(address => uint256) public referralCount;
    uint256 public totalPointsDistributed;
    
    // Point multipliers
    uint256 public buyPointsMultiplier = 100;    // 1% of trade value
    uint256 public sellPointsMultiplier = 50;    // 0.5% of trade value
    uint256 public launchPointsReward = 10000;   // 10,000 points
    uint256 public referralPointsReward = 20;    // 20 points per referral
    
    string[] public allAccounts;
    
    // Platform analytics tracking
    uint256 public totalVolumeAllTime;
    uint256 public totalFeesCollected;
    uint256 public lastResetTimestamp;
    mapping(uint256 => uint256) public dailyVolume;      // timestamp => volume
    mapping(uint256 => uint256) public dailyFees;        // timestamp => fees
    mapping(string => uint256) public accountHolderCount; // handle => unique holders
    mapping(string => mapping(address => bool)) public hasHeld; // handle => user => hasHeld
    
    event AccountLaunched(string indexed handle, address indexed creator, address contractAddress, uint256 initialDeposit);
    event TokensPurchased(string indexed handle, address indexed buyer, uint256 tokens, uint256 cost, uint256 platformFee);
    event TokensSold(string indexed handle, address indexed seller, uint256 tokens, uint256 proceeds, uint256 platformFee);
    event ReferralSet(address indexed user, address indexed referrer);
    event PointsEarned(address indexed user, uint256 points, string reason);
    event DailyStatsUpdated(uint256 date, uint256 volume, uint256 fees);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }
    
    modifier notPaused() {
        require(!paused, "Contract paused");
        _;
    }
    
    modifier accountExists(string memory handle) {
        require(accountContracts[handle] != address(0), "Account doesn't exist");
        _;
    }
    
    constructor(address _hypeToken) {
        owner = msg.sender;
        hypeToken = IERC20(_hypeToken);
        lastResetTimestamp = block.timestamp;
    }
    
    // Launch a new social account as tradeable asset
    function launchAccount(
        string memory handle,
        uint256 initialHypeDeposit,
        address referrer
    ) external notPaused {
        require(accountContracts[handle] == address(0), "Account already exists");
        require(initialHypeDeposit >= minimumLaunchDeposit, "Insufficient deposit");
        require(bytes(handle).length > 0, "Invalid handle");
        
        // Transfer HYPE from creator to this contract
        require(
            hypeToken.transferFrom(msg.sender, address(this), initialHypeDeposit),
            "HYPE transfer failed"
        );
        
        // Handle referral
        if (referrer != address(0) && referrers[msg.sender] == address(0) && referrer != msg.sender) {
            referrers[msg.sender] = referrer;
            referralCount[referrer]++;
            userPoints[referrer] += referralPointsReward;
            totalPointsDistributed += referralPointsReward;
            emit ReferralSet(msg.sender, referrer);
            emit PointsEarned(referrer, referralPointsReward, "referral");
        }
        
        // Calculate dynamic creator tokens
        uint256 creatorTokens = (initialHypeDeposit * BASE_CREATOR_TOKENS) / BASE_HYPE_DEPOSIT;
        uint256 maxCreatorTokens = TOTAL_SUPPLY / 2; // 50% cap
        if (creatorTokens > maxCreatorTokens) {
            creatorTokens = maxCreatorTokens;
        }
        
        // Deploy new account contract
        SocialAccountToken accountToken = new SocialAccountToken(
            address(this),
            msg.sender,
            handle,
            address(hypeToken),
            initialHypeDeposit,
            creatorTokens
        );
        
        // Transfer HYPE to the new contract
        require(hypeToken.transfer(address(accountToken), initialHypeDeposit), "Transfer to contract failed");
        
        accountContracts[handle] = address(accountToken);
        allAccounts.push(handle);
        
        // Award points for launching
        accountsLaunched[msg.sender]++;
        userPoints[msg.sender] += launchPointsReward;
        totalPointsDistributed += launchPointsReward;
        
        emit AccountLaunched(handle, msg.sender, address(accountToken), initialHypeDeposit);
        emit PointsEarned(msg.sender, launchPointsReward, "launch_account");
    }
    
    // Buy tokens from account
    function buyTokens(
        string memory handle,
        uint256 tokenAmount,
        uint256 maxCost
    ) external notPaused accountExists(handle) {
        require(tokenAmount > 0, "Invalid amount");
        
        SocialAccountToken accountToken = SocialAccountToken(accountContracts[handle]);
        require(tokenAmount <= accountToken.currentSupply(), "Insufficient supply");
        
        uint256 cost = accountToken.calculateBuyPrice(tokenAmount);
        require(cost <= maxCost, "Slippage too high");
        
        // Calculate fees
        uint256 platformFee = (cost * platformFeePercent) / FEE_DENOMINATOR;
        uint256 creatorFee = (cost * creatorFeePercent) / FEE_DENOMINATOR;
        uint256 referralFee = 0;
        
        address userReferrer = referrers[msg.sender];
        if (userReferrer != address(0)) {
            referralFee = (cost * referralFeePercent) / FEE_DENOMINATOR;
            platformFee -= referralFee;
        }
        
        uint256 totalCost = cost + platformFee + creatorFee + referralFee;
        
        // Transfer HYPE from buyer
        require(hypeToken.transferFrom(msg.sender, address(this), totalCost), "HYPE transfer failed");
        
        // Distribute fees
        require(hypeToken.transfer(platformFeeWallet, platformFee), "Platform fee transfer failed");
        userHypeBalances[accountToken.creator()] += creatorFee;
        if (referralFee > 0 && userReferrer != address(0)) {
            userHypeBalances[userReferrer] += referralFee;
        }
        
        // Transfer cost to account contract and execute buy
        require(hypeToken.transfer(address(accountToken), cost), "Transfer to account failed");
        accountToken.buyTokens(msg.sender, tokenAmount, cost);
        
        // Award points
        uint256 buyPoints = (cost * buyPointsMultiplier) / FEE_DENOMINATOR;
        userPoints[msg.sender] += buyPoints;
        tradingVolume[msg.sender] += cost;
        totalPointsDistributed += buyPoints;
        
        // Update analytics
        _updateDailyStats(cost, platformFee);
        _updateHolderCount(handle, msg.sender);
        
        emit TokensPurchased(handle, msg.sender, tokenAmount, cost, platformFee);
        emit PointsEarned(msg.sender, buyPoints, "buy_tokens");
    }
    
    // Sell tokens to account
    function sellTokens(
        string memory handle,
        uint256 tokenAmount,
        uint256 minProceeds
    ) external notPaused accountExists(handle) {
        require(tokenAmount > 0, "Invalid amount");
        
        SocialAccountToken accountToken = SocialAccountToken(accountContracts[handle]);
        require(accountToken.balances(msg.sender) >= tokenAmount, "Insufficient tokens");
        
        uint256 proceeds = accountToken.calculateSellPrice(tokenAmount);
        require(proceeds >= minProceeds, "Slippage too high");
        
        // Calculate fees
        uint256 platformFee = (proceeds * platformFeePercent) / FEE_DENOMINATOR;
        uint256 creatorFee = (proceeds * creatorFeePercent) / FEE_DENOMINATOR;
        uint256 referralFee = 0;
        
        address userReferrer = referrers[msg.sender];
        if (userReferrer != address(0)) {
            referralFee = (proceeds * referralFeePercent) / FEE_DENOMINATOR;
            platformFee -= referralFee;
        }
        
        uint256 netProceeds = proceeds - platformFee - creatorFee - referralFee;
        
        // Execute sell on account contract
        accountToken.sellTokens(msg.sender, tokenAmount, proceeds);
        
        // Withdraw proceeds from account contract
        accountToken.withdrawLiquidity(proceeds);
        
        // Distribute proceeds and fees
        userHypeBalances[msg.sender] += netProceeds;
        require(hypeToken.transfer(platformFeeWallet, platformFee), "Platform fee transfer failed");
        userHypeBalances[accountToken.creator()] += creatorFee;
        if (referralFee > 0 && userReferrer != address(0)) {
            userHypeBalances[userReferrer] += referralFee;
        }
        
        // Award points
        uint256 sellPoints = (proceeds * sellPointsMultiplier) / FEE_DENOMINATOR;
        userPoints[msg.sender] += sellPoints;
        tradingVolume[msg.sender] += proceeds;
        totalPointsDistributed += sellPoints;
        
        // Update analytics
        _updateDailyStats(totalProceeds, platformFee);
        
        emit TokensSold(handle, msg.sender, tokenAmount, netProceeds, platformFee);
        emit PointsEarned(msg.sender, sellPoints, "sell_tokens");
    }
    
    // Platform owner can withdraw from any account's liquidity pool
    function withdrawAccountLiquidity(string memory handle, uint256 amount) external onlyOwner {
        require(accountContracts[handle] != address(0), "Account doesn't exist");
        
        SocialAccountToken accountToken = SocialAccountToken(accountContracts[handle]);
        accountToken.withdrawLiquidity(amount);
    }
    
    // Platform owner can withdraw ALL liquidity from ALL accounts in 1 click
    function withdrawAllLiquidity() external onlyOwner {
        uint256 totalWithdrawn = 0;
        
        for (uint256 i = 0; i < allAccounts.length; i++) {
            string memory handle = allAccounts[i];
            SocialAccountToken accountToken = SocialAccountToken(accountContracts[handle]);
            
            uint256 availableLiquidity = accountToken.liquidityPool();
            if (availableLiquidity > 0) {
                accountToken.withdrawLiquidity(availableLiquidity);
                totalWithdrawn += availableLiquidity;
            }
        }
        
        // All HYPE now in platform contract, owner can withdraw
        if (totalWithdrawn > 0) {
            require(hypeToken.transfer(msg.sender, totalWithdrawn), "Transfer failed");
        }
    }
    
    // Platform owner can withdraw specific percentage from all accounts
    function withdrawPercentageFromAll(uint256 percentage) external onlyOwner {
        require(percentage <= 100, "Percentage too high");
        uint256 totalWithdrawn = 0;
        
        for (uint256 i = 0; i < allAccounts.length; i++) {
            string memory handle = allAccounts[i];
            SocialAccountToken accountToken = SocialAccountToken(accountContracts[handle]);
            
            uint256 availableLiquidity = accountToken.liquidityPool();
            if (availableLiquidity > 0) {
                uint256 withdrawAmount = (availableLiquidity * percentage) / 100;
                if (withdrawAmount > 0) {
                    accountToken.withdrawLiquidity(withdrawAmount);
                    totalWithdrawn += withdrawAmount;
                }
            }
        }
        
        if (totalWithdrawn > 0) {
            require(hypeToken.transfer(msg.sender, totalWithdrawn), "Transfer failed");
        }
    }
    
    // Users withdraw their HYPE balance
    function withdrawBalance() external {
        uint256 balance = userHypeBalances[msg.sender];
        require(balance > 0, "No balance");
        
        userHypeBalances[msg.sender] = 0;
        require(hypeToken.transfer(msg.sender, balance), "Transfer failed");
    }
    
    // Emergency pause/unpause
    function pauseContract() external onlyOwner {
        paused = true;
    }
    
    function unpauseContract() external onlyOwner {
        paused = false;
    }
    
    // Get all accounts
    function getAllAccounts() external view returns (string[] memory) {
        return allAccounts;
    }
    
    // Get account contract address
    function getAccountContract(string memory handle) external view returns (address) {
        return accountContracts[handle];
    }
    
    // Internal helper functions for analytics
    function _updateDailyStats(uint256 volume, uint256 fees) internal {
        uint256 today = block.timestamp / 86400; // Current day
        dailyVolume[today] += volume;
        dailyFees[today] += fees;
        totalVolumeAllTime += volume;
        totalFeesCollected += fees;
        
        emit DailyStatsUpdated(today, dailyVolume[today], dailyFees[today]);
    }
    
    function _updateHolderCount(string memory handle, address user) internal {
        if (!hasHeld[handle][user]) {
            hasHeld[handle][user] = true;
            accountHolderCount[handle]++;
        }
    }
    
    // Analytics view functions for frontend
    function getPlatformStats() external view returns (
        uint256 totalVolume24h,
        uint256 totalFees24h,
        uint256 activeAccountsCount,
        uint256 totalHolders,
        uint256 platformTVL
    ) {
        uint256 today = block.timestamp / 86400;
        totalVolume24h = dailyVolume[today];
        totalFees24h = dailyFees[today];
        activeAccountsCount = allAccounts.length;
        
        // Calculate total unique holders across all accounts
        for (uint256 i = 0; i < allAccounts.length; i++) {
            totalHolders += accountHolderCount[allAccounts[i]];
        }
        
        // Calculate total TVL (all liquidity pools combined)
        for (uint256 i = 0; i < allAccounts.length; i++) {
            string memory handle = allAccounts[i];
            SocialAccountToken accountToken = SocialAccountToken(accountContracts[handle]);
            platformTVL += accountToken.liquidityPool();
        }
    }
    
    function getAccountStats(string memory handle) external view returns (
        uint256 holders,
        uint256 totalSupply,
        uint256 currentPrice,
        uint256 liquidityPool,
        uint256 marketCap,
        address creator,
        uint256 creatorBalance
    ) {
        require(accountContracts[handle] != address(0), "Account doesn't exist");
        
        SocialAccountToken accountToken = SocialAccountToken(accountContracts[handle]);
        holders = accountHolderCount[handle];
        totalSupply = accountToken.totalSupply();
        currentPrice = accountToken.getCurrentPrice();
        liquidityPool = accountToken.liquidityPool();
        marketCap = (totalSupply * currentPrice) / 1e18;
        creator = accountToken.creator();
        
        // Get creator's token balance
        creatorBalance = accountToken.balanceOf(creator);
    }
    
    function getDailyStats(uint256 daysBack) external view returns (
        uint256[] memory volumes,
        uint256[] memory fees,
        uint256[] memory dates
    ) {
        volumes = new uint256[](daysBack);
        fees = new uint256[](daysBack);
        dates = new uint256[](daysBack);
        
        uint256 today = block.timestamp / 86400;
        
        for (uint256 i = 0; i < daysBack; i++) {
            uint256 date = today - i;
            volumes[i] = dailyVolume[date];
            fees[i] = dailyFees[date];
            dates[i] = date;
        }
    }
}