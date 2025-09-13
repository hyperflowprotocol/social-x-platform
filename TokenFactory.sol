// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title LaunchedToken
 * @dev Standard ERC20 token with additional features for launched tokens
 */
contract LaunchedToken is ERC20, ERC20Burnable, ERC20Pausable, Ownable, ReentrancyGuard {
    string private _tokenDescription;
    string private _website;
    string private _logoURI;
    uint256 private _launchTimestamp;
    address private _factory;
    
    event MetadataUpdated(string description, string website, string logoURI);
    event TokenLaunched(address indexed creator, uint256 timestamp);
    
    constructor(
        string memory name,
        string memory symbol,
        uint256 totalSupply,
        string memory description,
        string memory website,
        string memory logoURI,
        address creator
    ) ERC20(name, symbol) {
        _tokenDescription = description;
        _website = website;
        _logoURI = logoURI;
        _launchTimestamp = block.timestamp;
        _factory = msg.sender;
        
        _mint(creator, totalSupply * 10**decimals());
        _transferOwnership(creator);
        
        emit TokenLaunched(creator, block.timestamp);
    }
    
    function description() public view returns (string memory) {
        return _tokenDescription;
    }
    
    function website() public view returns (string memory) {
        return _website;
    }
    
    function logoURI() public view returns (string memory) {
        return _logoURI;
    }
    
    function launchTimestamp() public view returns (uint256) {
        return _launchTimestamp;
    }
    
    function factory() public view returns (address) {
        return _factory;
    }
    
    function updateMetadata(
        string memory newDescription,
        string memory newWebsite,
        string memory newLogoURI
    ) public onlyOwner {
        _tokenDescription = newDescription;
        _website = newWebsite;
        _logoURI = newLogoURI;
        
        emit MetadataUpdated(newDescription, newWebsite, newLogoURI);
    }
    
    function pause() public onlyOwner {
        _pause();
    }
    
    function unpause() public onlyOwner {
        _unpause();
    }
    
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal override(ERC20, ERC20Pausable) {
        super._beforeTokenTransfer(from, to, amount);
    }
}

/**
 * @title HYPETokenFactory
 * @dev Factory contract for seamless token deployment
 */
contract HYPETokenFactory is ReentrancyGuard {
    address public immutable platformToken; // HYPE token address
    uint256 public deploymentFee = 0.002 ether; // Fee in HYPE tokens
    address public feeCollector;
    uint256 public totalTokensDeployed;
    
    struct TokenInfo {
        address tokenAddress;
        string name;
        string symbol;
        uint256 totalSupply;
        string description;
        string website;
        string logoURI;
        address creator;
        uint256 timestamp;
    }
    
    mapping(address => TokenInfo) public deployedTokens;
    mapping(address => address[]) public creatorTokens;
    address[] public allTokens;
    
    event TokenDeployed(
        address indexed tokenAddress,
        address indexed creator,
        string name,
        string symbol,
        uint256 totalSupply
    );
    
    event FeeUpdated(uint256 oldFee, uint256 newFee);
    event FeeCollectorUpdated(address oldCollector, address newCollector);
    
    constructor(address _platformToken, address _feeCollector) {
        platformToken = _platformToken;
        feeCollector = _feeCollector;
    }
    
    /**
     * @dev Deploy a new token with specified parameters
     * @param name Token name
     * @param symbol Token symbol
     * @param totalSupply Total supply (will be multiplied by 10^18)
     * @param description Token description
     * @param website Project website
     * @param logoURI Logo URI (IPFS or HTTP)
     */
    function deployToken(
        string memory name,
        string memory symbol,
        uint256 totalSupply,
        string memory description,
        string memory website,
        string memory logoURI
    ) external payable nonReentrant {
        require(bytes(name).length > 0, "Name cannot be empty");
        require(bytes(symbol).length > 0, "Symbol cannot be empty");
        require(totalSupply > 0, "Total supply must be greater than 0");
        require(msg.value >= deploymentFee, "Insufficient deployment fee");
        
        // Deploy new token
        LaunchedToken newToken = new LaunchedToken(
            name,
            symbol,
            totalSupply,
            description,
            website,
            logoURI,
            msg.sender
        );
        
        // Store token information
        TokenInfo memory tokenInfo = TokenInfo({
            tokenAddress: address(newToken),
            name: name,
            symbol: symbol,
            totalSupply: totalSupply,
            description: description,
            website: website,
            logoURI: logoURI,
            creator: msg.sender,
            timestamp: block.timestamp
        });
        
        deployedTokens[address(newToken)] = tokenInfo;
        creatorTokens[msg.sender].push(address(newToken));
        allTokens.push(address(newToken));
        totalTokensDeployed++;
        
        // Transfer deployment fee
        if (msg.value > 0) {
            payable(feeCollector).transfer(msg.value);
        }
        
        emit TokenDeployed(
            address(newToken),
            msg.sender,
            name,
            symbol,
            totalSupply
        );
    }
    
    function getTokenInfo(address tokenAddress) external view returns (TokenInfo memory) {
        return deployedTokens[tokenAddress];
    }
    
    function getCreatorTokens(address creator) external view returns (address[] memory) {
        return creatorTokens[creator];
    }
    
    function getAllTokens() external view returns (address[] memory) {
        return allTokens;
    }
    
    function getRecentTokens(uint256 limit) external view returns (address[] memory) {
        require(limit > 0, "Limit must be greater than 0");
        
        uint256 length = allTokens.length;
        if (limit > length) {
            limit = length;
        }
        
        address[] memory recentTokens = new address[](limit);
        for (uint256 i = 0; i < limit; i++) {
            recentTokens[i] = allTokens[length - 1 - i];
        }
        
        return recentTokens;
    }
    
    function updateDeploymentFee(uint256 newFee) external {
        require(msg.sender == feeCollector, "Only fee collector can update fee");
        uint256 oldFee = deploymentFee;
        deploymentFee = newFee;
        emit FeeUpdated(oldFee, newFee);
    }
    
    function updateFeeCollector(address newCollector) external {
        require(msg.sender == feeCollector, "Only fee collector can update collector");
        require(newCollector != address(0), "Invalid collector address");
        address oldCollector = feeCollector;
        feeCollector = newCollector;
        emit FeeCollectorUpdated(oldCollector, newCollector);
    }
    
    // Emergency withdraw function (should rarely be used)
    function emergencyWithdraw() external {
        require(msg.sender == feeCollector, "Only fee collector can withdraw");
        payable(feeCollector).transfer(address(this).balance);
    }
}