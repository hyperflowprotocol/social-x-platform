// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/**
 * @title HyperFlowNFT
 * @dev Comprehensive NFT minting contract with phases, whitelist, and fund distribution
 */
contract HyperFlowNFT is ERC721, ERC721Enumerable, ERC721URIStorage, Pausable, Ownable, ReentrancyGuard {
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIdCounter;
    
    // Collection Configuration
    uint256 public constant MAX_SUPPLY = 10000;
    uint256 public constant MAX_MINT_PER_WALLET = 5;
    uint256 public constant WHITELIST_PRICE = 0.05 ether; // 0.05 ETH in whitelist phase
    uint256 public constant PUBLIC_PRICE = 0.08 ether;    // 0.08 ETH in public phase
    
    // HYPE Token Configuration
    IERC20 public immutable hypeToken;
    uint256 public constant HYPE_WHITELIST_PRICE = 100 * 10**18; // 100 HYPE tokens
    uint256 public constant HYPE_PUBLIC_PRICE = 150 * 10**18;    // 150 HYPE tokens
    
    // Mint Phases
    enum MintPhase { CLOSED, WHITELIST, PUBLIC }
    MintPhase public currentPhase = MintPhase.CLOSED;
    
    uint256 public whitelistStartTime;
    uint256 public whitelistEndTime;
    uint256 public publicStartTime;
    uint256 public publicEndTime;
    
    // Whitelist & Mint Tracking
    mapping(address => bool) public whitelist;
    mapping(address => uint256) public mintedCount;
    uint256 public whitelistSize;
    
    // Fund Distribution
    address public platformWallet;
    address public creatorWallet;
    address public developmentWallet;
    
    uint256 public constant PLATFORM_FEE_PERCENT = 5;    // 5%
    uint256 public constant CREATOR_ROYALTY_PERCENT = 10; // 10%
    uint256 public constant DEV_FUND_PERCENT = 85;       // 85%
    
    // Metadata
    string private _baseTokenURI;
    string public contractURI;
    
    // Events
    event WhitelistAdded(address indexed user, uint256 totalWhitelisted);
    event WhitelistRemoved(address indexed user, uint256 totalWhitelisted);
    event WhitelistBulkAdded(uint256 count);
    event PhaseChanged(MintPhase newPhase, uint256 timestamp);
    event NFTMinted(address indexed to, uint256 indexed tokenId, MintPhase phase, bool usedHYPE);
    event FundsDistributed(uint256 platformFee, uint256 creatorRoyalty, uint256 devFund);
    event PhaseTimeUpdated(MintPhase phase, uint256 startTime, uint256 endTime);
    
    constructor(
        string memory name,
        string memory symbol,
        string memory baseURI,
        address _hypeToken,
        address _platformWallet,
        address _creatorWallet,
        address _developmentWallet
    ) ERC721(name, symbol) {
        _baseTokenURI = baseURI;
        hypeToken = IERC20(_hypeToken);
        platformWallet = _platformWallet;
        creatorWallet = _creatorWallet;
        developmentWallet = _developmentWallet;
        
        // Start token IDs from 1
        _tokenIdCounter.increment();
    }
    
    // ============ WHITELIST MANAGEMENT ============
    
    /**
     * @dev Add single address to whitelist
     */
    function addToWhitelist(address user) external onlyOwner {
        require(!whitelist[user], "Already whitelisted");
        whitelist[user] = true;
        whitelistSize++;
        emit WhitelistAdded(user, whitelistSize);
    }
    
    /**
     * @dev Remove address from whitelist
     */
    function removeFromWhitelist(address user) external onlyOwner {
        require(whitelist[user], "Not whitelisted");
        whitelist[user] = false;
        whitelistSize--;
        emit WhitelistRemoved(user, whitelistSize);
    }
    
    /**
     * @dev Bulk add addresses to whitelist (CSV import functionality)
     */
    function bulkAddToWhitelist(address[] calldata users) external onlyOwner {
        require(users.length > 0, "Empty list");
        require(users.length <= 500, "Too many addresses at once"); // Gas limit protection
        
        uint256 addedCount = 0;
        for (uint256 i = 0; i < users.length; i++) {
            if (!whitelist[users[i]] && users[i] != address(0)) {
                whitelist[users[i]] = true;
                addedCount++;
            }
        }
        
        whitelistSize += addedCount;
        emit WhitelistBulkAdded(addedCount);
    }
    
    /**
     * @dev Check if address is whitelisted
     */
    function isWhitelisted(address user) external view returns (bool) {
        return whitelist[user];
    }
    
    // ============ PHASE MANAGEMENT ============
    
    /**
     * @dev Set whitelist phase times
     */
    function setWhitelistPhase(uint256 startTime, uint256 endTime) external onlyOwner {
        require(startTime > block.timestamp, "Start time must be in future");
        require(endTime > startTime, "End time must be after start time");
        require(startTime > 0 && endTime > 0, "Invalid timestamps");
        
        whitelistStartTime = startTime;
        whitelistEndTime = endTime;
        
        emit PhaseTimeUpdated(MintPhase.WHITELIST, startTime, endTime);
    }
    
    /**
     * @dev Set public phase times
     */
    function setPublicPhase(uint256 startTime, uint256 endTime) external onlyOwner {
        require(startTime > whitelistEndTime, "Public must start after whitelist ends");
        require(endTime > startTime, "End time must be after start time");
        
        publicStartTime = startTime;
        publicEndTime = endTime;
        
        emit PhaseTimeUpdated(MintPhase.PUBLIC, startTime, endTime);
    }
    
    /**
     * @dev Manually set current phase (emergency function)
     */
    function setPhase(MintPhase phase) external onlyOwner {
        currentPhase = phase;
        emit PhaseChanged(phase, block.timestamp);
    }
    
    /**
     * @dev Update phase based on current time (anyone can call)
     */
    function updatePhase() public {
        uint256 currentTime = block.timestamp;
        MintPhase newPhase = currentPhase;
        
        if (currentTime >= whitelistStartTime && currentTime <= whitelistEndTime) {
            newPhase = MintPhase.WHITELIST;
        } else if (currentTime >= publicStartTime && currentTime <= publicEndTime) {
            newPhase = MintPhase.PUBLIC;
        } else {
            newPhase = MintPhase.CLOSED;
        }
        
        if (newPhase != currentPhase) {
            currentPhase = newPhase;
            emit PhaseChanged(newPhase, currentTime);
        }
    }
    
    // ============ MINTING FUNCTIONS ============
    
    /**
     * @dev Mint NFT with ETH payment
     */
    function mintWithETH(uint256 quantity) external payable nonReentrant whenNotPaused {
        updatePhase();
        require(currentPhase != MintPhase.CLOSED, "Minting is closed");
        require(quantity > 0 && quantity <= 5, "Invalid quantity (1-5)");
        require(totalSupply() + quantity <= MAX_SUPPLY, "Exceeds max supply");
        require(mintedCount[msg.sender] + quantity <= MAX_MINT_PER_WALLET, "Exceeds wallet limit");
        
        uint256 price = (currentPhase == MintPhase.WHITELIST) ? WHITELIST_PRICE : PUBLIC_PRICE;
        require(msg.value >= price * quantity, "Insufficient payment");
        
        if (currentPhase == MintPhase.WHITELIST) {
            require(whitelist[msg.sender], "Not whitelisted");
        }
        
        // Mint NFTs
        for (uint256 i = 0; i < quantity; i++) {
            uint256 tokenId = _tokenIdCounter.current();
            _tokenIdCounter.increment();
            _safeMint(msg.sender, tokenId);
            emit NFTMinted(msg.sender, tokenId, currentPhase, false);
        }
        
        mintedCount[msg.sender] += quantity;
        
        // Refund excess payment
        if (msg.value > price * quantity) {
            payable(msg.sender).transfer(msg.value - (price * quantity));
        }
        
        // Distribute funds
        _distributeFunds(price * quantity);
    }
    
    /**
     * @dev Mint NFT with HYPE tokens
     */
    function mintWithHYPE(uint256 quantity) external nonReentrant whenNotPaused {
        updatePhase();
        require(currentPhase != MintPhase.CLOSED, "Minting is closed");
        require(quantity > 0 && quantity <= 5, "Invalid quantity (1-5)");
        require(totalSupply() + quantity <= MAX_SUPPLY, "Exceeds max supply");
        require(mintedCount[msg.sender] + quantity <= MAX_MINT_PER_WALLET, "Exceeds wallet limit");
        
        uint256 hypePrice = (currentPhase == MintPhase.WHITELIST) ? HYPE_WHITELIST_PRICE : HYPE_PUBLIC_PRICE;
        uint256 totalHypePrice = hypePrice * quantity;
        
        if (currentPhase == MintPhase.WHITELIST) {
            require(whitelist[msg.sender], "Not whitelisted");
        }
        
        // Transfer HYPE tokens from user
        require(hypeToken.transferFrom(msg.sender, address(this), totalHypePrice), "HYPE transfer failed");
        
        // Mint NFTs
        for (uint256 i = 0; i < quantity; i++) {
            uint256 tokenId = _tokenIdCounter.current();
            _tokenIdCounter.increment();
            _safeMint(msg.sender, tokenId);
            emit NFTMinted(msg.sender, tokenId, currentPhase, true);
        }
        
        mintedCount[msg.sender] += quantity;
        
        // Distribute HYPE tokens
        _distributeHYPEFunds(totalHypePrice);
    }
    
    /**
     * @dev Owner mint for promotions/team (free minting)
     */
    function ownerMint(address to, uint256 quantity) external onlyOwner {
        require(quantity > 0, "Quantity must be greater than 0");
        require(totalSupply() + quantity <= MAX_SUPPLY, "Exceeds max supply");
        
        for (uint256 i = 0; i < quantity; i++) {
            uint256 tokenId = _tokenIdCounter.current();
            _tokenIdCounter.increment();
            _safeMint(to, tokenId);
            emit NFTMinted(to, tokenId, MintPhase.CLOSED, false);
        }
    }
    
    // ============ FUND DISTRIBUTION ============
    
    /**
     * @dev Distribute ETH funds according to percentages
     */
    function _distributeFunds(uint256 amount) internal {
        uint256 platformFee = (amount * PLATFORM_FEE_PERCENT) / 100;
        uint256 creatorRoyalty = (amount * CREATOR_ROYALTY_PERCENT) / 100;
        uint256 devFund = amount - platformFee - creatorRoyalty;
        
        if (platformFee > 0) {
            payable(platformWallet).transfer(platformFee);
        }
        if (creatorRoyalty > 0) {
            payable(creatorWallet).transfer(creatorRoyalty);
        }
        if (devFund > 0) {
            payable(developmentWallet).transfer(devFund);
        }
        
        emit FundsDistributed(platformFee, creatorRoyalty, devFund);
    }
    
    /**
     * @dev Distribute HYPE token funds according to percentages
     */
    function _distributeHYPEFunds(uint256 amount) internal {
        uint256 platformFee = (amount * PLATFORM_FEE_PERCENT) / 100;
        uint256 creatorRoyalty = (amount * CREATOR_ROYALTY_PERCENT) / 100;
        uint256 devFund = amount - platformFee - creatorRoyalty;
        
        if (platformFee > 0) {
            hypeToken.transfer(platformWallet, platformFee);
        }
        if (creatorRoyalty > 0) {
            hypeToken.transfer(creatorWallet, creatorRoyalty);
        }
        if (devFund > 0) {
            hypeToken.transfer(developmentWallet, devFund);
        }
        
        emit FundsDistributed(platformFee, creatorRoyalty, devFund);
    }
    
    // ============ METADATA & URI FUNCTIONS ============
    
    function setBaseURI(string memory newBaseURI) external onlyOwner {
        _baseTokenURI = newBaseURI;
    }
    
    function setContractURI(string memory newContractURI) external onlyOwner {
        contractURI = newContractURI;
    }
    
    function _baseURI() internal view override returns (string memory) {
        return _baseTokenURI;
    }
    
    function tokenURI(uint256 tokenId) public view override(ERC721, ERC721URIStorage) returns (string memory) {
        return super.tokenURI(tokenId);
    }
    
    // ============ VIEW FUNCTIONS ============
    
    function getCurrentPrice() external view returns (uint256 ethPrice, uint256 hypePrice) {
        if (currentPhase == MintPhase.WHITELIST) {
            return (WHITELIST_PRICE, HYPE_WHITELIST_PRICE);
        } else if (currentPhase == MintPhase.PUBLIC) {
            return (PUBLIC_PRICE, HYPE_PUBLIC_PRICE);
        }
        return (0, 0);
    }
    
    function getPhaseInfo() external view returns (
        MintPhase phase,
        uint256 whitelistStart,
        uint256 whitelistEnd,
        uint256 publicStart,
        uint256 publicEnd,
        uint256 currentTime
    ) {
        return (
            currentPhase,
            whitelistStartTime,
            whitelistEndTime,
            publicStartTime,
            publicEndTime,
            block.timestamp
        );
    }
    
    function getMintInfo(address user) external view returns (
        uint256 minted,
        uint256 maxMint,
        bool isWhitelisted,
        uint256 remainingSupply
    ) {
        return (
            mintedCount[user],
            MAX_MINT_PER_WALLET,
            whitelist[user],
            MAX_SUPPLY - totalSupply()
        );
    }
    
    // ============ ADMIN FUNCTIONS ============
    
    function pause() external onlyOwner {
        _pause();
    }
    
    function unpause() external onlyOwner {
        _unpause();
    }
    
    function updateWallets(
        address _platformWallet,
        address _creatorWallet,
        address _developmentWallet
    ) external onlyOwner {
        require(_platformWallet != address(0), "Invalid platform wallet");
        require(_creatorWallet != address(0), "Invalid creator wallet");
        require(_developmentWallet != address(0), "Invalid development wallet");
        
        platformWallet = _platformWallet;
        creatorWallet = _creatorWallet;
        developmentWallet = _developmentWallet;
    }
    
    // Emergency withdrawal functions
    function withdrawETH() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
    
    function withdrawHYPE() external onlyOwner {
        uint256 balance = hypeToken.balanceOf(address(this));
        hypeToken.transfer(owner(), balance);
    }
    
    // ============ REQUIRED OVERRIDES ============
    
    function _beforeTokenTransfer(address from, address to, uint256 tokenId, uint256 batchSize)
        internal
        override(ERC721, ERC721Enumerable)
    {
        super._beforeTokenTransfer(from, to, tokenId, batchSize);
    }
    
    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }
    
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable, ERC721URIStorage)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}