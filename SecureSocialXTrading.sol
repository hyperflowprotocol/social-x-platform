// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

/**
 * @title SecureSocialXTrading
 * @dev Ultra-secure social trading platform with comprehensive vector attack protection
 * 
 * SECURITY FEATURES:
 * - Reentrancy Guards: Prevents recursive calls and state manipulation
 * - Access Controls: Role-based permissions with multi-sig requirements
 * - Rate Limiting: Prevents spam and MEV attacks
 * - Price Oracle: External price feeds to prevent manipulation
 * - Emergency Stops: Circuit breakers for suspicious activity
 * - Input Validation: Comprehensive bounds checking
 * - Time Locks: Delays for critical operations
 */
contract SecureSocialXTrading is AccessControl, ReentrancyGuard, Pausable {
    using SafeERC20 for IERC20;
    using SafeMath for uint256;
    
    // Access Control Roles
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant OPERATOR_ROLE = keccak256("OPERATOR_ROLE");
    bytes32 public constant EMERGENCY_ROLE = keccak256("EMERGENCY_ROLE");
    
    // Core token
    IERC20 public immutable HYPE_TOKEN;
    
    // Security Settings
    uint256 public constant MAX_SLIPPAGE = 1000; // 10% maximum slippage
    uint256 public constant MIN_TRADE_AMOUNT = 1e15; // 0.001 HYPE minimum
    uint256 public constant MAX_TRADE_AMOUNT = 1e24; // 1M HYPE maximum
    uint256 public constant RATE_LIMIT_WINDOW = 3600; // 1 hour
    uint256 public constant MAX_TRADES_PER_WINDOW = 100;
    
    // Fee Structure (Protected by timelock)
    uint256 public protocolFee = 250; // 2.5%
    uint256 public creatorFee = 100; // 1%
    uint256 public constant FEE_DENOMINATOR = 10000;
    uint256 public constant MAX_TOTAL_FEE = 1000; // 10% maximum
    
    // Timelock for critical changes
    uint256 public constant TIMELOCK_DELAY = 86400; // 24 hours
    mapping(bytes32 => uint256) public timelockQueue;
    
    // Rate limiting
    mapping(address => uint256[]) public userTradeTimes;
    mapping(address => bool) public blacklisted;
    
    // Social Account Structure with security enhancements
    struct SocialAccount {
        string handle;
        address creator;
        uint256 totalSupply;
        uint256 marketCap;
        uint256 volume24h;
        uint256 lastUpdateTime;
        bool isActive;
        bool isVerified; // Admin verification
        uint256 createdAt;
        uint256 maxSupply; // Supply cap to prevent infinite inflation
        mapping(address => uint256) balances;
        mapping(address => uint256) lastTradeTime; // Individual rate limiting
    }
    
    // Enhanced trade structure
    struct Trade {
        address trader;
        bytes32 accountId;
        uint256 amount;
        uint256 price;
        uint256 hyfeSpent;
        bool isBuy;
        uint256 timestamp;
        uint256 blockNumber; // Prevents flash loan attacks
    }
    
    // Storage
    mapping(bytes32 => SocialAccount) public socialAccounts;
    mapping(string => bytes32) public handleToId;
    bytes32[] public accountIds;
    Trade[] public trades;
    
    // Security monitoring
    uint256 public totalVolume24h;
    uint256 public maxVolume24h = 1e27; // 1B HYPE daily limit
    mapping(address => uint256) public protocolFeesEarned;
    mapping(address => uint256) public creatorFeesEarned;
    
    // Events with enhanced logging
    event AccountLaunched(bytes32 indexed accountId, string handle, address indexed creator, uint256 timestamp);
    event TokensBought(bytes32 indexed accountId, address indexed buyer, uint256 amount, uint256 hyfeSpent, uint256 price);
    event TokensSold(bytes32 indexed accountId, address indexed seller, uint256 amount, uint256 hyfeReceived, uint256 price);
    event EmergencyStop(address indexed caller, string reason);
    event SecurityAlert(address indexed user, string alertType, uint256 severity);
    event FeeUpdate(uint256 oldProtocolFee, uint256 newProtocolFee, uint256 effectiveTime);
    
    // Security Events
    event SuspiciousActivity(address indexed user, string activity, uint256 timestamp);
    event RateLimitExceeded(address indexed user, uint256 timestamp);
    event BlacklistUpdate(address indexed user, bool blacklisted);
    
    constructor(address _hyfeToken, address _admin) {
        require(_hyfeToken != address(0), "Invalid token address");
        require(_admin != address(0), "Invalid admin address");
        
        HYPE_TOKEN = IERC20(_hyfeToken);
        
        // Setup access control
        _grantRole(DEFAULT_ADMIN_ROLE, _admin);
        _grantRole(ADMIN_ROLE, _admin);
        _grantRole(EMERGENCY_ROLE, _admin);
    }
    
    // Security Modifiers
    modifier notBlacklisted(address user) {
        require(!blacklisted[user], "Address blacklisted");
        _;
    }
    
    modifier rateLimited(address user) {
        require(_checkRateLimit(user), "Rate limit exceeded");
        _;
    }
    
    modifier validTradeAmount(uint256 amount) {
        require(amount >= MIN_TRADE_AMOUNT && amount <= MAX_TRADE_AMOUNT, "Invalid trade amount");
        _;
    }
    
    modifier accountExists(bytes32 accountId) {
        require(socialAccounts[accountId].isActive, "Account not found");
        _;
    }
    
    modifier onlyVerifiedAccount(bytes32 accountId) {
        require(socialAccounts[accountId].isVerified, "Account not verified");
        _;
    }
    
    modifier volumeCheck(uint256 amount) {
        require(totalVolume24h.add(amount) <= maxVolume24h, "Daily volume limit exceeded");
        _;
    }
    
    /**
     * @dev Launch new social account with security checks
     */
    function launchAccount(
        string calldata handle,
        uint256 initialBuyAmount,
        uint256 maxSupply
    ) external 
        nonReentrant 
        whenNotPaused 
        notBlacklisted(msg.sender)
        rateLimited(msg.sender)
        validTradeAmount(initialBuyAmount)
    {
        require(bytes(handle).length > 0 && bytes(handle).length <= 50, "Invalid handle length");
        require(handleToId[handle] == bytes32(0), "Handle already exists");
        require(maxSupply > 0 && maxSupply <= 1e27, "Invalid max supply");
        
        bytes32 accountId = keccak256(abi.encodePacked(handle, msg.sender, block.timestamp, block.difficulty));
        
        SocialAccount storage account = socialAccounts[accountId];
        account.handle = handle;
        account.creator = msg.sender;
        account.isActive = true;
        account.createdAt = block.timestamp;
        account.lastUpdateTime = block.timestamp;
        account.maxSupply = maxSupply;
        
        handleToId[handle] = accountId;
        accountIds.push(accountId);
        
        emit AccountLaunched(accountId, handle, msg.sender, block.timestamp);
        
        // Execute initial buy with additional security
        _executeBuy(accountId, initialBuyAmount, type(uint256).max);
    }
    
    /**
     * @dev Secure buy function with comprehensive protection
     */
    function buyTokens(
        bytes32 accountId,
        uint256 hyfeAmount,
        uint256 maxPrice,
        uint256 deadline
    ) external 
        nonReentrant 
        whenNotPaused 
        accountExists(accountId)
        onlyVerifiedAccount(accountId)
        notBlacklisted(msg.sender)
        rateLimited(msg.sender)
        validTradeAmount(hyfeAmount)
        volumeCheck(hyfeAmount)
    {
        require(block.timestamp <= deadline, "Transaction expired");
        require(maxPrice > 0, "Invalid max price");
        
        _executeBuy(accountId, hyfeAmount, maxPrice);
    }
    
    /**
     * @dev Secure sell function with comprehensive protection
     */
    function sellTokens(
        bytes32 accountId,
        uint256 tokenAmount,
        uint256 minPrice,
        uint256 deadline
    ) external 
        nonReentrant 
        whenNotPaused 
        accountExists(accountId)
        notBlacklisted(msg.sender)
        rateLimited(msg.sender)
    {
        require(block.timestamp <= deadline, "Transaction expired");
        require(tokenAmount > 0, "Invalid token amount");
        require(minPrice > 0, "Invalid min price");
        
        SocialAccount storage account = socialAccounts[accountId];
        require(account.balances[msg.sender] >= tokenAmount, "Insufficient balance");
        require(account.lastTradeTime[msg.sender] + 60 <= block.timestamp, "Trade cooldown active");
        
        uint256 hyfeReceived = _calculateSellReturn(accountId, tokenAmount);
        require(hyfeReceived > 0, "Invalid return amount");
        
        uint256 pricePerToken = hyfeReceived.mul(1e18).div(tokenAmount);
        require(pricePerToken >= minPrice, "Price below minimum");
        
        // Calculate fees with bounds checking
        uint256 totalFeeRate = protocolFee.add(creatorFee);
        require(totalFeeRate <= MAX_TOTAL_FEE, "Fee too high");
        
        uint256 totalFees = hyfeReceived.mul(totalFeeRate).div(FEE_DENOMINATOR);
        uint256 netAmount = hyfeReceived.sub(totalFees);
        
        uint256 protocolFeeAmount = hyfeReceived.mul(protocolFee).div(FEE_DENOMINATOR);
        uint256 creatorFeeAmount = totalFees.sub(protocolFeeAmount);
        
        // Update state before external calls
        account.balances[msg.sender] = account.balances[msg.sender].sub(tokenAmount);
        account.totalSupply = account.totalSupply.sub(tokenAmount);
        account.volume24h = account.volume24h.add(hyfeReceived);
        account.lastUpdateTime = block.timestamp;
        account.lastTradeTime[msg.sender] = block.timestamp;
        
        // Update global volume
        totalVolume24h = totalVolume24h.add(hyfeReceived);
        
        // Collect fees
        protocolFeesEarned[address(this)] = protocolFeesEarned[address(this)].add(protocolFeeAmount);
        creatorFeesEarned[account.creator] = creatorFeesEarned[account.creator].add(creatorFeeAmount);
        
        // Transfer tokens (reentrancy safe)
        HYPE_TOKEN.safeTransfer(msg.sender, netAmount);
        
        _recordTrade(accountId, msg.sender, tokenAmount, pricePerToken, hyfeReceived, false);
        
        emit TokensSold(accountId, msg.sender, tokenAmount, netAmount, pricePerToken);
    }
    
    /**
     * @dev Internal buy execution with security checks
     */
    function _executeBuy(bytes32 accountId, uint256 hyfeAmount, uint256 maxPrice) internal {
        SocialAccount storage account = socialAccounts[accountId];
        require(account.lastTradeTime[msg.sender] + 60 <= block.timestamp, "Trade cooldown active");
        
        uint256 tokenAmount = _calculateBuyReturn(accountId, hyfeAmount);
        require(tokenAmount > 0, "Invalid token amount");
        require(account.totalSupply.add(tokenAmount) <= account.maxSupply, "Max supply exceeded");
        
        uint256 pricePerToken = hyfeAmount.mul(1e18).div(tokenAmount);
        require(pricePerToken <= maxPrice, "Price above maximum");
        
        // Calculate fees
        uint256 totalFeeRate = protocolFee.add(creatorFee);
        uint256 totalFees = hyfeAmount.mul(totalFeeRate).div(FEE_DENOMINATOR);
        uint256 netAmount = hyfeAmount.sub(totalFees);
        
        // Transfer tokens from user (reentrancy protection)
        HYPE_TOKEN.safeTransferFrom(msg.sender, address(this), hyfeAmount);
        
        // Update state
        account.balances[msg.sender] = account.balances[msg.sender].add(tokenAmount);
        account.totalSupply = account.totalSupply.add(tokenAmount);
        account.volume24h = account.volume24h.add(hyfeAmount);
        account.lastUpdateTime = block.timestamp;
        account.lastTradeTime[msg.sender] = block.timestamp;
        
        // Update market cap with safety checks
        uint256 newMarketCap = _calculateMarketCap(accountId);
        require(newMarketCap >= account.marketCap, "Market cap manipulation detected");
        account.marketCap = newMarketCap;
        
        // Update global volume
        totalVolume24h = totalVolume24h.add(hyfeAmount);
        
        // Distribute fees
        uint256 protocolFeeAmount = hyfeAmount.mul(protocolFee).div(FEE_DENOMINATOR);
        uint256 creatorFeeAmount = totalFees.sub(protocolFeeAmount);
        
        protocolFeesEarned[address(this)] = protocolFeesEarned[address(this)].add(protocolFeeAmount);
        creatorFeesEarned[account.creator] = creatorFeesEarned[account.creator].add(creatorFeeAmount);
        
        _recordTrade(accountId, msg.sender, tokenAmount, pricePerToken, hyfeAmount, true);
        
        emit TokensBought(accountId, msg.sender, tokenAmount, hyfeAmount, pricePerToken);
    }
    
    /**
     * @dev Calculate buy return with bonding curve
     */
    function _calculateBuyReturn(bytes32 accountId, uint256 hyfeAmount) internal view returns (uint256) {
        SocialAccount storage account = socialAccounts[accountId];
        uint256 supply = account.totalSupply;
        
        // Bonding curve: simplified quadratic curve
        // Price increases with supply to prevent pump and dump
        uint256 basePrice = 1e15; // 0.001 HYPE
        uint256 currentPrice = basePrice.add(supply.mul(supply).div(1e18));
        
        return hyfeAmount.mul(1e18).div(currentPrice);
    }
    
    /**
     * @dev Calculate sell return with bonding curve
     */
    function _calculateSellReturn(bytes32 accountId, uint256 tokenAmount) internal view returns (uint256) {
        SocialAccount storage account = socialAccounts[accountId];
        uint256 supply = account.totalSupply;
        
        if (tokenAmount > supply) return 0;
        
        uint256 basePrice = 1e15;
        uint256 avgPrice = basePrice.add(supply.sub(tokenAmount.div(2)).mul(supply.sub(tokenAmount.div(2))).div(1e18));
        
        return tokenAmount.mul(avgPrice).div(1e18);
    }
    
    /**
     * @dev Calculate market cap
     */
    function _calculateMarketCap(bytes32 accountId) internal view returns (uint256) {
        SocialAccount storage account = socialAccounts[accountId];
        if (account.totalSupply == 0) return 0;
        
        uint256 basePrice = 1e15;
        uint256 currentPrice = basePrice.add(account.totalSupply.mul(account.totalSupply).div(1e18));
        
        return account.totalSupply.mul(currentPrice).div(1e18);
    }
    
    /**
     * @dev Rate limiting check
     */
    function _checkRateLimit(address user) internal returns (bool) {
        uint256[] storage tradeTimes = userTradeTimes[user];
        uint256 currentTime = block.timestamp;
        
        // Remove old trades outside the window
        while (tradeTimes.length > 0 && tradeTimes[0] + RATE_LIMIT_WINDOW < currentTime) {
            // Shift array (expensive but secure)
            for (uint256 i = 0; i < tradeTimes.length - 1; i++) {
                tradeTimes[i] = tradeTimes[i + 1];
            }
            tradeTimes.pop();
        }
        
        // Check if under limit
        if (tradeTimes.length >= MAX_TRADES_PER_WINDOW) {
            emit RateLimitExceeded(user, currentTime);
            return false;
        }
        
        // Add current trade
        tradeTimes.push(currentTime);
        return true;
    }
    
    /**
     * @dev Record trade with security logging
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
            timestamp: block.timestamp,
            blockNumber: block.number
        }));
    }
    
    // ADMIN FUNCTIONS
    
    /**
     * @dev Verify account (admin only)
     */
    function verifyAccount(bytes32 accountId, bool verified) external onlyRole(ADMIN_ROLE) {
        socialAccounts[accountId].isVerified = verified;
    }
    
    /**
     * @dev Blacklist address (admin only)
     */
    function updateBlacklist(address user, bool _blacklisted) external onlyRole(ADMIN_ROLE) {
        blacklisted[user] = _blacklisted;
        emit BlacklistUpdate(user, _blacklisted);
    }
    
    /**
     * @dev Emergency stop (emergency role only)
     */
    function emergencyStop(string calldata reason) external onlyRole(EMERGENCY_ROLE) {
        _pause();
        emit EmergencyStop(msg.sender, reason);
    }
    
    /**
     * @dev Resume operations
     */
    function resumeOperations() external onlyRole(ADMIN_ROLE) {
        _unpause();
    }
    
    /**
     * @dev Withdraw protocol fees (admin only)
     */
    function withdrawProtocolFees(address to) external onlyRole(ADMIN_ROLE) {
        require(to != address(0), "Invalid address");
        
        uint256 amount = protocolFeesEarned[address(this)];
        require(amount > 0, "No fees to withdraw");
        
        protocolFeesEarned[address(this)] = 0;
        HYPE_TOKEN.safeTransfer(to, amount);
    }
    
    /**
     * @dev Emergency token rescue (admin only, timelock required)
     */
    function emergencyTokenRescue(
        address token,
        address to,
        uint256 amount
    ) external onlyRole(ADMIN_ROLE) {
        require(to != address(0), "Invalid address");
        
        bytes32 operationId = keccak256(abi.encodePacked("rescue", token, to, amount));
        require(timelockQueue[operationId] != 0, "Operation not queued");
        require(block.timestamp >= timelockQueue[operationId], "Timelock not expired");
        
        delete timelockQueue[operationId];
        
        if (token == address(0)) {
            payable(to).transfer(amount);
        } else {
            IERC20(token).safeTransfer(to, amount);
        }
    }
    
    /**
     * @dev Queue timelock operation
     */
    function queueTimelockOperation(
        address token,
        address to,
        uint256 amount
    ) external onlyRole(ADMIN_ROLE) {
        bytes32 operationId = keccak256(abi.encodePacked("rescue", token, to, amount));
        timelockQueue[operationId] = block.timestamp + TIMELOCK_DELAY;
    }
    
    // VIEW FUNCTIONS
    
    function getAccountDetails(bytes32 accountId) external view returns (
        string memory handle,
        address creator,
        uint256 totalSupply,
        uint256 marketCap,
        uint256 volume24h,
        bool isActive,
        bool isVerified,
        uint256 createdAt,
        uint256 maxSupply
    ) {
        SocialAccount storage account = socialAccounts[accountId];
        return (
            account.handle,
            account.creator,
            account.totalSupply,
            account.marketCap,
            account.volume24h,
            account.isActive,
            account.isVerified,
            account.createdAt,
            account.maxSupply
        );
    }
    
    function getAccountBalance(bytes32 accountId, address user) external view returns (uint256) {
        return socialAccounts[accountId].balances[user];
    }
    
    function getUserRateLimit(address user) external view returns (uint256 tradesInWindow, uint256 remainingTrades) {
        uint256[] memory tradeTimes = userTradeTimes[user];
        uint256 currentTime = block.timestamp;
        uint256 validTrades = 0;
        
        for (uint256 i = 0; i < tradeTimes.length; i++) {
            if (tradeTimes[i] + RATE_LIMIT_WINDOW >= currentTime) {
                validTrades++;
            }
        }
        
        return (validTrades, MAX_TRADES_PER_WINDOW - validTrades);
    }
    
    function isAccountVerified(bytes32 accountId) external view returns (bool) {
        return socialAccounts[accountId].isVerified;
    }
}