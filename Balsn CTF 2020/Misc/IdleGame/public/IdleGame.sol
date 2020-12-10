pragma solidity =0.5.17;

import "./Tokens.sol";

contract BalsnToken is ERC20 {
    uint randomNumber = 0;
    address public owner;
    
    constructor(uint initialValue) public ERC20("BalsnToken", "BSN") {
        owner = msg.sender;
        _mint(msg.sender, initialValue);
    }
    
    function giveMeMoney() public {
        require(balanceOf(msg.sender) == 0, "BalsnToken: you're too greedy");
        _mint(msg.sender, 1);
    }
}

contract IdleGame is FlashERC20, ContinuousToken {
    uint randomNumber = 0;
    address public owner;
    BalsnToken public BSN;
    mapping(address => uint) public startTime;
    mapping(address => uint) public level;
    
    constructor (address BSNAddr, uint32 reserveRatio) public ContinuousToken(reserveRatio) ERC20("IdleGame", "IDL") {
        owner = msg.sender;
        BSN = BalsnToken(BSNAddr);
        _mint(msg.sender, 0x9453 * scale);
    }
    
    function getReward() public returns (uint) {
        uint points = block.timestamp.sub(startTime[msg.sender]);
        points = points.add(level[msg.sender]).mul(points);
        _mint(msg.sender, points);
        startTime[msg.sender] = block.timestamp;
        return points;
    }
    
    function levelUp() public {
        _burn(msg.sender, level[msg.sender]);
        level[msg.sender] = level[msg.sender].add(1);
    }
    
    function buyGamePoints(uint amount) public returns (uint) {
        uint bought = _continuousMint(amount);
        BSN.transferFrom(msg.sender, address(this), amount);
        _mint(msg.sender, bought);
        return bought;
    }
    
    function sellGamePoints(uint amount) public returns (uint) {
        uint bought = _continuousBurn(amount);
        _burn(msg.sender, amount);
        BSN.transfer(msg.sender, bought);
        return bought;
    }
    
    function giveMeFlag() public {
        _burn(msg.sender, (10 ** 8) * scale);
        Setup(owner).giveMeFlag();
    }
}

contract Setup {
    uint randomNumber = 0;
    bool public sendFlag = false;
    BalsnToken public BSN;
    IdleGame public IDL;
    
    constructor() public {
        uint initialValue = 15000000 * (10 ** 18);
        BSN = new BalsnToken(initialValue);
        IDL = new IdleGame(address(BSN), 999000);
        BSN.approve(address(IDL), uint(-1));
        IDL.buyGamePoints(initialValue);
    }
    
    function giveMeFlag() public {
        require(msg.sender == address(IDL), "Setup: sender incorrect");
        sendFlag = true;
    }
}
