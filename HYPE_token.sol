// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}

contract HYPEToken is IERC20 {
    mapping(address => uint256) private _balances;
    mapping(address => mapping(address => uint256)) private _allowances;

    uint256 private _totalSupply;
    string public name;
    string public symbol;
    uint8 public decimals;
    address public owner;
    bool public mintingEnabled;
    uint256 public maxSupply;

    // Events
    event Mint(address indexed to, uint256 amount);
    event Burn(address indexed from, uint256 amount);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
    event MintingToggled(bool enabled);

    modifier onlyOwner() {
        require(msg.sender == owner, "HYPE: caller is not the owner");
        _;
    }

    modifier whenMintingEnabled() {
        require(mintingEnabled, "HYPE: minting is disabled");
        _;
    }

    constructor() {
        name = "HYPE Token";
        symbol = "HYPE";
        decimals = 18;
        owner = msg.sender;
        mintingEnabled = true;
        maxSupply = 1000000000 * 10**decimals; // 1 billion HYPE max supply
        
        // Initial mint to owner: 100 million HYPE
        uint256 initialSupply = 100000000 * 10**decimals;
        _totalSupply = initialSupply;
        _balances[owner] = initialSupply;
        emit Transfer(address(0), owner, initialSupply);
        emit Mint(owner, initialSupply);
    }

    function totalSupply() public view override returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account) public view override returns (uint256) {
        return _balances[account];
    }

    function transfer(address to, uint256 amount) public override returns (bool) {
        address owner = msg.sender;
        _transfer(owner, to, amount);
        return true;
    }

    function allowance(address owner, address spender) public view override returns (uint256) {
        return _allowances[owner][spender];
    }

    function approve(address spender, uint256 amount) public override returns (bool) {
        address owner = msg.sender;
        _approve(owner, spender, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) public override returns (bool) {
        address spender = msg.sender;
        _spendAllowance(from, spender, amount);
        _transfer(from, to, amount);
        return true;
    }

    function mint(address to, uint256 amount) public onlyOwner whenMintingEnabled {
        require(to != address(0), "HYPE: mint to the zero address");
        require(_totalSupply + amount <= maxSupply, "HYPE: exceeds maximum supply");

        _totalSupply += amount;
        unchecked {
            _balances[to] += amount;
        }
        emit Transfer(address(0), to, amount);
        emit Mint(to, amount);
    }

    function burn(uint256 amount) public {
        address account = msg.sender;
        require(account != address(0), "HYPE: burn from the zero address");

        uint256 accountBalance = _balances[account];
        require(accountBalance >= amount, "HYPE: burn amount exceeds balance");
        unchecked {
            _balances[account] = accountBalance - amount;
            _totalSupply -= amount;
        }

        emit Transfer(account, address(0), amount);
        emit Burn(account, amount);
    }

    function burnFrom(address account, uint256 amount) public {
        _spendAllowance(account, msg.sender, amount);
        _burn(account, amount);
    }

    function toggleMinting() public onlyOwner {
        mintingEnabled = !mintingEnabled;
        emit MintingToggled(mintingEnabled);
    }

    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(0), "HYPE: new owner is the zero address");
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }

    function renounceOwnership() public onlyOwner {
        emit OwnershipTransferred(owner, address(0));
        owner = address(0);
    }

    // Internal functions
    function _transfer(address from, address to, uint256 amount) internal {
        require(from != address(0), "HYPE: transfer from the zero address");
        require(to != address(0), "HYPE: transfer to the zero address");

        uint256 fromBalance = _balances[from];
        require(fromBalance >= amount, "HYPE: transfer amount exceeds balance");
        unchecked {
            _balances[from] = fromBalance - amount;
            _balances[to] += amount;
        }

        emit Transfer(from, to, amount);
    }

    function _approve(address owner, address spender, uint256 amount) internal {
        require(owner != address(0), "HYPE: approve from the zero address");
        require(spender != address(0), "HYPE: approve to the zero address");

        _allowances[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }

    function _spendAllowance(address owner, address spender, uint256 amount) internal {
        uint256 currentAllowance = allowance(owner, spender);
        if (currentAllowance != type(uint256).max) {
            require(currentAllowance >= amount, "HYPE: insufficient allowance");
            unchecked {
                _approve(owner, spender, currentAllowance - amount);
            }
        }
    }

    function _burn(address account, uint256 amount) internal {
        require(account != address(0), "HYPE: burn from the zero address");

        uint256 accountBalance = _balances[account];
        require(accountBalance >= amount, "HYPE: burn amount exceeds balance");
        unchecked {
            _balances[account] = accountBalance - amount;
            _totalSupply -= amount;
        }

        emit Transfer(account, address(0), amount);
        emit Burn(account, amount);
    }

    // View functions for token info
    function getTokenInfo() public view returns (
        string memory tokenName,
        string memory tokenSymbol,
        uint8 tokenDecimals,
        uint256 tokenTotalSupply,
        uint256 tokenMaxSupply,
        address tokenOwner,
        bool isMintingEnabled
    ) {
        return (name, symbol, decimals, _totalSupply, maxSupply, owner, mintingEnabled);
    }

    function getRemainingMintableSupply() public view returns (uint256) {
        return maxSupply - _totalSupply;
    }
}