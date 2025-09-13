// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

/**
 * @title SocialXTrading
 * @dev Social trading platform for X (Twitter) accounts as tradeable assets
 * Features: Bonding curve pricing, trading fees, slippage protection, emergency controls
 */
contract SocialXTrading is Ownable, ReentrancyGuard, Pausable {
    
    // State variables
    IERC20 public immutable HYPE_TOKEN;
    
    // Platform settings
    uint256 public constant PROTOCOL_FEE = 250; // 2.5% (250/10000)
    uint256 public constant CREATOR_FEE = 100;  // 1% (100/10000)
    uint256 public constant SLIPPAGE_TOLERANCE = 500; // 5% max slippage
    uint256 public constant FEE_DENOMINATOR = 10000;
    
    // Bonding curve parameters
    uint256 public constant CURVE_STEEPNESS = 16000; // Controls price curve steepness
    uint256 public constant BASE_PRICE = 1e15; // 0.001 HYPE minimum price
    
    // Social account structure
    struct SocialAccount {
        string handle;          // X handle
        address creator;        // Account creator
        uint256 totalSupply;    // Total tokens minted
        uint256 marketCap;      // Current market cap in HYPE
        uint256 volume24h;      // 24h trading volume
        bool isActive;          // Account status
        uint256 createdAt;      // Launch timestamp
        mapping(address => uint256) balances; // User token holdings
    }
    
    // Account registry
    mapping(bytes32 => SocialAccount) public socialAccounts;
    mapping(string => bytes32) public handleToId;
    bytes32[] public accountIds;
    
    // Trading history
    struct Trade {
        address trader;
        bytes32 accountId;
        uint256 amount;
        uint256 price;
        uint256 hyfeSpent;
        bool isBuy;
        uint256 timestamp;
    }
    
    Trade[] public trades;
    mapping(address => uint256[]) public userTrades;
    
    // Fee collection
    uint256 public protocolFeesCollected;
    mapping(address => uint256) public creatorFeesEarned;
    
    // Events
    event AccountLaunched(bytes32 indexed accountId, string handle, address creator);
    event TokensBought(bytes32 indexed accountId, address buyer, uint256 amount, uint256 hyfeSpent);
    event TokensSold(bytes32 indexed accountId, address seller, uint256 amount, uint256 hyfeReceived);
    event FeesCollected(address recipient, uint256 amount);
    event EmergencyWithdrawal(address token, uint256 amount);
    
    // Modifiers
    modifier accountExists(bytes32 accountId) {
        require(socialAccounts[accountId].isActive, "Account not found");
        _;
    }
    
    modifier validSlippage(uint256 expectedPrice, uint256 actualPrice, bool isBuy) {
        if (isBuy) {
            require(actualPrice <= expectedPrice * (FEE_DENOMINATOR + SLIPPAGE_TOLERANCE) / FEE_DENOMINATOR, "Price slippage too high");
        } else {
            require(actualPrice >= expectedPrice * (FEE_DENOMINATOR - SLIPPAGE_TOLERANCE) / FEE_DENOMINATOR, "Price slippage too high");
        }
        _;
    }
    
    constructor(address _hyfeToken) {
        HYPE_TOKEN = IERC20(_hyfeToken);
    }
    
    /**
     * @dev Launch a new social account as tradeable asset
     */
    function launchAccount(
        string calldata handle,
        uint256 initialBuyAmount
    ) external nonReentrant whenNotPaused {
        require(bytes(handle).length > 0, "Handle required");
        require(handleToId[handle] == bytes32(0), "Handle already exists");
        require(initialBuyAmount > 0, "Initial buy required");
        
        // Generate unique account ID
        bytes32 accountId = keccak256(abi.encodePacked(handle, msg.sender, block.timestamp));
        
        // Initialize account
        SocialAccount storage account = socialAccounts[accountId];
        account.handle = handle;
        account.creator = msg.sender;
        account.isActive = true;
        account.createdAt = block.timestamp;
        
        // Register account
        handleToId[handle] = accountId;
        accountIds.push(accountId);
        
        emit AccountLaunched(accountId, handle, msg.sender);
        
        // Execute initial buy
        _buyTokens(accountId, initialBuyAmount, type(uint256).max);
    }
    
    /**
     * @dev Buy tokens for a social account
     */
    function buyTokens(
        bytes32 accountId,
        uint256 hyfeAmount,
        uint256 maxPricePerToken
    ) external nonReentrant whenNotPaused accountExists(accountId) {
        _buyTokens(accountId, hyfeAmount, maxPricePerToken);
    }
    
    /**
     * @dev Sell tokens for a social account
     */
    function sellTokens(
        bytes32 accountId,
        uint256 tokenAmount,
        uint256 minPricePerToken
    ) external nonReentrant whenNotPaused accountExists(accountId) {
        require(tokenAmount > 0, "Amount required");
        require(socialAccounts[accountId].balances[msg.sender] >= tokenAmount, "Insufficient balance");
        
        uint256 hyfeReceived = calculateSellReturn(accountId, tokenAmount);
        uint256 pricePerToken = hyfeReceived * 1e18 / tokenAmount;
        
        require(pricePerToken >= minPricePerToken, "Price below minimum");
        
        // Calculate fees
        uint256 protocolFee = hyfeReceived * PROTOCOL_FEE / FEE_DENOMINATOR;
        uint256 creatorFee = hyfeReceived * CREATOR_FEE / FEE_DENOMINATOR;
        uint256 netAmount = hyfeReceived - protocolFee - creatorFee;
        
        // Update state
        SocialAccount storage account = socialAccounts[accountId];
        account.balances[msg.sender] -= tokenAmount;
        account.totalSupply -= tokenAmount;
        account.volume24h += hyfeReceived;
        
        // Update market cap based on new supply
        if (account.totalSupply > 0) {
            account.marketCap = calculateBuyPrice(accountId, 1) * account.totalSupply / 1e18;
        } else {
            account.marketCap = 0;
        }
        
        // Collect fees
        protocolFeesCollected += protocolFee;
        creatorFeesEarned[account.creator] += creatorFee;
        
        // Transfer HYPE to seller
        require(HYPE_TOKEN.transfer(msg.sender, netAmount), "Transfer failed");
        
        // Record trade
        _recordTrade(accountId, msg.sender, tokenAmount, pricePerToken, hyfeReceived, false);
        
        emit TokensSold(accountId, msg.sender, tokenAmount, netAmount);
    }
    
    /**
     * @dev Internal buy tokens function
     */
    function _buyTokens(
        bytes32 accountId,
        uint256 hyfeAmount,
        uint256 maxPricePerToken
    ) internal {
        require(hyfeAmount > 0, "Amount required");
        
        uint256 tokenAmount = calculateBuyReturn(accountId, hyfeAmount);
        require(tokenAmount > 0, "Invalid token amount");
        
        uint256 pricePerToken = hyfeAmount * 1e18 / tokenAmount;
        require(pricePerToken <= maxPricePerToken, "Price above maximum");
        
        // Transfer HYPE from buyer
        require(HYPE_TOKEN.transferFrom(msg.sender, address(this), hyfeAmount), "Transfer failed");
        
        // Calculate fees
        uint256 protocolFee = hyfeAmount * PROTOCOL_FEE / FEE_DENOMINATOR;
        uint256 creatorFee = hyfeAmount * CREATOR_FEE / FEE_DENOMINATOR;
        
        // Update state
        SocialAccount storage account = socialAccounts[accountId];
        account.balances[msg.sender] += tokenAmount;
        account.totalSupply += tokenAmount;
        account.volume24h += hyfeAmount;
        
        // Update market cap
        account.marketCap = calculateBuyPrice(accountId, 1) * account.totalSupply / 1e18;
        
        // Collect fees
        protocolFeesCollected += protocolFee;
        creatorFeesEarned[account.creator] += creatorFee;
        
        // Record trade
        _recordTrade(accountId, msg.sender, tokenAmount, pricePerToken, hyfeAmount, true);
        
        emit TokensBought(accountId, msg.sender, tokenAmount, hyfeAmount);
    }
    
    /**
     * @dev Record trade in history
     */
    function _recordTrade(
        bytes32 accountId,
        address trader,
        uint256 amount,
        uint256 price,
        uint256 hyfeAmount,
        bool isBuy
    ) internal {
        trades.push(Trade({
            trader: trader,
            accountId: accountId,
            amount: amount,
            price: price,
            hyfeSpent: hyfeAmount,
            isBuy: isBuy,
            timestamp: block.timestamp
        }));
        
        userTrades[trader].push(trades.length - 1);
    }
    
    /**
     * @dev Calculate tokens received for HYPE amount (bonding curve)
     */
    function calculateBuyReturn(bytes32 accountId, uint256 hyfeAmount) public view returns (uint256) {
        if (!socialAccounts[accountId].isActive) return 0;
        
        uint256 currentSupply = socialAccounts[accountId].totalSupply;
        uint256 netAmount = hyfeAmount * (FEE_DENOMINATOR - PROTOCOL_FEE - CREATOR_FEE) / FEE_DENOMINATOR;
        
        // Bonding curve: price = BASE_PRICE + (supply / CURVE_STEEPNESS)^2
        uint256 newSupply = currentSupply + _calculateTokensFromCurve(currentSupply, netAmount);
        
        return newSupply - currentSupply;
    }
    
    /**
     * @dev Calculate HYPE received for token amount (bonding curve)
     */
    function calculateSellReturn(bytes32 accountId, uint256 tokenAmount) public view returns (uint256) {
        if (!socialAccounts[accountId].isActive) return 0;
        
        uint256 currentSupply = socialAccounts[accountId].totalSupply;
        if (tokenAmount > currentSupply) return 0;
        
        uint256 newSupply = currentSupply - tokenAmount;
        uint256 hyfeFromCurve = _calculateHypeFromCurve(newSupply, currentSupply);
        
        return hyfeFromCurve;
    }
    
    /**
     * @dev Calculate current buy price per token
     */
    function calculateBuyPrice(bytes32 accountId, uint256 amount) public view returns (uint256) {
        if (!socialAccounts[accountId].isActive || amount == 0) return 0;
        
        uint256 currentSupply = socialAccounts[accountId].totalSupply;
        
        // Price at current supply point on bonding curve
        return BASE_PRICE + (currentSupply * currentSupply) / (CURVE_STEEPNESS * CURVE_STEEPNESS);
    }
    
    /**
     * @dev Internal bonding curve calculation for buying
     */
    function _calculateTokensFromCurve(uint256 currentSupply, uint256 hyfeAmount) internal pure returns (uint256) {
        // Simplified bonding curve calculation
        // In production, this would use more sophisticated curve math
        if (hyfeAmount == 0) return 0;
        
        uint256 priceAtCurrent = BASE_PRICE + (currentSupply * currentSupply) / (CURVE_STEEPNESS * CURVE_STEEPNESS);
        
        // Approximate tokens based on average price
        return hyfeAmount * 1e18 / (priceAtCurrent + BASE_PRICE);
    }
    
    /**
     * @dev Internal bonding curve calculation for selling
     */
    function _calculateHypeFromCurve(uint256 newSupply, uint256 oldSupply) internal pure returns (uint256) {
        if (newSupply >= oldSupply) return 0;
        
        uint256 avgPrice = BASE_PRICE + ((newSupply + oldSupply) * (newSupply + oldSupply)) / (4 * CURVE_STEEPNESS * CURVE_STEEPNESS);
        
        return (oldSupply - newSupply) * avgPrice / 1e18;
    }
    
    /**
     * @dev Get account balance for user
     */
    function getAccountBalance(bytes32 accountId, address user) external view returns (uint256) {
        return socialAccounts[accountId].balances[user];
    }
    
    /**
     * @dev Get account details
     */
    function getAccountDetails(bytes32 accountId) external view returns (
        string memory handle,
        address creator,
        uint256 totalSupply,
        uint256 marketCap,
        uint256 volume24h,
        bool isActive,
        uint256 createdAt
    ) {
        SocialAccount storage account = socialAccounts[accountId];
        return (
            account.handle,
            account.creator,
            account.totalSupply,
            account.marketCap,
            account.volume24h,
            account.isActive,
            account.createdAt
        );
    }
    
    /**
     * @dev Get recent trades
     */
    function getRecentTrades(uint256 limit) external view returns (Trade[] memory) {
        uint256 length = trades.length;
        uint256 returnLength = limit > length ? length : limit;
        
        Trade[] memory recentTrades = new Trade[](returnLength);
        
        for (uint256 i = 0; i < returnLength; i++) {
            recentTrades[i] = trades[length - 1 - i];
        }
        
        return recentTrades;
    }
    
    /**
     * @dev Withdraw protocol fees (owner only)
     */
    function withdrawProtocolFees() external onlyOwner {
        uint256 amount = protocolFeesCollected;
        protocolFeesCollected = 0;
        
        require(HYPE_TOKEN.transfer(owner(), amount), "Transfer failed");
        emit FeesCollected(owner(), amount);
    }
    
    /**
     * @dev Withdraw creator fees
     */
    function withdrawCreatorFees() external {
        uint256 amount = creatorFeesEarned[msg.sender];
        require(amount > 0, "No fees available");
        
        creatorFeesEarned[msg.sender] = 0;
        
        require(HYPE_TOKEN.transfer(msg.sender, amount), "Transfer failed");
        emit FeesCollected(msg.sender, amount);
    }
    
    /**
     * @dev Emergency withdrawal (owner only)
     */
    function emergencyWithdraw(address token, uint256 amount) external onlyOwner {
        if (token == address(0)) {
            payable(owner()).transfer(amount);
        } else {
            IERC20(token).transfer(owner(), amount);
        }
        
        emit EmergencyWithdrawal(token, amount);
    }
    
    /**
     * @dev Pause trading (emergency)
     */
    function pauseTrading() external onlyOwner {
        _pause();
    }
    
    /**
     * @dev Resume trading
     */
    function unpauseTrading() external onlyOwner {
        _unpause();
    }
    
    /**
     * @dev Get total number of accounts
     */
    function getAccountCount() external view returns (uint256) {
        return accountIds.length;
    }
    
    /**
     * @dev Get total number of trades
     */
    function getTradeCount() external view returns (uint256) {
        return trades.length;
    }
}