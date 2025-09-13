// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./SocialAccountToken.sol";

/**
 * @title SocialXTradingFactory
 * @dev Factory contract that deploys individual SocialAccountToken contracts for each X account
 */
contract SocialXTradingFactory {
    address public owner;
    address public platformFeeWallet;
    IERC20 public hypeToken;
    bool public paused = false;
    
    // Minimum deposit requirements
    uint256 public minimumLaunchDeposit = 1 * 1e18; // 1 HYPE minimum
    
    // Track all deployed accounts
    mapping(string => address) public accountContracts; // handle => contract address
    mapping(address => string) public contractToHandle; // contract => handle
    string[] public allHandles;
    
    // User stats for gamification
    mapping(address => uint256) public userPoints;
    mapping(address => uint256) public tradingVolume;
    mapping(address => uint256) public accountsLaunched;
    mapping(address => uint256) public referralCount;
    mapping(address => address) public referrers; // user => referrer
    mapping(address => uint256) public referralEarnings;
    
    // Points multipliers
    uint256 public buyPointsMultiplier = 100;      // 1% of trade value in points
    uint256 public sellPointsMultiplier = 50;      // 0.5% of trade value in points
    uint256 public launchPointsReward = 10000;     // 10,000 points for launching
    uint256 public referralPointsReward = 20;      // 20 points per referral
    
    uint256 public totalPointsDistributed;
    
    // Events
    event AccountLaunched(string indexed handle, address indexed creator, address contractAddress, uint256 initialDeposit);
    event DeveloperTokensAllocated(string indexed handle, address indexed creator, uint256 tokens, uint256 hypeDeposit);
    event PointsEarned(address indexed user, uint256 points, string reason);
    event ReferralSet(address indexed user, address indexed referrer);
    event BatchPoolWithdrawal(address indexed owner, uint256 totalAmount);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }
    
    modifier notPaused() {
        require(!paused, "Factory paused");
        _;
    }
    
    constructor(address _hypeToken, address _platformFeeWallet) {
        owner = msg.sender;
        hypeToken = IERC20(_hypeToken);
        platformFeeWallet = _platformFeeWallet;
    }
    
    /**
     * @dev Launch a new X account token with its own contract and pools
     */
    function launchAccount(string memory handle, uint256 initialHypeDeposit, address referrer) external notPaused {
        require(bytes(handle).length > 0, "Invalid handle");
        require(accountContracts[handle] == address(0), "Account already exists");
        require(initialHypeDeposit >= minimumLaunchDeposit, "Insufficient deposit");
        
        // Transfer HYPE from creator to factory
        require(hypeToken.transferFrom(msg.sender, address(this), initialHypeDeposit), "HYPE transfer failed");
        
        // Deploy new SocialAccountToken contract
        SocialAccountToken accountToken = new SocialAccountToken(
            handle,
            msg.sender,
            address(this),
            platformFeeWallet,
            address(hypeToken),
            initialHypeDeposit
        );
        
        // Transfer HYPE to the new account contract
        require(hypeToken.transfer(address(accountToken), initialHypeDeposit), "Transfer to account failed");
        
        // Register the new account
        accountContracts[handle] = address(accountToken);
        contractToHandle[address(accountToken)] = handle;
        allHandles.push(handle);
        
        // Handle referral system
        if (referrer != address(0) && referrer != msg.sender) {
            if (referrers[msg.sender] == address(0)) {
                referrers[msg.sender] = referrer;
                referralCount[referrer]++;
                userPoints[referrer] += referralPointsReward;
                totalPointsDistributed += referralPointsReward;
                
                emit ReferralSet(msg.sender, referrer);
                emit PointsEarned(referrer, referralPointsReward, "referral");
            }
        }
        
        // Award points and update stats
        accountsLaunched[msg.sender]++;
        userPoints[msg.sender] += launchPointsReward;
        totalPointsDistributed += launchPointsReward;
        
        emit AccountLaunched(handle, msg.sender, address(accountToken), initialHypeDeposit);
        emit DeveloperTokensAllocated(handle, msg.sender, 3000000 * 1e18, initialHypeDeposit);
        emit PointsEarned(msg.sender, launchPointsReward, "launch_account");
    }
    
    /**
     * @dev Buy tokens from a specific account contract
     */
    function buyTokens(string memory handle, uint256 tokenAmount, address referrer) external notPaused {
        address accountContract = accountContracts[handle];
        require(accountContract != address(0), "Account doesn't exist");
        
        // Get cost from account contract
        uint256 cost = SocialAccountToken(accountContract).calculateBuyPrice(tokenAmount);
        require(cost > 0, "Invalid cost");
        
        // Transfer HYPE from buyer to account contract
        require(hypeToken.transferFrom(msg.sender, accountContract, cost), "HYPE transfer failed");
        
        // Call buyTokens on the account contract
        SocialAccountToken(accountContract).buyTokens(tokenAmount, referrer);
        
        // Award points and update stats
        uint256 points = (cost * buyPointsMultiplier) / 10000;
        userPoints[msg.sender] += points;
        tradingVolume[msg.sender] += cost;
        totalPointsDistributed += points;
        
        emit PointsEarned(msg.sender, points, "buy_tokens");
    }
    
    /**
     * @dev Sell tokens to a specific account contract
     */
    function sellTokens(string memory handle, uint256 tokenAmount, address referrer) external notPaused {
        address accountContract = accountContracts[handle];
        require(accountContract != address(0), "Account doesn't exist");
        
        // Get proceeds from account contract
        uint256 proceeds = SocialAccountToken(accountContract).calculateSellPrice(tokenAmount);
        require(proceeds > 0, "Invalid proceeds");
        
        // Call sellTokens on the account contract
        SocialAccountToken(accountContract).sellTokens(tokenAmount, referrer);
        
        // Award points and update stats
        uint256 points = (proceeds * sellPointsMultiplier) / 10000;
        userPoints[msg.sender] += points;
        tradingVolume[msg.sender] += proceeds;
        totalPointsDistributed += points;
        
        emit PointsEarned(msg.sender, points, "sell_tokens");
    }
    
    /**
     * @dev Owner can withdraw from any account's pools
     */
    function withdrawFromAccountPool(string memory handle, string memory poolType, uint256 amount) external onlyOwner {
        address accountContract = accountContracts[handle];
        require(accountContract != address(0), "Account doesn't exist");
        
        SocialAccountToken(accountContract).factoryWithdrawFromPool(poolType, amount);
    }
    
    /**
     * @dev Owner can withdraw all funds from any account
     */
    function withdrawAllFromAccount(string memory handle) external onlyOwner {
        address accountContract = accountContracts[handle];
        require(accountContract != address(0), "Account doesn't exist");
        
        SocialAccountToken(accountContract).factoryWithdrawAll();
    }
    
    /**
     * @dev Owner can withdraw from multiple accounts at once
     */
    function batchWithdrawFromAccounts(string[] memory handles, string[] memory poolTypes, uint256[] memory amounts) external onlyOwner {
        require(handles.length == poolTypes.length && handles.length == amounts.length, "Array length mismatch");
        
        uint256 totalWithdrawn = 0;
        
        for (uint i = 0; i < handles.length; i++) {
            address accountContract = accountContracts[handles[i]];
            require(accountContract != address(0), "Account doesn't exist");
            
            uint256 beforeBalance = hypeToken.balanceOf(address(this));
            SocialAccountToken(accountContract).factoryWithdrawFromPool(poolTypes[i], amounts[i]);
            uint256 afterBalance = hypeToken.balanceOf(address(this));
            
            totalWithdrawn += (afterBalance - beforeBalance);
        }
        
        emit BatchPoolWithdrawal(msg.sender, totalWithdrawn);
    }
    
    /**
     * @dev Owner can pause/unpause individual accounts
     */
    function pauseAccount(string memory handle, bool _paused) external onlyOwner {
        address accountContract = accountContracts[handle];
        require(accountContract != address(0), "Account doesn't exist");
        
        SocialAccountToken(accountContract).setPaused(_paused);
    }
    
    /**
     * @dev Owner can pause/unpause the entire factory
     */
    function setPaused(bool _paused) external onlyOwner {
        paused = _paused;
    }
    
    /**
     * @dev Update minimum launch deposit
     */
    function updateMinimumLaunchDeposit(uint256 newMinimum) external onlyOwner {
        require(newMinimum > 0, "Invalid minimum");
        minimumLaunchDeposit = newMinimum;
    }
    
    /**
     * @dev Update points multipliers
     */
    function updatePointsMultipliers(
        uint256 _buyPointsMultiplier,
        uint256 _sellPointsMultiplier,
        uint256 _launchPointsReward,
        uint256 _referralPointsReward
    ) external onlyOwner {
        buyPointsMultiplier = _buyPointsMultiplier;
        sellPointsMultiplier = _sellPointsMultiplier;
        launchPointsReward = _launchPointsReward;
        referralPointsReward = _referralPointsReward;
    }
    
    /**
     * @dev Get account contract address
     */
    function getAccountContract(string memory handle) external view returns (address) {
        return accountContracts[handle];
    }
    
    /**
     * @dev Get account info from contract
     */
    function getAccountInfo(string memory handle) external view returns (
        uint256 currentPrice,
        uint256 marketCap,
        uint256 tradingPool,
        uint256 creatorPool,
        uint256 platformPool,
        uint256 currentSupply
    ) {
        address accountContract = accountContracts[handle];
        require(accountContract != address(0), "Account doesn't exist");
        
        SocialAccountToken token = SocialAccountToken(accountContract);
        currentPrice = token.getCurrentPrice();
        marketCap = token.getMarketCap();
        (tradingPool, creatorPool, platformPool) = token.getPoolBalances();
        currentSupply = token.currentSupply();
    }
    
    /**
     * @dev Get user's token balance for specific account
     */
    function getUserTokenBalance(string memory handle, address user) external view returns (uint256) {
        address accountContract = accountContracts[handle];
        require(accountContract != address(0), "Account doesn't exist");
        
        return SocialAccountToken(accountContract).balances(user);
    }
    
    /**
     * @dev Get all launched handles
     */
    function getAllHandles() external view returns (string[] memory) {
        return allHandles;
    }
    
    /**
     * @dev Get user stats
     */
    function getUserStats(address user) external view returns (
        uint256 points,
        uint256 volume,
        uint256 launched,
        uint256 referrals,
        address referrer
    ) {
        return (
            userPoints[user],
            tradingVolume[user],
            accountsLaunched[user],
            referralCount[user],
            referrers[user]
        );
    }
}