// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title SocialAccountToken
 * @dev Individual contract for each X account token with its own liquidity pool
 */
contract SocialAccountToken is ReentrancyGuard {
    string public handle;
    address public creator;
    address public factory;
    address public platformFeeWallet;
    IERC20 public hypeToken;
    
    // Token economics
    uint256 public constant TOTAL_SUPPLY = 1000000000 * 1e18; // 1B tokens
    uint256 public constant CREATOR_ALLOCATION = 3000000 * 1e18; // 3M tokens to creator
    uint256 public currentSupply = TOTAL_SUPPLY - CREATOR_ALLOCATION; // 997M available
    
    // Separate pools for this account
    uint256 public tradingPool;    // 70% - HYPE for buy/sell operations
    uint256 public creatorPool;    // 20% - HYPE reserved for creator fees
    uint256 public platformPool;   // 10% - HYPE for platform fees
    
    // Fee structure (basis points)
    uint256 public constant PLATFORM_FEE = 250; // 2.5%
    uint256 public constant CREATOR_FEE = 100;   // 1.0%
    uint256 public constant REFERRAL_FEE = 50;   // 0.5%
    uint256 public constant FEE_DENOMINATOR = 10000;
    
    // Token balances
    mapping(address => uint256) public balances;
    mapping(address => uint256) public userHypeBalances;
    
    // Pool allocation percentages
    uint256 public constant TRADING_POOL_PERCENT = 70;
    uint256 public constant CREATOR_POOL_PERCENT = 20;
    uint256 public constant PLATFORM_POOL_PERCENT = 10;
    
    bool public paused = false;
    
    // Events
    event TokensPurchased(address indexed buyer, uint256 tokens, uint256 cost);
    event TokensSold(address indexed seller, uint256 tokens, uint256 proceeds);
    event PoolWithdrawal(address indexed user, string poolType, uint256 amount);
    
    modifier onlyFactory() {
        require(msg.sender == factory, "Only factory can call");
        _;
    }
    
    modifier onlyCreator() {
        require(msg.sender == creator, "Only creator can call");
        _;
    }
    
    modifier notPaused() {
        require(!paused, "Contract paused");
        _;
    }
    
    constructor(
        string memory _handle,
        address _creator,
        address _factory,
        address _platformFeeWallet,
        address _hypeToken,
        uint256 _initialDeposit
    ) {
        handle = _handle;
        creator = _creator;
        factory = _factory;
        platformFeeWallet = _platformFeeWallet;
        hypeToken = IERC20(_hypeToken);
        
        // Allocate pools from initial deposit
        tradingPool = (_initialDeposit * TRADING_POOL_PERCENT) / 100;    // 70%
        creatorPool = (_initialDeposit * CREATOR_POOL_PERCENT) / 100;    // 20%
        platformPool = (_initialDeposit * PLATFORM_POOL_PERCENT) / 100;  // 10%
        
        // Give creator their initial tokens
        balances[_creator] = CREATOR_ALLOCATION;
    }
    
    /**
     * @dev Buy tokens with linear pricing based on trading pool
     */
    function buyTokens(uint256 tokenAmount, address referrer) external nonReentrant notPaused {
        require(tokenAmount > 0, "Invalid token amount");
        require(currentSupply >= tokenAmount, "Insufficient supply");
        
        uint256 cost = calculateBuyPrice(tokenAmount);
        require(cost > 0, "Invalid cost");
        
        // Transfer HYPE from buyer
        require(hypeToken.transferFrom(msg.sender, address(this), cost), "HYPE transfer failed");
        
        // Calculate fees
        uint256 platformFee = (cost * PLATFORM_FEE) / FEE_DENOMINATOR;
        uint256 creatorFee = (cost * CREATOR_FEE) / FEE_DENOMINATOR;
        uint256 referralFee = referrer != address(0) ? (cost * REFERRAL_FEE) / FEE_DENOMINATOR : 0;
        uint256 netCost = cost - platformFee - creatorFee - referralFee;
        
        // Distribute fees
        if (platformFee > 0) {
            require(hypeToken.transfer(platformFeeWallet, platformFee), "Platform fee transfer failed");
        }
        if (creatorFee > 0) {
            userHypeBalances[creator] += creatorFee;
        }
        if (referralFee > 0 && referrer != address(0)) {
            userHypeBalances[referrer] += referralFee;
        }
        
        // Distribute remaining cost to pools
        uint256 toTradingPool = (netCost * 80) / 100;    // 80%
        uint256 toPlatformPool = (netCost * 15) / 100;   // 15%
        uint256 toCreatorPool = (netCost * 5) / 100;     // 5%
        
        tradingPool += toTradingPool;
        platformPool += toPlatformPool;
        creatorPool += toCreatorPool;
        
        // Update token balances
        currentSupply -= tokenAmount;
        balances[msg.sender] += tokenAmount;
        
        emit TokensPurchased(msg.sender, tokenAmount, cost);
    }
    
    /**
     * @dev Sell tokens back to trading pool
     */
    function sellTokens(uint256 tokenAmount, address referrer) external nonReentrant notPaused {
        require(tokenAmount > 0, "Invalid token amount");
        require(balances[msg.sender] >= tokenAmount, "Insufficient balance");
        
        uint256 proceeds = calculateSellPrice(tokenAmount);
        require(tradingPool >= proceeds, "Insufficient trading pool");
        
        // Calculate fees
        uint256 platformFee = (proceeds * PLATFORM_FEE) / FEE_DENOMINATOR;
        uint256 creatorFee = (proceeds * CREATOR_FEE) / FEE_DENOMINATOR;
        uint256 referralFee = referrer != address(0) ? (proceeds * REFERRAL_FEE) / FEE_DENOMINATOR : 0;
        uint256 netProceeds = proceeds - platformFee - creatorFee - referralFee;
        
        // Update pools and balances
        tradingPool -= proceeds;
        currentSupply += tokenAmount;
        balances[msg.sender] -= tokenAmount;
        
        // Transfer proceeds and fees
        require(hypeToken.transfer(msg.sender, netProceeds), "Proceeds transfer failed");
        
        if (platformFee > 0) {
            require(hypeToken.transfer(platformFeeWallet, platformFee), "Platform fee transfer failed");
        }
        if (creatorFee > 0) {
            userHypeBalances[creator] += creatorFee;
        }
        if (referralFee > 0 && referrer != address(0)) {
            userHypeBalances[referrer] += referralFee;
        }
        
        emit TokensSold(msg.sender, tokenAmount, netProceeds);
    }
    
    /**
     * @dev Calculate buy price based on linear pricing
     */
    function calculateBuyPrice(uint256 tokenAmount) public view returns (uint256) {
        uint256 circulatingSupply = TOTAL_SUPPLY - currentSupply;
        if (circulatingSupply == 0) return 0;
        
        uint256 currentPrice = (tradingPool * 1e18) / circulatingSupply;
        return (currentPrice * tokenAmount) / 1e18;
    }
    
    /**
     * @dev Calculate sell price based on linear pricing
     */
    function calculateSellPrice(uint256 tokenAmount) public view returns (uint256) {
        uint256 circulatingSupply = TOTAL_SUPPLY - currentSupply;
        if (circulatingSupply == 0) return 0;
        
        uint256 currentPrice = (tradingPool * 1e18) / circulatingSupply;
        return (currentPrice * tokenAmount) / 1e18;
    }
    
    /**
     * @dev Factory can withdraw from any pool (platform control)
     */
    function factoryWithdrawFromPool(string memory poolType, uint256 amount) external onlyFactory {
        if (keccak256(abi.encodePacked(poolType)) == keccak256(abi.encodePacked("trading"))) {
            require(tradingPool >= amount, "Insufficient trading pool");
            tradingPool -= amount;
        } else if (keccak256(abi.encodePacked(poolType)) == keccak256(abi.encodePacked("creator"))) {
            require(creatorPool >= amount, "Insufficient creator pool");
            creatorPool -= amount;
        } else if (keccak256(abi.encodePacked(poolType)) == keccak256(abi.encodePacked("platform"))) {
            require(platformPool >= amount, "Insufficient platform pool");
            platformPool -= amount;
        } else {
            revert("Invalid pool type");
        }
        
        require(hypeToken.transfer(factory, amount), "Withdrawal failed");
        emit PoolWithdrawal(factory, poolType, amount);
    }
    
    /**
     * @dev Factory can withdraw all funds from this account
     */
    function factoryWithdrawAll() external onlyFactory {
        uint256 totalAmount = tradingPool + creatorPool + platformPool;
        require(totalAmount > 0, "No funds to withdraw");
        
        tradingPool = 0;
        creatorPool = 0;
        platformPool = 0;
        
        require(hypeToken.transfer(factory, totalAmount), "Withdrawal failed");
        emit PoolWithdrawal(factory, "all", totalAmount);
    }
    
    /**
     * @dev Users can withdraw their HYPE balance
     */
    function withdrawHypeBalance() external nonReentrant {
        uint256 balance = userHypeBalances[msg.sender];
        require(balance > 0, "No balance to withdraw");
        
        userHypeBalances[msg.sender] = 0;
        require(hypeToken.transfer(msg.sender, balance), "Withdrawal failed");
    }
    
    /**
     * @dev Factory can pause/unpause this account
     */
    function setPaused(bool _paused) external onlyFactory {
        paused = _paused;
    }
    
    /**
     * @dev Get current price per token
     */
    function getCurrentPrice() external view returns (uint256) {
        uint256 circulatingSupply = TOTAL_SUPPLY - currentSupply;
        if (circulatingSupply == 0) return 0;
        return (tradingPool * 1e18) / circulatingSupply;
    }
    
    /**
     * @dev Get market cap
     */
    function getMarketCap() external view returns (uint256) {
        uint256 currentPrice = this.getCurrentPrice();
        uint256 circulatingSupply = TOTAL_SUPPLY - currentSupply;
        return (currentPrice * circulatingSupply) / 1e18;
    }
    
    /**
     * @dev Get pool balances
     */
    function getPoolBalances() external view returns (uint256, uint256, uint256) {
        return (tradingPool, creatorPool, platformPool);
    }
}